/**
 * Takes quickhull node coordinates and places a layer of affected settlement locations on the map
 * pulled from the natural earth dataset.
 *
 * @param {[number, number][]} parsedCoordinates - latitude and longitude coordinate list of convex hull nodes.
 * @param {L.map} map - leaflet.js map instance to add settlement markers to.
 * @returns {Promise<L.GeoJSON>} - Layer of individual markers of settlements within the convex hull. 
 */
export async function settlementsInRange(parsedCoordinates, map) {
  // Convert to geoJSON
  const hullGeoJSON = L.geoJSON({
    type: "Feature",
    geometry: {
      type: "Polygon",
      // Swap lat and long with geojson convention
      coordinates: [
        [
          ...parsedCoordinates.map(([lat, lng]) => [lng, lat]),
          [parsedCoordinates[0][1], parsedCoordinates[0][0]],
        ],
      ],
    },
  });

  // Get dataset from geoJSON
  const res = await fetch("settlement_dataset.json");
  const data = await res.json();

  // Build settlement layer onto map
  const settlementLayer = L.geoJSON(data, {
    // Apply filter to return only settlements within the convex hull region
    filter: (feature) => {
      const [lng, lat] = feature.geometry.coordinates;
      const matches = leafletPip.pointInLayer([lng, lat], hullGeoJSON);
      return matches.length > 0;
    },
    pointToLayer: (feature, latlng) => {
      return L.circleMarker(latlng, {
        radius: 5,
        fillColor: "#0078A8",
        color: "#ffffff",
        weight: 1,
        fillOpacity: 0.8,
      });
    },
    onEachFeature: (feature, layer) => {
      layer.bindPopup(
        `<strong> Affected Area: ${feature.properties.name}</strong>`,
      );
    },
  }).addTo(map);

  return settlementLayer;
}

export default settlementsInRange;
