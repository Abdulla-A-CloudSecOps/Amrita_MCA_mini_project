from netmiko import ConnectHandler
import time

switch = {
    "device_type": "cisco_ios",
    "ip": "10.70.80.15",
    "username": "admin",
    "password": "admin"
}

backup_dir = "/home/DEVICE-BACKUPS/Switches_Backups"

try:
    with ConnectHandler(**switch) as connection:
        hostname = connection.send_command("show start | include hostname").strip().split()[-1]
        output = connection.send_command("show start")
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{backup_dir}/{hostname}_{current_time}.txt"
        with open(filename, "w") as f:
            f.write(output)
        print(f"Backup successful! File saved as {filename}")
except Exception as e:
    print(f"Backup failed: {str(e)}")
