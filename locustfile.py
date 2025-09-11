import os
import random
import string
from typing import Any, Dict, Optional

from locust import HttpUser, between, events, task


def _rand_str(min_len: int = 5, max_len: int = 20) -> str:
    length = random.randint(min_len, max_len)
    alphabet = string.ascii_letters + string.digits + " "
    # avoid leading/trailing spaces
    s = "".join(random.choice(alphabet) for _ in range(length)).strip()
    return s or "text"


def _blog_payload() -> Dict[str, str]:
    return {
        "title": _rand_str(5, 32),
        "body": _rand_str(20, 160),
    }


class BlogApiUser(HttpUser):
    """
    Locust user that exercises the blog API.

    How to run locally (examples):
      locust -f simulation.py --headless -u 10 -r 2 -t 1m --host=http://localhost:8080

    You can also set LOCUST_HOST env var instead of passing --host.
    """

    # Give users a small think time between requests
    wait_time = between(0.2, 1.2)

    # Keep a small pool of recently created IDs per user to use for read/update/delete
    recent_ids: list[int]

    def on_start(self) -> None:
        # Optionally set host from env var if not provided via CLI
        env_host = os.getenv("LOCUST_HOST")
        if (
            env_host
            and not getattr(
                self.environment.host, "__bool__", lambda: bool(self.environment.host)
            )()
        ):
            # Locust 2.x keeps host at environment.host; only set if empty
            self.environment.host = env_host

        self.recent_ids = []
        # Warm up by creating one post per user
        self._create_post()

    # --- Helper request wrappers -------------------------------------------------

    def _create_post(self) -> Optional[int]:
        with self.client.post(
            "/v1/blog", json=_blog_payload(), name="POST /blog", catch_response=True
        ) as resp:
            if resp.status_code == 201:
                try:
                    pid = resp.json().get("id")
                except Exception:
                    pid = None
                if isinstance(pid, int):
                    self.recent_ids.append(pid)
                    # keep only the N most recent IDs
                    if len(self.recent_ids) > 20:
                        self.recent_ids.pop(0)
                    resp.success()
                    return pid
                else:
                    resp.failure("No id in response")
            else:
                resp.failure(f"Unexpected status {resp.status_code}")
        return None

    def _get_any_id(self) -> Optional[int]:
        if self.recent_ids:
            return random.choice(self.recent_ids)
        # fallback: try to fetch the first page and grab one id
        with self.client.get(
            "/v1/blog?limit=1", name="GET /blog?page", catch_response=True
        ) as resp:
            if resp.status_code == 200:
                try:
                    items = resp.json().get("items", [])
                    if items:
                        return items[0].get("id")
                except Exception:
                    pass
                resp.success()
            else:
                resp.failure(f"Unexpected status {resp.status_code}")
        return None

    # --- Tasks -------------------------------------------------------------------

    @task(5)
    def list_posts(self) -> None:
        # exercise pagination parameters randomly
        limit = random.choice([5, 10, 20, 50])
        offset = random.choice([0, 0, 0, 10, 20, 50])
        self.client.get(f"/v1/blog?limit={limit}&offset={offset}", name="GET /blog")

    @task(3)
    def create_post(self) -> None:
        self._create_post()

    @task(4)
    def get_post_by_id(self) -> None:
        pid = self._get_any_id()
        if pid is not None:
            self.client.get(f"/v1/blog/{pid}", name="GET /blog/{id}")

    @task(2)
    def patch_post(self) -> None:
        pid = self._get_any_id()
        if pid is not None:
            payload: Dict[str, Any] = {}
            # Randomly update title/body or both
            if random.random() < 0.7:
                payload["title"] = _rand_str(5, 40)
            if random.random() < 0.7:
                payload["body"] = _rand_str(10, 120)
            if not payload:
                payload = {"title": _rand_str(5, 40)}
            self.client.patch(f"/v1/blog/{pid}", json=payload, name="PATCH /blog/{id}")

    @task(1)
    def delete_post(self) -> None:
        # Low weight to avoid rapidly draining DB
        pid = self._get_any_id()
        if pid is not None:
            with self.client.delete(
                f"/v1/blog/{pid}", name="DELETE /blog/{id}", catch_response=True
            ) as resp:
                if resp.status_code in (200, 202, 204, 404):
                    # 404 is acceptable if already deleted by another user
                    resp.success()
                    # best-effort clean local cache
                    try:
                        self.recent_ids.remove(pid)
                    except ValueError:
                        pass
                else:
                    resp.failure(f"Unexpected status {resp.status_code}")


# Optional: record environment info at test start
@events.test_start.add_listener
def on_test_start(environment, **kwargs):  # type: ignore[no-redef]
    env_host = os.getenv("LOCUST_HOST")
    if env_host and not environment.host:
        environment.host = env_host
