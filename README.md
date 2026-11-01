## ECM3428 Group Project Submission

|                        |                                                                                                                                          |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Project title**      | Satellite Fire Watch                                                                                                                     |
| **Selected algorithm** | Quickhull                                                                                                                                |
| **Problem statement**  | Given a set of raw coordinate data from fire monitoring satellites, identify the convex hull (which represents the surface area at risk) |
| **Intended users**     | Fire departments in affected areas, wildfire researchers                                                                                 |


### URL
The website is live at [satellitefirewatch.com](https://satellitefirewatch.com).

### Install

- The website is hosted on AWS, using S3 for file storage and Lambdas for
  serverless compute.
- For running locally, the only requirement is a Python runtime (3.12+). 
- Try it out locally using:
  ```
  python3 -m venv venv
  source venv/bin/activate # (or ./venv/Scripts/Activate.ps1 on Windows)
  pip install -r requirements.txt
  python3 -m http.server
  ```
  And then visit http://localhost:8000.

```mermaid
flowchart LR
    user(["Visitor's browser"])

    subgraph CF["Cloudflare"]
        dns["DNS<br/>satellitefirewatch.com"]
        worker["Worker: firewatch<br/>serves `web/` subdir as static files"]
    end

    subgraph AWS["AWS eu-north-1"]
        apigw["API Gateway<br/>HTTP API"]
        transfer["Lambda<br/>src.transfer_lambda.generate_url"]
        qh["Lambda<br/>src.quickhull_lambda.lambda_handler"]
        s3[("S3<br/>s3-upload-bucket-firewatch")]
    end

    %% Edge deployment & static hosting / delivery through Cloudflare
    user -- "loads the page" --> dns --> worker

    %% Upload Presigned URL flow
    user -- "1. POST /generate_url" --> apigw
    apigw --> transfer
    transfer -. "generates presigned PUT" .-> s3
    transfer --> apigw
    apigw -- "2. returns presigned upload URL" --> user
    user -- "3. PUT CSV directly" --> s3

    %% Processing & Download flow
    user -- "4. POST /quickhull_download" --> apigw
    apigw --> qh
    qh -- "reads raw CSV & writes hull CSV" --> s3
    qh -. "generates presigned GET" .-> s3
    qh --> apigw
    apigw -- "5. returns presigned download URL" --> user
    user -- "6. GET hull CSV directly" --> s3
```

### Testing

Install the development dependencies, then run our Python test suite using
```
pip install -r requirements-dev.txt
python3 -m unittest
```

We have a mix of white-box and black-box testing.

### Pseudocode

![Pseudocode of Quickhull algorithm](./img/pseudocode/quickhull_pseudocode.png)

### Limitations, dependencies, and third-party resources

|                           |                                                                                                                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Third-party resources** | The initial datasets for historic fire locations were taken from NASA's FIRMS (Fire Information for Resource Management System) dataset, freely available [here](https://firms.modaps.eosdis.nasa.gov/active_fire). Settlement data is gathered from the Natural Earth Populated Places dataset, freely available [here](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/).|
| **Limitations**           | TODO                                                                                                                                                                                   |
| **Dependencies**          | Python 3.12+ for runtime. Amazon AWS S3 and Lambdas for file storage and compute (and AWS SDK for deployment). Cloudflare for DNS and edge hosting.                                    |

### Individual Contributions

> **Emre Acarsoy**:
- stuff
- stuff

> **Luca Croci**:
- stuff
- stuff

> **Luca Pacitti**:
- stuff
- stuff

> **Harry Taylor**:
- stuff
- stuff

> **Jack Wyatt**:
- stuff
- stuff

### Acknowledgment of genAI use

