from netmiko import ConnectHandler
import csv
import os
from datetime import datetime
import logging

# Create required directories
os.makedirs("logs", exist_ok=True)
os.makedirs("backups", exist_ok=True)

# Configure logging
logging.basicConfig(
    filename="logs/backup.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def create_device_backup_dir(device_name):
    path = os.path.join("backups", device_name)
    os.makedirs(path, exist_ok=True)
    return path

def backup_device(device):
    try:
        connection = ConnectHandler(
            device_type=device["device_type"],
            host=device["ip"],
            username=device["username"],
            password=device["password"]
        )

        running_config = connection.send_command("show running-config")
        connection.disconnect()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        device_dir = create_device_backup_dir(device["device_name"])
        filename = f"{device['device_name']}_{timestamp}.txt"

        with open(os.path.join(device_dir, filename), "w") as file:
            file.write(running_config)

        logging.info(f"Backup successful for {device['device_name']}")

    except Exception as e:
        logging.error(f"Backup failed for {device['device_name']} - {str(e)}")

def main():
    with open("devices.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for device in reader:
            backup_device(device)

if __name__ == "__main__":
    main()
