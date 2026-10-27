/**
 * Uploads a CSV file to S3 via a presigned URL, triggers quickhull on it,
 * then downloads the resulting convex hull.
 *
 * @param {File} file - The CSV file selected by the user.
 * @param {string} apiEndpoint
 * [apiEndpoint='https://xnyu0pnd88.execute-api.eu-north-1.amazonaws.com']
 * - API gateway handling incoming/outgoing file requests.
 * @returns {Promise<string>} - Convex hull as CSV text (`latitude,longitude`
 * rows), as returned from S3.
 * @throws {Error} - Error relating to failed S3 upload/download.
 */
export async function uploadDownloadFile(
  file,
  apiEndpoint = "https://xnyu0pnd88.execute-api.eu-north-1.amazonaws.com",
) {
  //Get download/upload URLs from api endpoint response
  const presignUploadResponse = await fetch(apiEndpoint + "/generate_url", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ filename: file.name }),
  });

  if (!presignUploadResponse.ok) {
    //s3 URL get
    const errorBody = await presignUploadResponse.text();
    console.error("SERVER 500 DETAILS:", errorBody);
    throw new Error(`Failed to get S3 upload URL: ${errorBody}`);
  }
  const { upload_url: uploadUrl, input_s3_key: uploadS3Key } =
    await presignUploadResponse.json();
  //Attempt S3 upload
  const uploadResponse = await fetch(uploadUrl, {
    method: "PUT",
    headers: { "Content-Type": "text/csv" },
    body: file,
  });

  if (!uploadResponse.ok) {
    throw new Error("S3 upload failed");
  }

  const presignDownloadResponse = await fetch(
    apiEndpoint + "/quickhull_download",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input_s3_key: uploadS3Key }),
    },
  );

  if (!presignDownloadResponse.ok) {
    //s3 URL get
    throw new Error("Failed to get S3 URL");
  }
  const { download_url: downloadUrl } = await presignDownloadResponse.json();
  //Attempt S3 download
  const downloadResponse = await fetch(downloadUrl);

  if (!downloadResponse.ok) {
    throw new Error("S3 download failed");
  }
  const convexHullCoordinates = await downloadResponse.text();

  return convexHullCoordinates;
}

export default uploadDownloadFile;
