import { parseCoordinatesFrom } from "./coordinates.js";
import { settlementsInRange } from "./settlements.js";
import { uploadDownloadFile } from "./upload_download.js";

// Initialise map instance, with initial view of London
const map = L.map("map").setView([51.505, -0.09], 13);
map.zoomControl.setPosition("topright");
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// Layers for the currently displayed dataset.
const pointsLayer = L.featureGroup().addTo(map);
const convexHullLayer = L.featureGroup().addTo(map);

// Bumped on every load.
// Used to prevent the hull response of an earlier click overwriting a newly
// selected dataset.
let currentLoadId = 0;

let currentSettlementLayer = null;

/**
 * Plots the points in a CSV file on the map, and moves the map onto them.
 * Calls quickhull on the set of points, and draws that hull once it returns.
 *
 * @param {File} file - CSV file of `latitude,longitude` rows.
 */
async function plotFileAndHull(file) {
  const loadId = ++currentLoadId;
  const isStale = () => loadId !== currentLoadId;

  const csvData = await file.text();
  if (isStale()) return;

  const points = parseCoordinatesFrom(csvData);
  if (points.length === 0) {
    throw new Error(`${file.name} is empty (no coordinates)`);
  }

  pointsLayer.clearLayers();
  convexHullLayer.clearLayers();
  for (const point of points) {
    L.circleMarker(point, {
      radius: 7,
      color: "#ff7f0f",
      weight: 1,
      fillColor: "#eb0707",
      fillOpacity: 0.95,
    }).addTo(pointsLayer);
  }

  // Padding to keep points clear or UI elements.
  map.fitBounds(pointsLayer.getBounds(), {
    paddingTopLeft: [350, 75],
    paddingBottomRight: [50, 50],
  });

  const convexHullCoordinates = await uploadDownloadFile(file);
  if (isStale()) return;

  const parsedCoordinates = parseCoordinatesFrom(convexHullCoordinates);

  updateSettlements(parsedCoordinates, map);

  L.polygon(parsedCoordinates, {
    color: "#8d05fd",
    weight: 5,
    fillColor: "#8d05fd",
    fillOpacity: 0.4,
  }).addTo(convexHullLayer);
  pointsLayer.bringToFront();
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

/**
 * Updates settlements based on current convex hull in view, removes
 * previous settlements if applicable.
 *
 * @param {[number, number][]} hullCoordinates - latitude and longitude coordinate list of convex hull nodes.
 */
async function updateSettlements(hullCoordinates) {
  if (currentSettlementLayer) {
    map.removeLayer(currentSettlementLayer);
    currentSettlementLayer = null;
  }
  currentSettlementLayer = await settlementsInRange(hullCoordinates, map);
}

// File upload logic.
let file = null;
const fileInput = document.getElementById("fileInput");
if (fileInput) {
  fileInput.addEventListener("change", (event) => {
    const intendedFile = event.target.files[0];
    if (!intendedFile) return;
    file = intendedFile;
  });
}

// File upload button logic.
const uploadButton = document.getElementById("uploadButton");
if (uploadButton) {
  uploadButton.addEventListener("click", async () => {
    if (!file) {
      alert("Please choose a CSV to upload.");
      return;
    }
    try {
      await plotFileAndHull(file);
    } catch (error) {
      console.error(error);
      alert(`Couldn't interpret file: ${error.message}`);
    }
  });
}

for (const button of document.querySelectorAll(".sample-button")) {
  button.addEventListener("click", async () => {
    try {
      await loadSample(button.dataset.sample);
    } catch (error) {
      console.error(error);
      alert(`Couldn't load sample: ${error.message}`);
    }
  });
}
