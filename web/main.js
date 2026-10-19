import { uploadDownloadFile } from "./upload_download.js";

// Initialise map instance, with initial view of London
const map = L.map("map").setView([51.505, -0.09], 13);
map.zoomControl.setPosition('topright');
L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

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
    const { _fileId, _inputS3Key, _uploadS3Key, quickhullCoords } =
      await uploadDownloadFile(file);
    alert(quickhullCoords);
    //insert quickhull functionality here
  });
}

window.sampleMessage = function() {
	alert("A sample dataset will be displayed here (subject to change)");
  //functionality to display sample dataset to be added
};
