from locust import HttpUser, task, between
import random

class BMSUser(HttpUser):
    wait_time = between(1, 3)

    @task(35)
    def browse_events(self):
        self.client.get("/api/events")

    @task(30)
    def check_seats(self):
        eid = random.randint(1, 3)
        self.client.get(f"/api/events/{eid}/seats")

    @task(20)
    def book_ticket(self):
        self.client.post("/api/bookings",
            json={"event_id": random.randint(1,3), "seats": 2},
            headers={"Content-Type": "application/json"})

    @task(15)
    def health_check(self):
        self.client.get("/health/ready")
