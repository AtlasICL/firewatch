//TODO: add commenting
import { uploadDownloadFile} from './upload_download.js';

// Initialise map instance, with initial view of London
const map = L.map('map').setView([51.505, -0.09], 13)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

// File upload logic.
let file = null;
const fileInput = document.getElementById('fileInput');
if (fileInput) {
    fileInput.addEventListener('change', (event) => {
        const intendedFile = event.target.files[0];
        if (!intendedFile) return;
        file = intendedFile;
});
}

// File upload button logic.
const uploadButton = document.getElementById('uploadButton');
if (uploadButton) {
    uploadButton.addEventListener('click', async () => {
        const {fileId, s3Key, content} = await uploadDownloadFile(file);
        alert(content)
        //insert quickhull functionality here
    });
}

