import urllib3
import json


class TeamsWebhookException(Exception):
    pass


class TeamsProvider:
    def __init__(self, webhook_url, http_timeout=60):
        self.http = urllib3.PoolManager()
        self.payload = {}
        self.webhook_url = webhook_url
        self.http_timeout = http_timeout

    def text(self, text_messsage):
        self.payload["text"] = text_messsage
        return self

    def send(self):
        headers = {"Content-Type": "application/json"}
        request = self.http.request(
            'POST',
            f'{self.webhook_url}',
            body=json.dumps(self.payload).encode('utf-8'),
            headers=headers,
            timeout=self.http_timeout
        )

        if request.status == 200 or request.status == 202:
            return True
        else:
            raise TeamsWebhookException(request.reason)
