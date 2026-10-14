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

  const markers = L.layerGroup().addTo(map);

  document.getElementById('plotButton').addEventListener('click', () => {
      const input = document.getElementById('coordinates').value;
      const points = [];

      // Reads each coordinate line-by-line, separate arrays for each
      input.trim().split('\n').forEach(line => {
          const values = line.split(',').map(Number);

          if (
            values.length === 2 &&
            // 0 = latitude, 1 = longitude
            values[0] >= -90 && values[0] <= 90 &&
            values[1] >= -180 && values[1] <= 180
          ) {
              points.push(values);
          }
      });

      if (points.length === 0) {
        alert('Please enter valid coordinates!');
        return;
      }

      points.forEach(point => {
          L.circleMarker(point, {
              radius: 2,
              color: 'red',
          }).addTo(markers);
      });

      map.fitBounds(points);

      console.log(`${points.length} coordinates plotted!`);
  });
