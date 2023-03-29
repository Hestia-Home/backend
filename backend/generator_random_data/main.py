import time
import os

from generator import RandomGenerator
from random import randint

if __name__ == "__main__":
    amount = randint(5, 10)
    amount = 2

    try:
        while True:
            delay = randint(5, 10)
            delay = 3
            random_generator = RandomGenerator()
            data = random_generator.get_data(randint(1, amount))
            random_generator.write_data_in_file((randint(1, amount)), data)
            print(os.listdir("./devices/"))
            time.sleep(delay)
    except KeyboardInterrupt:
        for file_name in os.listdir("./devices/"):
            os.remove("./devices/" + file_name)

