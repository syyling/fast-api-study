import pytest
from fastapi.testclient import TestClient
from main import app

# 데코레이터
@pytest.fixture
def client():
    return TestClient(app=app)