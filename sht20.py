import time
import smbus2
import csv
from datetime import datetime

# Alamat I2C untuk SHT20
SHT20_ADDR = 0x40
CMD_MEASURE_TEMP = 0xF3
CMD_MEASURE_HUMID = 0xF5

# Fungsi untuk membaca suhu dari SHT20
def read_temperature(bus):
    bus.write_byte(SHT20_ADDR, CMD_MEASURE_TEMP)
    time.sleep(0.1)
    data0 = bus.read_byte(SHT20_ADDR)
    data1 = bus.read_byte(SHT20_ADDR)
    temperature = ((data0 << 8) + data1) * 175.72 / 65536.0 - 46.85
    return temperature

# Fungsi untuk membaca kelembaban dari SHT20
def read_humidity(bus):
    bus.write_byte(SHT20_ADDR, CMD_MEASURE_HUMID)
    time.sleep(0.1)
    data0 = bus.read_byte(SHT20_ADDR)
    data1 = bus.read_byte(SHT20_ADDR)
    humidity = ((data0 << 8) + data1) * 125.0 / 65536.0 - 6.0
    return humidity

# Konfigurasi I2C
bus = smbus2.SMBus(1)

# Nama file CSV
csv_filename = "sensor_data.csv"

# Fungsi untuk membuat atau menambahkan data ke file CSV
def save_to_csv(timestamp, temperature, humidity):
    # Periksa apakah file sudah ada, jika tidak, buat dengan header
    try:
        with open(csv_filename, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Temperature (°C)", "Humidity (%)"])
    except FileExistsError:
        pass  # Jika file sudah ada, lanjutkan tanpa membuat ulang
    
    # Tambahkan data baru ke file
    with open(csv_filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, f"{temperature:.2f}", f"{humidity:.2f}"])

# Loop utama untuk membaca data sensor dan menyimpannya ke CSV
def main():
    try:
        while True:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            temperature = read_temperature(bus)
            humidity = read_humidity(bus)
            
            print(f"[{timestamp}] Temperature: {temperature:.2f} °C, Humidity: {humidity:.2f} %")

            # Simpan ke CSV
            save_to_csv(timestamp, temperature, humidity)
            
            time.sleep(1)  # Tunggu sebelum pembacaan berikutnya
    except KeyboardInterrupt:
        print("\nTerminating program...")

if _name_ == "_main_":
    main()