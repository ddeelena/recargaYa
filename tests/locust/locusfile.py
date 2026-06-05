from locust import HttpUser, task, between

class ClienteRecarga(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(4)
    def recarga_normal(self):
        self.client.post("/recarga", json={
            "monto": 10000,
            "premium": False
        })

    @task(2)
    def recarga_premium(self):
        self.client.post("/recarga", json={
            "monto": 30000,
            "premium": True
        })

    @task(1)
    def recarga_minima(self):
        self.client.post("/recarga", json={
            "monto": 1000,
            "premium": False
        })

    @task(1)
    def health_check(self):
        self.client.get("/health")
