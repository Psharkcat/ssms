import psutil
import time
import os
import sys
import select

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=0.5)
    
    # RAM Usage
    memory = psutil.virtual_memory()
    total_ram = memory.total / 1e9  # convert to GB
    used_ram = memory.used / 1e9    # convert to GB
    ram_percent = memory.percent

    # temperature Informations
    try:
        sensors = psutil.sensors_temperatures()
        temperatures = {}
        if sensors:
            for name, entries in sensors.items():
                for entry in entries:
                    temperatures[entry.label or 'Unnamed'] = entry.current
        else:
            temperatures = {"No sensors": "N/A"}
    except AttributeError:
        temperatures = {"Error": "No temperature data available"}
    
    os.system('cls' if os.name == 'nt' else 'clear')

    # displaying the info
    print(f"\nCPU Usage: {cpu_usage}%")
    print(f"Total RAM: {total_ram:.2f} GB")
    print(f"Used RAM: {used_ram:.2f} GB ({ram_percent}%)")
    print("Temperatures:")
    for label, temp in temperatures.items():
        print(f"  {label}: {temp}°C")

def wait_for_input():
    print("Press Enter to stop the updates.")
    while True:
        # Check if Enter is pressed (non-blocking)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            input()  # To consume the input and exit
            return True
        time.sleep(0.5)
        get_system_info()

try:
    wait_for_input()
except KeyboardInterrupt:
    print("\nExiting...")
