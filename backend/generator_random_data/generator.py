import json
import time
from datetime import datetime
from random import randint

class RandomGenerator:
    def __init__(self, amount=1):
        self.amount = amount

    def get_data(self, device_id):
        temperature = randint(18, 28)
        return {"id": device_id, "temperature": temperature, "time": datetime.now().strftime("%H:%M:%S-%d:%m:%Y")}
    def write_data_in_file(self, device_id, data):
        file_name = "device#" + str(device_id)
        with open(f"devices/{file_name}.txt", "w") as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
        print(f"Write {file_name}")
