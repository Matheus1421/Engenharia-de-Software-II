import importlib.util
from fastapi.testclient import TestClient
from pathlib import Path

main_path = Path(__file__).resolve().parents[1] / "main.py"

spec = importlib.util.spec_from_file_location("main", main_path)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

app = main.app
client = TestClient(app)

def test_status_endpoint_ok():
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json().get("ok") is True
