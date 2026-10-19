/**
 * Parses CSV text of `latitude,longitude` rows into Leaflet-ready
 * `[latitude, longitude]` pairs. Blank lines are skipped, matching the Python
 * parser.
 *
 * @param {string} csvString - CSV string (each line is x, y).
 * @returns {[number, number][]} - Parsed output coordinate pair objects.
 * @throws {Error} - Throws is encounters a line with unexpected data.
 */
export function parseCoordinatesFrom(csvString) {
  const coordinates = [];

  for (const [index, line] of csvString.split(/\r?\n/).entries()) {
    if (line.trim() === "") {
      continue;
    }

    const vals = line.split(",");
    const [latitude, longitude] = vals.map(Number);
    const isValid =
      vals.length === 2 &&
      vals.every((field) => field.trim() !== "") &&
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
