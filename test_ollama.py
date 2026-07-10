import urllib.request
import json
import urllib.error

url = "http://localhost:11434/api/generate"
payload = json.dumps({
    "model": "llama3.2:3b",
    "prompt": "test",
    "stream": False,
    "options": {
        "num_ctx": 2048,
    }
}).encode("utf-8")

req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
try:
    with urllib.request.urlopen(req) as resp:
        print("Success:", resp.status)
        print(resp.read().decode("utf-8"))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    print(e.read().decode("utf-8"))
except Exception as e:
    print("Error:", e)
