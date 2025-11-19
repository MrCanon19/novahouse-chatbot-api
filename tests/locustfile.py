"""
Load Testing Configuration for NovaHouse Chatbot API
Usage:
    locust -f locustfile.py --host=http://localhost:5000
    locust -f locustfile.py --host=https://glass-core-467907-e9.ey.r.appspot.com

    # Headless mode
    locust -f locustfile.py --headless --users 100 --spawn-rate 10 --run-time 60s
"""

import random

from locust import HttpUser, between, task


class ChatbotUser(HttpUser):
    """Simulates a typical chatbot user"""

    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        """Called when a simulated user starts"""
        self.session_id = f"load-test-{random.randint(1000, 9999)}"

    @task(10)  # Weight: 10 (most common operation)
    def send_message(self):
        """Test chatbot message endpoint"""
        messages = [
            "Witam, interesuje mnie konsultacja",
            "Jakie są ceny?",
            "Chciałbym umówić spotkanie",
            "Gdzie znajduje się biuro?",
            "Jakie macie realizacje?",
        ]

        self.client.post(
            "/api/chatbot/message",
            json={
                "message": random.choice(messages),
                "session_id": self.session_id,
                "language": "pl",
            },
            headers={"Content-Type": "application/json", "X-API-Key": "test-api-key"},
        )

    @task(5)  # Weight: 5
    def get_health(self):
        """Test health endpoint"""
        self.client.get("/api/health")

    @task(3)  # Weight: 3
    def search_knowledge(self):
        """Test knowledge base search"""
        queries = ["projekt", "cena", "realizacja", "technologia", "usługi"]

        self.client.get(
            f"/api/knowledge/search",
            params={"query": random.choice(queries), "limit": 5},
            headers={"X-API-Key": "test-api-key"},
        )

    @task(2)  # Weight: 2
    def get_analytics(self):
        """Test analytics endpoint"""
        self.client.get("/api/analytics/summary", headers={"X-API-Key": "test-api-key"})

    @task(1)  # Weight: 1
    def create_lead(self):
        """Test lead creation"""
        self.client.post(
            "/api/leads",
            json={
                "name": f"Test User {random.randint(1, 1000)}",
                "email": f"test{random.randint(1, 1000)}@example.com",
                "phone": f"+48{random.randint(100000000, 999999999)}",
                "source": "load_test",
                "message": "Load testing lead",
            },
            headers={"Content-Type": "application/json", "X-API-Key": "test-api-key"},
        )


class AdminUser(HttpUser):
    """Simulates an admin dashboard user"""

    wait_time = between(2, 5)

    @task(5)
    def view_dashboard(self):
        """Test dashboard widgets"""
        self.client.get("/api/dashboard/widgets", headers={"X-API-Key": "test-api-key"})

    @task(3)
    def view_leads(self):
        """Test leads listing"""
        self.client.get("/api/leads?page=1&per_page=20", headers={"X-API-Key": "test-api-key"})

    @task(2)
    def view_analytics(self):
        """Test detailed analytics"""
        self.client.get("/api/analytics/detailed", headers={"X-API-Key": "test-api-key"})


class ApiStressTest(HttpUser):
    """Heavy load test for stress testing"""

    wait_time = between(0.1, 0.5)  # Very aggressive

    @task
    def spam_health(self):
        """Spam health endpoint"""
        self.client.get("/api/health")

    @task
    def spam_chatbot(self):
        """Spam chatbot endpoint"""
        self.client.post(
            "/api/chatbot/message",
            json={"message": "stress test", "session_id": f"stress-{random.randint(1, 100)}"},
            headers={"X-API-Key": "test-api-key"},
        )


# Load test scenarios (run different user types)
# To use: locust -f locustfile.py --host=http://localhost:5000 --users 50 --spawn-rate 5
# This will simulate 50 users (mixture of ChatbotUser, AdminUser, ApiStressTest)
