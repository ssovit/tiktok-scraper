import json
import os
import random


DEVICES_DIR = "./devices"
os.makedirs(DEVICES_DIR, exist_ok=True)
def get_random_device():
    device_files = [f for f in os.listdir(DEVICES_DIR) if f.endswith(".json")]
    if not device_files:
        return {"error": "No device files available."}
    device_file=random.choice(device_files)
    with open(os.path.join(DEVICES_DIR, device_file), "r", encoding="utf-8") as file:
        return json.load(file)