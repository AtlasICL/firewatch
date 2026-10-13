const map = L.map('map').setView([51.505, -0.09], 13)
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);
const hullCoordinates = [
    [51.509, -0.08],
    [51.503, -0.06],
    [51.51, -0.047]
  ];

  const polygon = L.polygon(hullCoordinates, {
    color: '#2563eb',       
    weight: 2,              
    fillColor: '#3b82f6',   
    fillOpacity: 0.4        
  }).addTo(map);

  map.fitBounds(polygon.getBounds(), { padding: [40, 40] });