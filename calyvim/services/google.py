import httpx

from calyvim.models.connected_account import ConnectedAccount


class GoogleAPI:
    def __init__(self, token):
        self._token = token
        self.client = httpx.Client(
            base_url="https://www.googleapis.com",
            headers={"Authorization": f"Bearer {self._token}"},
        )

    """
    calenderId ---> For most use cases calenderId, is basically the email address
    """
