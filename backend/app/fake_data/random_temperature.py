# from random import randint, uniform
# import asyncio
# import json
#
#
# def get_random_temperature_data():
#     rooms = ["Спальня", "Гостинная", "Кухня", "Спальня #2", "Коридор"]
#     device_id = randint(1, 5)
#     temperature = randint(20, 28)
#     data = {
#         "room_name": rooms[randint(0, len(rooms)-1)],
#         "device_id": device_id,
#         "temperature": temperature
#     }
#     # data = json.dumps(data, indent=4, ensure_ascii=False)
#     return data