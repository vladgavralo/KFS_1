import pytest
from app.services.calculator import calculate_cost
from config import TARIFFS  

# Тест 1 - коректний розрахунок вартості
def test_calculate_cost():
    total, day, night = calculate_cost(100, 50)
    expected_total = 100 * TARIFFS["day_rate"] + 50 * TARIFFS["night_rate"]
    expected_day = 100 * TARIFFS["day_rate"]
    expected_night = 50 * TARIFFS["night_rate"]

    assert total == pytest.approx(expected_total, abs=0.1)
    assert day == pytest.approx(expected_day, abs=0.1)
    assert night == pytest.approx(expected_night, abs=0.1)

# Тест 2 - нульове споживання
def test_calculate_zero_cost():
    total, day, night = calculate_cost(0, 0)
    assert total == 0
    assert day == 0
    assert night == 0

# Тест 3 - від'ємні значення (очікуємо помилку)
def test_calculate_negative_cost():
    with pytest.raises(ValueError):
        calculate_cost(-10, 50)

# Тест 4 - перевірка округлення
def test_calculate_rounding():
    total, day, night = calculate_cost(5.678, 3.456)
    expected_day = round(5.678 * TARIFFS["day_rate"], 2)
    expected_night = round(3.456 * TARIFFS["night_rate"], 2)
    expected_total = round(expected_day + expected_night, 2)

    assert day == pytest.approx(expected_day, abs=0.1)
    assert night == pytest.approx(expected_night, abs=0.1)
    assert total == pytest.approx(expected_total, abs=0.1)
