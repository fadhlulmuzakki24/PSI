import time
import Adafruit_DHT
import smbus2
import RPi.GPIO as GPIO

# Kelas untuk SHT20
class SHT20:
    def __init__(self, bus=1, address=0x40):
        self.bus = smbus2.SMBus(bus)
        self.address = address

    def read_temperature(self):
        self.bus.write_byte(self.address, 0xF3)
        time.sleep(0.1)
        data = self.bus.read_i2c_block_data(self.address, 0, 2)
        raw_temperature = (data[0] << 8) + data[1]
        temperature = -46.85 + (175.72 * raw_temperature / 65536.0)
        return temperature

    def read_humidity(self):
        self.bus.write_byte(self.address, 0xF5)
        time.sleep(0.1)
        data = self.bus.read_i2c_block_data(self.address, 0, 2)
        raw_humidity = (data[0] << 8) + data[1]
        humidity = -6.0 + (125.0 * raw_humidity / 65536.0)
        return humidity

# Konfigurasi pin dan sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17  # Pin GPIO untuk DHT22
SHT20_SENSOR = SHT20()  # Inisialisasi SHT20
MAX6675_CLK = 18  # Pin GPIO untuk CLK MAX6675
MAX6675_CS = 23   # Pin GPIO untuk CS MAX6675
MAX6675_DO = 24   # Pin GPIO untuk DO MAX6675

# Inisialisasi GPIO untuk MAX6675
GPIO.setmode(GPIO.BCM)
GPIO.setup(MAX6675_CLK, GPIO.OUT)
GPIO.setup(MAX6675_CS, GPIO.OUT)
GPIO.setup(MAX6675_DO, GPIO.IN)

def read_max6675():
    GPIO.output(MAX6675_CS, GPIO.LOW)
    time.sleep(0.002)

    value = 0
    for i in range(16):
        GPIO.output(MAX6675_CLK, GPIO.HIGH)
        time.sleep(0.001)
        value <<= 1
        if GPIO.input(MAX6675_DO):
            value |= 1
        GPIO.output(MAX6675_CLK, GPIO.LOW)
        time.sleep(0.001)

    GPIO.output(MAX6675_CS, GPIO.HIGH)

    # Proses data
    if value & 0x4:  # Periksa bit kesalahan
        return None
    return (value >> 3) * 0.25  # Konversi ke Celsius

def read_sensors():
    try:
        # Membaca data dari DHT22
        humidity, temperature_dht22 = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature_dht22 is not None:
            print(f"DHT22 - Suhu: {temperature_dht22:.2f}°C, Kelembaban: {humidity:.2f}%")
        else:
            print("DHT22 - Gagal membaca data")

        # Membaca data dari SHT20
        temperature_sht20 = SHT20_SENSOR.read_temperature()
        humidity_sht20 = SHT20_SENSOR.read_humidity()
        print(f"SHT20 - Suhu: {temperature_sht20:.2f}°C, Kelembaban: {humidity:.2f}%")

        # Membaca data dari MAX6675
        temperature_max6675 = read_max6675()
        if temperature_max6675 is not None:
            print(f"MAX6675 - Suhu: {temperature_max6675:.2f}°C")
        else:
            print("MAX6675 - Gagal membaca data")

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    while True:
        read_sensors()
        time.sleep(2)  # Tunggu 2 detik sebelum membaca ulang