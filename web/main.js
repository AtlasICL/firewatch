import { parseCoordinatesFrom } from "./coordinates.js";
import { settlementsInRange } from "./settlements.js";
import { uploadDownloadFile } from "./upload_download.js";

// Initialise map instance, with initial view of London
const map = L.map("map").setView([51.505, -0.09], 13);
map.zoomControl.setPosition("topright");

const terrain = L.tileLayer(
  "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
  {
    maxZoom: 19,
    attribution:
      "&copy; OpenStreetMap contributors, SRTM | OpenTopoMap (CC-BY-SA)",
  },
);

const satellite = L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    maxZoom: 19,
    attribution: "Tiles &copy; Esri and imagery providers",
  },
);

satellite.addTo(map);
L.control
  .layers(
    {
      Terrain: terrain,
      Satellite: satellite,
    },
    null,
    {
      position: "topright",
      //collapsed: false
    },
  )
  .addTo(map);

// Layers for the currently displayed dataset.
const pointsLayer = L.featureGroup().addTo(map);
const convexHullLayer = L.featureGroup().addTo(map);
const settlementsLayer = L.featureGroup().addTo(map);

// Bumped on every load.
// Used to prevent the hull response of an earlier click overwriting a newly
// selected dataset.
let currentLoadId = 0;

/**
 * Plots the points in a CSV file on the map, and moves the map onto them.
 * Calls quickhull on the set of points, and draws that hull once it returns.
 *
 * @param {File} file - CSV file of `latitude,longitude[,date]` rows.
 */
async function plotFileAndHull(file) {
  const loadId = ++currentLoadId;
  const isStale = () => loadId !== currentLoadId;
  hideLoading();

  const csvData = await file.text();
  if (isStale()) return;

  const points = parseCoordinatesFrom(csvData);
  if (points.length === 0) {
    throw new Error(`${file.name} is empty (no coordinates)`);
  }

  pointsLayer.clearLayers();
  convexHullLayer.clearLayers();
  settlementsLayer.clearLayers();
  for (const point of points) {
    L.circleMarker(point, {
      radius: 7,
      color: "#ff7f0f",
      weight: 1,
      fillColor: "#eb0707",
      fillOpacity: 0.95,
    })
      .bindPopup(point[0] + ", " + point[1])
      .addTo(pointsLayer);
  }

  map.fitBounds(pointsLayer.getBounds(), {
    paddingTopLeft: [55, 55],
    paddingBottomRight: [70, 50],
  });

  showLoading();
  const convexHullCoordinates = await uploadDownloadFile(file);
  if (isStale()) return;

  const hullPoints = parseCoordinatesFrom(convexHullCoordinates);

  L.polygon(hullPoints, {
    color: "#8d05fd",
    weight: 5,
    fillColor: "#8d05fd",
    fillOpacity: 0.4,
  }).addTo(convexHullLayer);
  pointsLayer.bringToFront();
  hideLoading();

  const settlements = await settlementsInRange(hullPoints);
  if (isStale()) return;
  settlements.addTo(settlementsLayer);
}

/**
 * Fetches a premade CSV file (served statically to the user), then plots it
 * and its convex hull.
 *
 * @param {string} path - Path (relative) for the sample CSV.
 */
async function loadSample(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(
      `Failed to fetch ${path} (HTTP status: ${response.status})`,
    );
  }
  const csvData = await response.text();
  const filename = path.split("/").pop();
  await plotFileAndHull(new File([csvData], filename, { type: "text/csv" }));
}

const sampleRadios = document.querySelectorAll('input[name="sample"]');

// File upload logic.
let file = null;
const fileInput = document.getElementById("fileInput");
const fileLabel = document.querySelector('label[for="fileInput"]');
const fileName = document.getElementById("fileName");
const fileHint = document.getElementById("fileHint");
const uploadButton = document.getElementById("uploadButton");
if (fileInput) {
  fileInput.addEventListener("change", (event) => {
    const intendedFile = event.target.files[0];
    if (!intendedFile) return;
    file = intendedFile;
    fileName.textContent = file.name;
    fileHint.textContent = "Click to change file";
    fileLabel.classList.add("has-file");
    uploadButton.disabled = false;
  });
}

const errorOverlay = document.getElementById("errorOverlay");
const errorDismissButton = document.getElementById("errorDismissButton");

function showError() {
  errorOverlay.classList.remove("hidden");
}

errorDismissButton.addEventListener("click", () => {
  errorOverlay.classList.add("hidden");
});
// File upload button logic.
if (uploadButton) {
  uploadButton.addEventListener("click", async () => {
    if (!file) {
      showError();
      return;
    }
    // Uploaded file replaces whichever sample was shown.
    for (const radio of sampleRadios) radio.checked = false;
    try {
      await plotFileAndHull(file);
    } catch (error) {
      hideLoading();
      console.error(error);
      showError();
    }
  });
}

// Sample datasets are radios, so only one can be selected at a time.
for (const radio of sampleRadios) {
  radio.addEventListener("change", async () => {
    if (!radio.checked) return;
    try {
      await loadSample(radio.value);
    } catch (error) {
      hideLoading();
      console.error(error);
      alert(`Couldn't load sample: ${error.message}`);
    }
  });
}

const splashOverlay = document.getElementById("splashOverlay");
const startButton = document.getElementById("startButton");

if (sessionStorage.getItem("splashSeen") === "true") {
  splashOverlay.classList.add("hidden");
}

startButton.addEventListener("click", () => {
  splashOverlay.classList.add("hidden");
  sessionStorage.setItem("splashSeen", "true");
});

const mapLoading = document.getElementById("mapLoading");

function showLoading() {
  mapLoading.hidden = false;
}

function hideLoading() {
  mapLoading.hidden = true;
}
