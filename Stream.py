import requests


class Stream:
    def __init__(self, token):
        self.s = requests.session()
        self.s.headers.update({
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) StreamlabsDesktop/1.16.7 Chrome/114.0.5735.289 Electron/25.9.3 Safari/537.36",
            "authorization": f"Bearer {token}"
        })

    def search(self, game):
        if not game:
            return []
        url = f"https://streamlabs.com/api/v5/slobs/tiktok/info?category={game}"
        info = self.s.get(url).json()
        info["categories"].append({"full_name": "Other", "game_mask_id": ""})
        return info["categories"]

    def start(self, title, category):
        url = "https://streamlabs.com/api/v5/slobs/tiktok/stream/start"
        files=(
            ('title', (None, title)),
            ('device_platform', (None, 'win32')),
            ('category', (None, category)),
        )
        response = self.s.post(url, files=files).json()
        try:
            self.id = response["id"]
            return response["rtmp"], response["key"]
        except KeyError:
            return None, None

    def end(self):
        url = f"https://streamlabs.com/api/v5/slobs/tiktok/stream/{self.id}/end"
        response = self.s.post(url).json()
        return response["success"]