import requests


class Exchange:
    URL_API_LATESTS = "https://api.bluelytics.com.ar/v2/latest"

    def __init__(self) -> None:
        self.data = self.req()

    def req(self) -> dict:
        return requests.get(self.URL_API_LATESTS).json()
