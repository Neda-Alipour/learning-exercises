from typing import Any

text: str = "value"
part: int =  90
temp: float = 10.5

class City:
    def __init__(self, name: str, location: float):
        self.name = name
        self.location = location

number: int | float = 13

digits: list[int] = [1, 3, 4]

table_2: tuple[int, ...] = (1, 2, 3, 4)

tehran = City("Tehran", 13213135.0)
city_temp: tuple[City, float] = (tehran, 10.5)

shipment: dict[str, Any] = {
    "id": 1,
    "temp": 10.5,
    "content": "Wooden table",
    "status": "In transit"
}

def root(num: int | float, exp: float | None = .5) -> float:
    return pow(num, exp if exp is not None else .5)

root_5 = root(25)