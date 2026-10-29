// Parsed settlement dataset, fetched once and shared between loads.
let datasetPromise = null;

/**
 * Fetches and parses the settlement dataset, caching the result. A failed
 * fetch is not cached, so the next call retries.
 *
 * @returns {Promise<object>} - GeoJSON FeatureCollection of settlement points.
 */
function loadSettlementDataset() {
  datasetPromise ??= fetch("settlement_dataset.json")
    .then((response) => {
      if (!response.ok) {
        throw new Error(
          `Failed to fetch settlement data (HTTP status: ${response.status})`,
        );
      }
      return response.json();
    })
    .catch((error) => {
      datasetPromise = null;
      throw error;
    });
  return datasetPromise;
}

/**
 * Whether a point lies inside (or on the edge of) a convex polygon: it must
 * be on the same side of every edge. Works for either winding order.
 *
 * @param {[number, number]} point - latitude and longitude of the point.
 * @param {[number, number][]} hull - latitude and longitude coordinate list of
 * convex hull nodes, in order around the hull.
 * @returns {boolean} - true if the point is inside or on the hull.
 */
export function isInsideConvexHull([lat, lng], hull) {
  if (hull.length < 3) return false;

  let sign = 0;
  for (let i = 0; i < hull.length; i++) {
    const [latitudeA, longitudeA] = hull[i];
    const [latitudeB, longitudeB] = hull[(i + 1) % hull.length];
    const cross_product =
      (latitudeB - latitudeA) * (lng - longitudeA) -
      (longitudeB - longitudeA) * (lat - latitudeA);
    if (cross_product === 0) continue;
    if (sign === 0) sign = Math.sign(cross_product);
    else if (Math.sign(cross_product) !== sign) return false;
  }
  return true;
}

/**
 * Builds the popup content for a settlement: its name, where it is, and its
 * population when known. Uses text nodes so names are never parsed as HTML.
 *
 * @param {object} properties - Natural Earth properties of the settlement.
 * @returns {HTMLElement} - Popup content.
 */
function settlementPopup({ name, adm1name, adm0name, pop_max }) {
  const popup = document.createElement("div");

  const title = document.createElement("strong");
  title.textContent = `Affected area: ${name}`;
  popup.append(title);

  // Skip regions with repeating settlement or country name.
  const location = [adm1name, adm0name].filter(
    (part, i, parts) => part && part !== name && parts.indexOf(part) === i,
  );
  if (location.length > 0) {
    const line = document.createElement("div");
    line.textContent = location.join(", ");
    popup.append(line);
  }

  // The Natural Earth dataset we use uses 0 or -99 for an unknown population.
  // We ignore those.
  if (pop_max > 0) {
    const line = document.createElement("div");
    line.textContent = `Population: ${pop_max.toLocaleString()}`;
    popup.append(line);
  }

  return popup;
}

/**
 * Builds a layer of markers for the settlements from the Natural Earth
 * dataset inside a given convex hull.
 *
 * @param {[number, number][]} hullCoordinates - latitude and longitude
 * coordinate list of the nodes making up the convex hull.
 * @returns {Promise<L.GeoJSON>} - Layer of individual markers of settlements
 * located within the convex hull.
 */
export async function settlementsInRange(hullCoordinates) {
  const data = await loadSettlementDataset();

  return L.geoJSON(data, {
    filter: (feature) => {
      const [lng, lat] = feature.geometry.coordinates;
      return isInsideConvexHull([lat, lng], hullCoordinates);
    },
    pointToLayer: (feature, latlng) =>
      L.circleMarker(latlng, {
        radius: 5,
        fillColor: "#0078A8",
        color: "#ffffff",
        weight: 1,
        fillOpacity: 0.8,
      }),
    onEachFeature: (feature, layer) => {
      layer.bindPopup(settlementPopup(feature.properties));
    },
  });
}

export default settlementsInRange;
