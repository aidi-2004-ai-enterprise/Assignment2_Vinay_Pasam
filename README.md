# Penguin Species Prediction API

## Project Overview
This project provides a REST API to predict penguin species based on physical measurements and categorical features using a trained XGBoost model. The API is built with FastAPI, containerized using Docker, and deployed on Google Cloud Run for scalable, serverless hosting. The model file and label encoder are stored in Google Cloud Storage and accessed securely via a GCP service account.

Load testing is performed using Locust to ensure the application’s robustness and performance under different traffic scenarios.

#Cloud link for penguin species prediction

https://penguin-api-111837677549.northamerica-northeast1.run.app/docs#/default/predict_species_predict_post


---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Docker Desktop
- Google Cloud SDK with authentication (`gcloud init`)
- Google Cloud project with enabled APIs:
  - Cloud Run
  - Artifact Registry
  - Google Cloud Storage
- Service account JSON key with Storage Object Viewer permissions
- Locust for load testing

### Local Setup
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/penguin-api.git
   cd penguin-api
Create and activate a virtual environment:

bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Set Google credentials environment variable:

bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/sa-key.json"
Run the API locally:

bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
Access API docs at: http://localhost:8080/docs

Docker Setup
Build and run locally:

bash
docker build -t penguin-api .
docker run -p 8080:8080 penguin-api

Cloud Deployment
Push Docker image to Artifact Registry.

Deploy image to Cloud Run.

Test live endpoints via Cloud Run URL.

API Documentation
POST /predict
Predict penguin species from features.

Request body example:

json

{
  "bill_length_mm": 45.1,
  "bill_depth_mm": 14.5,
  "flipper_length_mm": 220,
  "body_mass_g": 4500,
  "sex": "Male",
  "island": "Biscoe"
}
Response example:

json

{
  "predicted_species": "Adelie"
}
Edge Cases That Might Break the Model in Production
Out-of-range numerical values: Negative or zero values for features like body mass or flipper length which are biologically invalid.

Missing categorical fields: Absence of sex or island information can cause incorrect one-hot encoding or prediction failures.

Unseen categories: If new categories appear for island or sex, the model may fail or produce unreliable predictions.

Corrupted or incomplete input JSON: Malformed or partial requests may cause server errors.

What Happens if the Model File Becomes Corrupted?
The model loading step will fail, likely causing the app to crash or return 500 errors.

To mitigate, implement try-except blocks during model load and fallbacks, such as:

Return clear error messages.

Alert monitoring systems.

Use model versioning with backups.

Regular automated testing ensures model file integrity.

Realistic Load for Penguin Classification Service
Anticipated traffic is low to moderate: approx. 10-50 requests per second under normal operation.

Peaks could occur during research or batch inference jobs.

Cloud Run auto-scaling supports higher burst loads but testing should confirm upper limits.

How to Optimize if Response Times are Too Slow
Model caching: Load the model once at startup instead of per request.

Increase Cloud Run CPU/Memory: Allocate more resources for faster inference.

Batch predictions: Aggregate multiple requests where feasible.

Use async endpoints: For better concurrency handling.

Add caching layers: Cache frequent predictions or partial computations.

Important Metrics for ML Inference APIs
Latency: Time per prediction request.

Throughput: Requests handled per second.

Error rate: Percentage of failed predictions or server errors.

Resource usage: CPU, memory consumption during inference.

Cold start time: Time to spin up new container instances in Cloud Run.

Why Docker Layer Caching Is Important for Build Speed
Docker caches unchanged layers during builds to avoid re-executing all commands.

Leveraging caching reduces rebuild time, especially for large dependencies.

Example: Installing dependencies before copying source code ensures only app changes trigger rebuilds of app layers, not dependencies.

Security Risks Running Containers as Root
Running as root allows processes inside the container full permissions, increasing risk if compromised.

It may lead to privilege escalation on the host machine.

Best practice: Run containers as non-root users with least privilege.

Add user creation and switch steps in Dockerfile.

How Cloud Auto-Scaling Affects Load Test Results
Auto-scaling allows the app to handle increased traffic by creating new container instances.

Initial spikes cause "cold starts" with higher latency.

Sustained load results in faster response times as more instances serve traffic.

Scale down after traffic drops to reduce cost.

What Would Happen With 10x More Traffic?
Without proper scaling, response times will degrade, error rates increase.

Cloud Run auto-scaling will attempt to add instances but may hit concurrency or quota limits.

Costs will increase significantly.

Requires optimization in scaling parameters, resource allocation, and possibly load balancing.

How to Monitor Performance in Production
Use Google Cloud Monitoring and Logging.

Track metrics like latency, error rate, CPU/memory usage.

Set up alerts for anomalies or resource limits.

Use tracing tools (e.g., OpenTelemetry) for detailed request insights.

Periodically review logs and metrics dashboards.

How to Implement Blue-Green Deployment
Deploy new version to a separate environment (green) while old (blue) continues serving.

Test green environment thoroughly.

Switch traffic from blue to green after verification.

Roll back by switching back if issues arise.

Minimizes downtime and deployment risk.

What to Do If Deployment Fails in Production
Immediately rollback to last stable version.

Check Cloud Run and container logs for errors.

Investigate changes causing failures.

Fix bugs and redeploy.

Use feature flags to disable risky features.

What Happens If Your Container Uses Too Much Memory?
Cloud Run may kill the container (OOMKilled).

Application crashes or restarts frequently.

Leads to increased latency and request failures.

Mitigation:

Optimize code and dependencies.

Increase memory allocation in Cloud Run settings.

Use memory profiling and monitoring.
