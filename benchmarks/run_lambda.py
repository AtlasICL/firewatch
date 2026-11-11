from pathlib import Path
import requests

def run_lambda(csv_path: Path):
    """
    Upload a CSV file, runs quickhull via api, and download its output.

    :param csv_path: Path to the CSV file to process.
    :raises Exception: If generating an upload URL, uploading the file, running
        the quickhull job, or downloading its output fails.
    :return: Downloaded convex hull.
    :rtype: str
    """
    TRANSFER_URL: str = "https://xnyu0pnd88.execute-api.eu-north-1" \
                ".amazonaws.com/generate_url"

    QUICKHULL_URL: str = "https://xnyu0pnd88.execute-api.eu-north-1" \
                ".amazonaws.com/quickhull_download"

    url_gen_res: requests.Response = requests.post(
        TRANSFER_URL, json={"filename": csv_path.name}, timeout=10
    )

    if url_gen_res.status_code != 200:
       raise Exception(f"Failed to generate upload URL {url_gen_res.text}")

    upload_url_data: dict[str, str] = url_gen_res.json()
    upload_url: str = upload_url_data["upload_url"]
    s3_key: str = upload_url_data["input_s3_key"]

    with csv_path.open("rb") as f:
        upload_res: requests.Response = requests.put(
            upload_url,
            data=f,
            headers={"Content-Type": "text/csv"},
            timeout=30,
        )

    if upload_res.status_code != 200:
        raise Exception(
            f"Failed to generate upload URL {url_gen_res.text}"
        )

    quickhull_res: requests.Response = requests.post(
        QUICKHULL_URL, json={"input_s3_key": s3_key}, timeout=15
    )

    if upload_res.status_code != 200:
        raise Exception(
            f"Failed to generate upload URL {quickhull_res.text}"
        )

    download_url_data: dict[str, str] = quickhull_res.json()
    download_url = download_url_data["download_url"]

    download_res: requests.Response = requests.get(
        download_url, json={"filename": csv_path.name}, timeout=10
    )
    if upload_res.status_code != 200:
        raise Exception(
            f"Failed to generate upload URL {download_res.text}"
        )

    return download_res.text.strip().replace("\r\n", "\n")