import minimalmodbus
import serial
import time
import csv  # Library untuk menulis ke file CSV
from contextlib import closing

DEVICE_ADDRESS = 0x01
BAUD_RATE = 9600
TIMEOUT = 1
PORT = '/dev/ttyUSB0'

def read_pzem_data():
    # Initialize the connection to the PZEM device
    instrument = minimalmodbus.Instrument(PORT, DEVICE_ADDRESS)
    instrument.serial.baudrate = 9600
    instrument.serial.bytesize = 8
    instrument.serial.parity = serial.PARITY_NONE
    instrument.serial.stopbits = 2
    instrument.serial.timeout = 1

    # Membuka file CSV untuk menyimpan data
    with open('pzem_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        # Menulis header ke file CSV
        writer.writerow(['Voltage (V)', 'Current (A)', 'Power (W)', 'Energy (Wh)'])

        try:
            while True:
                # Read measurement data
                voltage = instrument.read_register(0x0000, number_of_decimals=2, functioncode=4)
                current = instrument.read_register(0x0001, number_of_decimals=2, functioncode=4)
                power_low = instrument.read_register(0x0002, functioncode=4)
                power_high = instrument.read_register(0x0003, functioncode=4)
                power = (power_high << 16) + power_low
                energy_low = instrument.read_register(0x0004, functioncode=4)
                energy_high = instrument.read_register(0x0005, functioncode=4)
                energy = (energy_high << 16) + energy_low

                # Print data to console
                print(f"Voltage: {voltage} V")
                print(f"Current: {current} A")
                print(f"Power: {power * 0.1} W")
                print(f"Energy: {energy} Wh")

                # Menulis data ke file CSV
                writer.writerow([voltage, current, power * 0.1, energy])

                # Delay sebelum pembacaan berikutnya
                time.sleep(1)

        except minimalmodbus.IllegalRequestError as e:
            print(f"Error: {e}")

        except KeyboardInterrupt:
            print("\nProgram dihentikan oleh pengguna.")

        finally:
            instrument.serial.close()

if __name__ == "__main__":
    read_pzem_data()