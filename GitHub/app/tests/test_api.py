import pytest
from fastapi.testclient import TestClient
from main import app
import random

client = TestClient(app)

# Тест 1 - додавання нового лічильника (унікальний номер)
def test_add_meter():
    random_meter_number = str(random.randint(100000, 999999))  # генеруємо випадковий номер
    response = client.post("/add_meter", json={"meter_number": random_meter_number, "owner_name": "Тестовый Користувач"})
    assert response.status_code == 200
    assert "meter_id" in response.json()

# Тест 2 - додавання дубліката 
def test_add_existing_meter():
    response = client.post("/add_meter", json={"meter_number": "987654", "owner_name": "Клон"})
    assert response.status_code == 400

# Тест 3 - додавання показань
def test_add_reading():
    response = client.post("/add_reading", json={"meter_id": 1, "day_kwh": 120, "night_kwh": 80})
    assert response.status_code == 200
    assert "total_cost" in response.json()

# Тест 4 - додавання показань для неіснуючого лічильника
def test_add_reading_invalid_meter():
    response = client.post("/add_reading", json={"meter_id": 999, "day_kwh": 100, "night_kwh": 50})
    assert response.status_code == 404

# Тест 5 - отримання історії для лічильника
def test_get_history():
    response = client.get("/history", params={"meter_id": 1})
    assert response.status_code == 200

# Тест 6 - отримання історії для неіснуючого лічильника
def test_get_history_invalid_meter():
    response = client.get("/history", params={"meter_id": 999})
    assert response.status_code == 404

# Тест 7 - оновлення тарифів
def test_update_tariffs():
    response = client.put("/update_tariffs", json={"day_rate": 2.00, "night_rate": 1.00})
    assert response.status_code == 200
    assert response.json()["new_tariffs"]["day_rate"] == 2.00
    assert response.json()["new_tariffs"]["night_rate"] == 1.00

# Тест 8 - Експорт історії
def test_export_history():
    response = client.get("/export_history", params={"meter_id": 1})
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

# Тест 9 -  експорт історії для неіснуючого лічильника
def test_export_history_invalid_meter():
    response = client.get("/export_history", params={"meter_id": 999})
    assert response.status_code == 404
