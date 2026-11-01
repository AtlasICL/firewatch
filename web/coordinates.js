/**
 * Parses CSV text of `latitude,longitude` rows into Leaflet-ready
 * `[latitude, longitude]` pairs. Rows can have an optional date field.
 * Skips blank lines.
 *
 * @param {string} csvString - CSV string (each line is x, y, ...).
 * @returns {[number, number][]} - Parsed output coordinate pair objects.
 * @throws {Error} - Throws is encounters a line with unexpected data.
 */
export function parseCoordinatesFrom(csvString) {
  const coordinates = [];

  for (const [index, line] of csvString.split(/\r?\n/).entries()) {
    if (line.trim() === "") {
      continue;
    }

    // Coordinates are required, date field is optional
    const coordinateFields = line.split(",").slice(0, 2);
    const [latitude, longitude] = coordinateFields.map(Number);
    const isValid =
      coordinateFields.length === 2 &&
      coordinateFields.every((field) => field.trim() !== "") &&
      Number.isFinite(latitude) &&
      Number.isFinite(longitude);
    if (!isValid) {
      throw new Error(
        `Invalid coordinate csv on line ${index + 1}:\n"${line}"`,
      );
    }
    coordinates.push([latitude, longitude]);
  }
  return coordinates;
}

export default parseCoordinatesFrom;
