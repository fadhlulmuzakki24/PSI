import time
import os
import glob
import Adafruit_DHT  # Library untuk membaca DHT22
import smbus2  # Library untuk komunikasi I2C dengan SHT20
import spidev  # Library untuk komunikasi SPI dengan MAX6675
import csv  # Untuk menyimpan hasil ke file CSV

# Konfigurasi sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 5  # Pin GPIO untuk DHT22

SHT20_ADDR = 0x40  # Alamat I2C untuk SHT20
CMD_TEMP = 0xE3  # Perintah untuk membaca suhu
CMD_HUM = 0xE5   # Perintah untuk membaca kelembapan

MAX6675_CHANNEL = 0  # Channel SPI untuk MAX6675

# Inisialisasi SPI untuk MAX6675
spi = spidev.SpiDev()
spi.open(0, MAX6675_CHANNEL)
spi.max_speed_hz = 500000

# Inisialisasi DS18B20
os.system('modprobe w1-gpio')  # Memuat modul GPIO 1-Wire
os.system('modprobe w1-therm')  # Memuat modul sensor suhu 1-Wire (DS18B20)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]  # Mencari perangkat DS18B20
device_file = device_folder + '/w1_slave'  # File tempat membaca data

# Fungsi membaca suhu dari SHT20
def read_sht20_temperature():
    try:
        bus = smbus2.SMBus(1)
        bus.write_byte(SHT20_ADDR, CMD_TEMP)  # Perintah baca suhu
        time.sleep(0.1)
        data = bus.read_i2c_block_data(SHT20_ADDR, CMD_TEMP, 2)
        bus.close()
        temp_raw = (data[0] << 8) | data[1]
        temperature = -46.85 + 175.72 * (temp_raw / 65536.0)
        return round(temperature, 2)
    except:
        return None

# Fungsi membaca kelembapan dari SHT20
def read_sht20_humidity():
    try:
        bus = smbus2.SMBus(1)
        bus.write_byte(SHT20_ADDR, CMD_HUM)  # Perintah baca kelembapan
        time.sleep(0.1)
        data = bus.read_i2c_block_data(SHT20_ADDR, CMD_HUM, 2)
        bus.close()
        hum_raw = (data[0] << 8) | data[1]
        humidity = -6.0 + 125.0 * (hum_raw / 65536.0)
        return round(humidity, 2)
    except:
        return None

# Fungsi membaca suhu dari DHT22
def read_dht22():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if temperature is not None and humidity is not None:
        return round(temperature, 2), round(humidity, 2)
    else:
        return None, None

# Fungsi membaca suhu dari DS18B20
def read_ds18b20():
    try:
        with open(device_file, 'r') as f:
            lines = f.readlines()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            with open(device_file, 'r') as f:
                lines = f.readlines()
        temp_string = lines[1][lines[1].find('t=')+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    except Exception:
        return None

# Fungsi membaca suhu dari MAX6675
def read_max6675():
    try:
        raw = spi.xfer2([0, 0])
        value = ((raw[0] << 8) | raw[1]) >> 3
        temperature = value * 0.25  # Konversi ke Celsius
        return round(temperature, 2)
    except:
        return None

# Inisialisasi file CSV untuk menyimpan data
csv_filename = "sensor_readings.csv"
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "DHT22 Temp (°C)", "DHT22 Hum (%)", "DS18B20 Temp (°C)", "MAX6675 Temp (°C)", "SHT20 Temp (°C)", "SHT20 Hum (%)"])

# Loop utama untuk membaca semua sensor setiap 1 detik
try:
    while True:
        timestamp = time.strftime("%H:%M:%S")  # Timestamp jam:menit:detik
        
        # Membaca data dari sensor DHT22
        dht22_temp, dht22_humidity = read_dht22()

        # Membaca data dari sensor SHT20
        sht20_temp = read_sht20_temperature()
        sht20_humidity = read_sht20_humidity()

        # Membaca data dari sensor DS18B20
        ds18b20_temp = read_ds18b20()

        # Membaca data dari sensor MAX6675
        max6675_temp = read_max6675()

        # Cetak hasil pembacaan
        print(f"{timestamp}")
        print(f"DHT22   | Suhu: {dht22_temp}°C | Kelembaban: {dht22_humidity}%" if dht22_temp is not None else "DHT22   | Data tidak terbaca")
        print(f"SHT20   | Suhu: {sht20_temp}°C | Kelembaban: {sht20_humidity}%" if sht20_temp is not None else "SHT20   | Data tidak terbaca")
        print(f"DS18B20 | Suhu: {ds18b20_temp}°C" if ds18b20_temp is not None else "DS18B20 | Data tidak terbaca")
        print(f"MAX6675 | Suhu: {max6675_temp}°C" if max6675_temp is not None else "MAX6675 | Data tidak terbaca")
        print("")

        # Simpan data ke CSV
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, dht22_temp, dht22_humidity, ds18b20_temp, max6675_temp, sht20_temp, sht20_humidity])
        
        time.sleep(1)  # Tunggu 1 detik sebelum membaca ulang

except KeyboardInterrupt:
    print("\nProgram dihentikan.")
