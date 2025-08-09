from locust import HttpUser, task, between

class PenguinUser(HttpUser):
    host = "http://localhost:8080"  # Change this to your deployed URL when testing cloud
    wait_time = between(1, 3)  # Wait time between tasks

    @task
    def predict(self):
        json_payload = {
            "bill_length_mm": 45.0,
            "bill_depth_mm": 14.5,
            "flipper_length_mm": 210,
            "body_mass_g": 4500,
            "sex": "Male",
            "island": "Biscoe"
        }
        self.client.post("/predict", json=json_payload)
