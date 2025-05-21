from locust import HttpUser, between, task
import random
import string

def random_task_text():
    return "".join(random.choices(string.ascii_letters + string.digits, k=10))

class TodoUser(HttpUser):
    wait_time = between(1, 3)  # isteğe yarım–3 s bekle

    @task(2)
    def get_todos(self):
        self.client.get("/get")

    @task(1)
    def add_todo(self):
        payload = {"task": random_task_text()}
        self.client.post("/add", json=payload)

    @task(1)
    def toggle_todo(self):
        # önce rastgele bir ID alın
        resp = self.client.get("/get")
        todos = resp.json()
        if todos:
            todo = random.choice(todos)
            self.client.put(f"/edit/{todo['_id']}")

    @task(1)
    def update_todo(self):
        resp = self.client.get("/get")
        todos = resp.json()
        if todos:
            todo = random.choice(todos)
            payload = {"task": random_task_text()}
            self.client.put(f"/update/{todo['_id']}", json=payload)

    @task(1)
    def delete_todo(self):
        resp = self.client.get("/get")
        todos = resp.json()
        if todos:
            todo = random.choice(todos)
            self.client.delete(f"/delete/{todo['_id']}")

