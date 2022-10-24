import requests


class Exchange:
    URL_API_LATESTS = "https://api.bluelytics.com.ar/v2/latest"

    def __init__(self) -> None:
        self.data = self._req()

    def _req(self) -> dict:
        self.json_data = requests.get(self.URL_API_LATESTS)
        return self.json_data.json()
