import importlib.util
from pathlib import Path
from fastapi.testclient import TestClient

# carrega o main.py do serviço, apesar do hífen no nome da pasta
main_path = Path(__file__).resolve().parents[1] / "main.py"
spec = importlib.util.spec_from_file_location("main", main_path)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

app = main.app
client = TestClient(app)

def test_status_endpoint_ok():
    r = client.get("/status")
    assert r.status_code == 200
    body = r.json()
    # contrato padronizado:
    assert body.get("ok") is True
    assert body.get("service") == "equipamentos"
    assert body.get("status") in {"Operacional", "OK", "ok"}
    assert "version" in body and isinstance(body["version"], str)
    assert "timestamp" in body and isinstance(body["timestamp"], str)


