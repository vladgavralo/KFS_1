from config import TARIFFS

def calculate_cost(day_kwh: float, night_kwh: float):
    if day_kwh < 0 or night_kwh < 0:
        raise ValueError("⛔ Показники споживання не можуть бути меншими за 0!")

    
    print(f"DEBUG: TARIFFS = {TARIFFS}")

    
    day_cost = round(day_kwh * TARIFFS["day_rate"], 2)
    night_cost = round(night_kwh * TARIFFS["night_rate"], 2)
    total_cost = round(day_cost + night_cost, 2)


    print(f"DEBUG: day={day_cost}, night={night_cost}, total={total_cost}")

    return total_cost, day_cost, night_cost
