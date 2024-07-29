import time

import requests


def get_ngrok_url(timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get("http://ngrok:4040/api/tunnels")
            if response.status_code == 200:
                data = response.json()
                public_url = data.get("tunnels", [{}])[0].get("public_url")
                if public_url:
                    return public_url
        except requests.exceptions.ConnectionError:
            print("Waiting for ngrok to start...")
        time.sleep(2)
    raise Exception("Ngrok did not start in time.")
