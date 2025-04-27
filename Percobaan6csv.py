import minimalmodbus
import serial
import time
import csv
import os
from datetime import datetime
from contextlib import closing

DEVICE_ADDRESS = 0x01
BAUD_RATE = 9600
TIMEOUT = 1
PORT = '/dev/ttyUSB0'
CSV_FILE = "pzem004t_data.csv"

def read_pzem_data():
    # Initialize the connection to the PZEM device
    instrument = minimalmodbus.Instrument(PORT, DEVICE_ADDRESS)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 1
    instrument.serial.timeout = 1
    
    try:
        # Read measurement data
        voltage = instrument.read_register(0x0000, number_of_decimals=1, functioncode=4)
        currentlow = instrument.read_register(0x0001, functioncode=4)
        currenthigh = instrument.read_register(0x0002, functioncode=4)
        current = (currenthigh << 16) + currentlow
        power_low = instrument.read_register(0x0003, functioncode=4)
        power_high = instrument.read_register(0x0004, functioncode=4)
        power = (power_high << 16) + power_low
        energy_low = instrument.read_register(0x0005, functioncode=4)
        energy_high = instrument.read_register(0x0006, functioncode=4)
        energy = (energy_high << 16) + energy_low
        
        # Menampilkan data
        print(f"Voltage: {voltage} V")
        print(f"Current: {current * 0.001} A")
        print(f"Power: {power * 0.1} W")
        print(f"Energy: {energy} Wh")
        
        # Simpan ke CSV
        save_to_csv(voltage, current * 0.001, power * 0.1, energy)
        
    except minimalmodbus.IllegalRequestError as e:
        print(f"Error: {e}")
    
    finally:
        time.sleep(1)
        instrument.serial.close()

def save_to_csv(voltage, current, power, energy):
    file_exists = os.path.isfile(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Timestamp", "Voltage (V)", "Current (A)", "Power (W)", "Energy (Wh)"])
        writer.writerow([
            datetime.now().strftime("%H:%M:%S"),
            voltage, 
            current, 
            power, 
            energy
        ])

if __name__ == "__main__":
    read_pzem_data()
