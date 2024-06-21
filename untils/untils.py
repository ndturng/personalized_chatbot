import time

import requests


def wait_for_server(url, timeout=300):
    """
    Wait for the server to start by periodically checking the URL.
    """
    start_time = time.time()
    while True:
        time.sleep(5)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except ConnectionError:
            return False
        if time.time() - start_time > timeout:
            raise TimeoutError("Server did not start within the timeout period")

