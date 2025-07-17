import importlib.util
import sys
from pathlib import Path

# Dynamically load app.py
app_path = Path(__file__).resolve().parent.parent / "app.py"
spec = importlib.util.spec_from_file_location("app", app_path)
app_module = importlib.util.module_from_spec(spec)
sys.modules["app"] = app_module
spec.loader.exec_module(app_module)

app = app_module.app  # Get the Flask app instance


def test_homepage():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200
