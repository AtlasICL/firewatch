import unittest
from pathlib import Path

import requests

RESOURCES: Path = Path(__file__).resolve().parent.parent / "resources"
TRANSFER_URL: str = (
    "https://xnyu0pnd88.execute-api.eu-north-1 .amazonaws.com/generate_url"
)

QUICKHULL_URL: str = (
    "https://xnyu0pnd88.execute-api.eu-north-1"
    ".amazonaws.com/quickhull_download"
)


class TestLambda(unittest.TestCase):
    def __lambda_run(self, csv_path):
        """
        Helper function for uploading file to api endpoint, running
        quickhull and receiving download url.

        :param csv_path: Path object for test csv
        :type csv_path: Path
        :return: HTTP response with download URL
        :rtype: requests.Response
        """
        url_gen_res: requests.Response = requests.post(
            TRANSFER_URL, json={"filename": csv_path.name}, timeout=10
        )
        self.assertEqual(
            url_gen_res.status_code,
            200,
            f"Failed to generate upload URL {url_gen_res.text}",
        )

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
        self.assertEqual(
            upload_res.status_code,
            200,
            f"Failed to upload to S3 {upload_res.text}",
        )

        quickhull_res: requests.Response = requests.post(
            QUICKHULL_URL, json={"input_s3_key": s3_key}, timeout=15
        )
        return quickhull_res

    def test_successful_lambda_run(self):
        """
        Test Upload/Quickhull on valid csv file.
        """
        csv_path: Path = RESOURCES / "valid_csv_files" / "normal.csv"

        quickhull_res: requests.Response = self.__lambda_run(csv_path)

        self.assertEqual(
            quickhull_res.status_code,
            200,
            f"Failed to run quickhull {quickhull_res.text}",
        )

        download_url_data: dict[str, str] = quickhull_res.json()
        download_url = download_url_data["download_url"]

        download_res: requests.Response = requests.get(
            download_url, json={"filename": csv_path.name}, timeout=10
        )
        self.assertEqual(
            download_res.status_code,
            200,
            f"Failed to download from S3 {download_res.text}",
        )

        actual_text: str = download_res.text.strip().replace("\r\n", "\n")

        expected_text: str = (
            "51.5212,-3.6538\n"
            "53.569,-0.5875\n"
            "55.5915,-3.6387\n"
            "54.8854,-6.7712\n"
            "51.5231,-3.6689"
        )

        self.assertEqual(actual_text, expected_text)

    def test_invalid_csv_lambda_run(self):
        """
        Test Upload/Quickhull on invalid csv file.
        """
        csv_path: Path = (
            RESOURCES / "invalid_csv_files" / "missing_element.csv"
        )

        quickhull_res: requests.Response = self.__lambda_run(csv_path)

        self.assertEqual(quickhull_res.status_code, 500)
        self.assertEqual(
            {
                "error": "Failed to parse CSV file "
                + "/tmp/current.csv: "
                + "could not convert string to float: '15/08/2025'"
            },
            quickhull_res.json(),
        )
