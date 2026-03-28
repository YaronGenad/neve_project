"""
Al-Hasade Load Test — Locust configuration.

Simulates 50 concurrent teachers performing the full workflow:
  register/login → submit generation → poll status → approve/reject

Run:
  pip install locust
  locust -f locustfile.py --host=http://localhost:8000

  # Headless (CI / automated):
  locust -f locustfile.py --host=http://localhost:8000 \
         --users 50 --spawn-rate 5 --run-time 2m --headless

Performance targets (from production_ready_plan_v2.md):
  - BM25 search latency      < 50 ms
  - Redis cache hit latency  <  5 ms
  - Generation submit        < 500 ms  (background task, not full pipeline)
  - /health                  < 100 ms
"""
import random
import uuid

from locust import HttpUser, SequentialTaskSet, between, events, task


# ── Shared data ────────────────────────────────────────────────────────────────

SUBJECTS = ["מתמטיקה", "מדעים", "עברית", "היסטוריה", "ביולוגיה", "כימיה", "פיזיקה", "תנ\"ך", "אנגלית"]
TOPICS   = ["תאים", "שברים", "שירה", "ציונות", "פוטוסינתזה", "חומצות", "כוחות", "שיבת ציון", "grammar"]
GRADES   = ["ג-ד", "ה-ו", "ז-ח", "ח-ט", "י-יא", "יא-יב"]


# ── Task sets ──────────────────────────────────────────────────────────────────

class TeacherWorkflow(SequentialTaskSet):
    """
    Simulates a teacher's complete session:
    1. Register (once)
    2. Login → get access token
    3. Search for existing materials
    4. Submit a generation request
    5. Poll generation status
    6. Approve or reject the result
    """

    token: str = ""
    generation_id: str = ""
    material_id: str = ""

    def on_start(self):
        """Register and login before running tasks."""
        email = f"load_test_{uuid.uuid4().hex[:8]}@example.com"
        password = "loadtest-password-123"

        # Register
        self.client.post(
            "/auth/register",
            json={"email": email, "password": password, "full_name": "Load Test Teacher"},
            name="/auth/register",
        )

        # Login
        resp = self.client.post(
            "/auth/login",
            data={"username": email, "password": password},
            name="/auth/login",
        )
        if resp.status_code == 200:
            self.token = resp.json().get("access_token", "")

    def _auth_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}"}

    @task
    def search_existing_materials(self):
        """Search for existing materials (debounced as the teacher types)."""
        subject = random.choice(SUBJECTS)
        topic = random.choice(TOPICS)
        with self.client.get(
            f"/search/?q={subject} {topic}",
            headers=self._auth_headers(),
            name="/search/",
            catch_response=True,
        ) as resp:
            if resp.status_code not in (200, 401, 403):
                resp.failure(f"Search failed: {resp.status_code}")

    @task
    def submit_generation(self):
        """Submit a generation request."""
        subject = random.choice(SUBJECTS)
        topic = random.choice(TOPICS)
        grade = random.choice(GRADES)

        with self.client.post(
            "/generations/",
            json={"subject": subject, "topic": topic, "grade": grade, "rounds": 2},
            headers=self._auth_headers(),
            name="/generations/ (submit)",
            catch_response=True,
        ) as resp:
            if resp.status_code == 202:
                self.generation_id = resp.json().get("generation_id", "")
            elif resp.status_code in (401, 403, 429):
                resp.success()  # expected rate-limit or auth
            else:
                resp.failure(f"Submit failed: {resp.status_code}")

    @task
    def poll_generation_status(self):
        """Poll for generation status (teachers usually poll every 5s)."""
        if not self.generation_id:
            return
        with self.client.get(
            f"/generations/{self.generation_id}",
            headers=self._auth_headers(),
            name="/generations/{id} (poll)",
            catch_response=True,
        ) as resp:
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "completed":
                    self.material_id = data.get("material_id", "")
            elif resp.status_code in (404, 401, 403):
                resp.success()
            else:
                resp.failure(f"Poll failed: {resp.status_code}")

    @task
    def approve_material(self):
        """Approve a completed material."""
        if not self.material_id:
            return
        with self.client.post(
            f"/materials/{self.material_id}/approve",
            headers=self._auth_headers(),
            name="/materials/{id}/approve",
            catch_response=True,
        ) as resp:
            if resp.status_code in (200, 404, 401, 403):
                resp.success()
            else:
                resp.failure(f"Approve failed: {resp.status_code}")
            self.material_id = ""  # reset for next round

    @task
    def get_history(self):
        """List the teacher's generation history."""
        with self.client.get(
            "/generations/?limit=10&offset=0",
            headers=self._auth_headers(),
            name="/generations/ (list)",
            catch_response=True,
        ) as resp:
            if resp.status_code not in (200, 401, 403):
                resp.failure(f"History failed: {resp.status_code}")


class TeacherUser(HttpUser):
    """
    Represents a single teacher.
    Wait 1–5 seconds between tasks (realistic browser interaction speed).
    """
    tasks = [TeacherWorkflow]
    wait_time = between(1, 5)


# ── Event hooks ────────────────────────────────────────────────────────────────

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("==> Load test started")
    print("    Target: 50 concurrent teachers")
    print("    Performance targets:")
    print("      /search/       < 50 ms")
    print("      /health        < 100 ms")
    print("      /generations/  < 500 ms (submit, not full pipeline)")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats
    print("\n==> Load test complete")
    for name, entry in stats.entries.items():
        print(f"    {name[1]:<40} p50={entry.get_response_time_percentile(0.5):.0f}ms"
              f"  p95={entry.get_response_time_percentile(0.95):.0f}ms"
              f"  fails={entry.num_failures}")
