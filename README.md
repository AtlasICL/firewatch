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


### Testing

Run our Python test suite using
```
python3 -m unittest
```

We have a mix of white-box and black-box testing.

### Pseudocode

![Pseudocode of Quickhull algorithm](./img/pseudocode/quickhull_pseudocode.png)

### Limitations, dependencies, and third-party resources

|                           |                                                                                                                                                                                        |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Third-party resources** | The initial datasets were taken from NASA's FIRMS (Fire Information for Resource Management System) dataset, freely available [here](https://firms.modaps.eosdis.nasa.gov/active_fire) |
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

