from locust import HttpUser, between, task
import random
import string
import json

def random_task_text():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))

class TodoUser(HttpUser):
    wait_time = between(1, 3)  # isteğe yarım–3 s bekle

    @task(2)
    def get_todos(self):
        self.client.get("/get", name="get")

    @task(1)
    def add_todo(self):
        payload = {"task": random_task_text()}
        self.client.post("/add", json=payload, name="add")

    def _safe_get_todos(self):
        """
        /get endpoint'inden JSON parse ederken hatayı yakalar,
        başarısızsa boş liste döner.
        """
        resp = self.client.get("/get", name="get")
        try:
            return resp.json() or []
        except ValueError:
            return []

    @task(1)
    def toggle_todo(self):
        todos = self._safe_get_todos()
        if not todos:
            return
        todo = random.choice(todos)
        self.client.put(f"/edit/{todo['_id']}", name="toggle")

    @task(1)
    def update_todo(self):
        todos = self._safe_get_todos()
        if not todos:
            return
        todo = random.choice(todos)
        payload = {"task": random_task_text()}
        self.client.put(f"/update/{todo['_id']}", json=payload, name="update")

    @task(1)
    def delete_todo(self):
        todos = self._safe_get_todos()
        if not todos:
            return
        todo = random.choice(todos)
        self.client.delete(f"/delete/{todo['_id']}", name="delete")

