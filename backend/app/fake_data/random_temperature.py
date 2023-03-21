from random import randint, uniform
import asyncio
import json


def get_random_temperature_data():
    rooms = ["Спальня", "Гостинная", "Кухня", "Спальня #2", "Коридор"]
    sensor_id = randint(1, 100)
    temperature = randint(20, 28)
    data = {
        "room_name": rooms[randint(0, len(rooms)-1)],
        "sensor_id": sensor_id,
        "temperature": temperature
    }
    # data = json.dumps(data, indent=4, ensure_ascii=False)
    return data