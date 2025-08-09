## Containerization and Deployment Process

### Docker Containerization

- **Dockerfile**:
  - Base image: `python:3.10-slim`
  - Installed dependencies via `requirements.txt`
  - Copied source code and model loader
  - Exposed port 8080 for Cloud Run compatibility
  - Used `uvicorn` to serve FastAPI app

- **.dockerignore**:
  - Excluded unnecessary files:
    ```
    __pycache__
    *.pyc
    .env
    .git
    .gitignore
    *.md
    ```

### Local Build and Test

- Built Docker image:
  ```bash
  docker build -t penguin-api .
Ran container locally:

bash
docker run -p 8080:8080 penguin-api
Verified API endpoints accessible on http://localhost:8080/docs

Used docker inspect penguin-api to analyze image layers:

Total image size: ~150MB (mainly due to Python and dependencies)

Layer caching utilized by installing dependencies before copying source

GCP Service Account Setup
Created service account penguin-api-sa

Assigned roles: Storage Object Viewer, Storage Bucket Viewer

Downloaded JSON key and securely stored locally

Set environment variable GOOGLE_APPLICATION_CREDENTIALS for authentication

Mounted key file in Docker container for local testing

Artifact Registry
Created Artifact Registry repository penguin-repo in region northamerica-northeast1

Tagged Docker image for Artifact Registry:

bash
docker tag penguin-api us-central1-docker.pkg.dev/top-broker-468417-b8/penguin-repo/penguin-api:latest
Pushed image to Artifact Registry:

bash
docker push us-central1-docker.pkg.dev/top-broker-468417-b8/penguin-repo/penguin-api:latest
Cloud Run Deployment
Deployed using CLI:

bash
gcloud run deploy penguin-api \
  --image=us-central1-docker.pkg.dev/top-broker-468417-b8/penguin-repo/penguin-api:latest \
  --platform=managed \
  --region=northamerica-northeast1 \
  --allow-unauthenticated
Configured 1 CPU, 4 GB memory

Port 8080 exposed

Verified service URL and endpoint accessibility

Issues Encountered and Solutions
Issue: API failed to load model due to missing service account environment variable inside container
Solution: Mounted service account key as read-only volume and set environment variable inside Docker run command.

Issue: Deployment failed with image not found error
Solution: Fixed Docker image tagging and pushed correctly to Artifact Registry.

Issue: Locust load tests failed due to incorrect target URL and missing payload variable
Solution: Updated locustfile.py with proper host and JSON payload.

Final Cloud Run URL
https://penguin-api-111837677549.northamerica-northeast1.run.app/docs
(Replace with your actual deployed URL)

Notes on Security and Performance
Service account key is never committed to version control.

Docker container runs as non-root user (added in Dockerfile).

Monitored CPU and memory usage with Cloud Monitoring.

Enabled autoscaling with max instances = 10.