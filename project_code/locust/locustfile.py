from locust import HttpUser, task, between
from requests.auth import HTTPBasicAuth
import random

class User(HttpUser):
    REMOTE_URL = "/remote.php/dav/files"
    CREATE_USER_URL = "/ocs/v1.php/cloud/users"
    wait_time = between(1, 3)  # Simulate wait time between 1 and 3 seconds

    def on_start(self):
        self.username = "locustuser" + str(random.randint(1, 100000))
        self.password = self.username
        headers = {
            "OCS-APIRequest": "true",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        payload = {
            "userid": self.username,
            "password": self.password
    
        }
        self.client.post(self.CREATE_USER_URL, data=payload, headers=headers, auth=HTTPBasicAuth("admin", "password"))
       
    @task(8)
    def get_files(self):
        self.client.request("PROPFIND", f"{self.REMOTE_URL}/{self.username}/", auth=(self.username, self.password), name="get_files")

    @task(5)
    def download_file(self):
        self.client.get(f"{self.REMOTE_URL}/{self.username}/Readme.md", auth=(self.username, self.password), name="download_file")

    @task(8)
    def upload_kb(self):
        with open("/locust/1kb", "rb") as file:
            self.client.put(
                f"{self.REMOTE_URL}/{self.username}/myfile_kb_{random.randint(1, 100000)}",
                data=file,
                auth=(self.username, self.password),
                name=f"up_kb"
            )

    @task(5)
    def upload_mb(self):
        with open("/locust/1mb", "rb") as file:
            self.client.put(
                f"{self.REMOTE_URL}/{self.username}/myfile_mb_{random.randint(1, 100000)}",
                data=file,
                auth=(self.username, self.password),
                name=f"up_mb"
            )
    
    @task(2)
    def upload_gb(self):
        with open("/locust/1gb", "rb") as file:
            self.client.put(
                f"{self.REMOTE_URL}/{self.username}/myfile_gb_{random.randint(1, 100000)}",
                data=file,
                auth=(self.username, self.password),
                name=f"up_gb"
            )