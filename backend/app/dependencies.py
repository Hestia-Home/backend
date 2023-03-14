from random import randint, uniform


def get_random_data():
    rooms = ["Спальня", "Гостинная", "Кухня", "Спальня #2", "Коридор"]
    sensor_id = randint(1, 100)
    temprature = uniform(25, 25)
    data = {
        "Room name": rooms[randint(0, len(rooms)-1)],
        "sensor_id": sensor_id,
        "Temprature": temprature
    }
    return data
