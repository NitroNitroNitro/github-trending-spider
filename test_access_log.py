from fastapi import FastAPI
from fastapi.testclient import TestClient
from access_log import AccessLogMiddleware, _stats

app = FastAPI()
app.add_middleware(AccessLogMiddleware)

@app.get("/test")
def test_endpoint():
    return {"status": "ok"}

client = TestClient(app)

def test_access_log():
    resp = client.get("/test", headers={"X-Forwarded-For": "1.2.3.4\r\nInject: True"})
    assert resp.status_code == 200
    print(_stats)

if __name__ == "__main__":
    test_access_log()
