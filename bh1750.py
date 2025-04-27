# Micropython BH1750 ambient light sensor driver: https://github.com/PinkInk/upylib/tree/master/bh1750

from time import sleep, strftime
from smbus import SMBus  # Gunakan SMBus untuk komunikasi I2C
import csv  # Library untuk menulis ke file CSV

class BH1750():
    """Micropython BH1750 ambient light sensor driver."""

    PWR_OFF = 0x00
    PWR_ON = 0x01
    RESET = 0x07

    # modes
    CONT_LOWRES = 0x13
    CONT_HIRES_1 = 0x10
    CONT_HIRES_2 = 0x11
    ONCE_HIRES_1 = 0x20
    ONCE_HIRES_2 = 0x21
    ONCE_LOWRES = 0x23

    # default addr=0x23 if addr pin floating or pulled to ground
    # addr=0x5c if addr pin pulled high
    def __init__(self, bus, addr=0x23):
        self.bus = bus
        self.addr = addr
        self.off()
        self.reset()

    def off(self):
        """Turn sensor off."""
        self.set_mode(self.PWR_OFF)

    def on(self):
        """Turn sensor on."""
        self.set_mode(self.PWR_ON)

    def reset(self):
        """Reset sensor, turn on first if required."""
        self.on()
        self.set_mode(self.RESET)

    def set_mode(self, mode):
        """Set sensor mode."""
        self.mode = mode
        self.bus.write_byte(self.addr, self.mode)

    def luminance(self, mode):
        """Sample luminance (in lux), using specified sensor mode."""
        # continuous modes
        if mode & 0x10 and mode != self.mode:
            self.set_mode(mode)
        # one shot modes
        if mode & 0x20:
            self.set_mode(mode)
        # earlier measurements return previous reading
        sleep(0.024 if mode in (0x13, 0x23) else 0.18)  # Mengganti sleep_ms dengan sleep (dalam detik)
        data = self.bus.read_i2c_block_data(self.addr, 0, 2)
        factor = 2.0 if mode in (0x11, 0x21) else 1.0
        return (data[0] << 8 | data[1]) / (1.2 * factor)

# Main program
if __name__ == "__main__":

    # Inisialisasi I2C bus dan BH1750
    i2c_bus = SMBus(1)  # Gunakan I2C bus 1 (default untuk Raspberry Pi)
    sensor = BH1750(i2c_bus)

    # Nama file CSV
    csv_file = "bh1750_data.csv"

    try:
        # Membuka file CSV untuk menyimpan data
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Menulis header ke file CSV
            writer.writerow(["Timestamp", "Luminance (lux)"])

            print("Mulai membaca data dari sensor BH1750...")
            while True:
                # Membaca luminansi dalam mode resolusi tinggi (CONT_HIRES_1)
                lux = sensor.luminance(BH1750.CONT_HIRES_1)
                timestamp = strftime("%H:%M:%S")  # Mendapatkan waktu saat ini (jam:menit:detik)
                print(f"{timestamp} - Luminansi: {lux:.2f} lux")

                # Menyimpan data ke file CSV
                writer.writerow([timestamp, lux])

                # Reset sensor setelah pembacaan
                sensor.reset()

                sleep(1)  # Tunggu 1 detik sebelum pembacaan berikutnya

    except KeyboardInterrupt:
        print("\nProgram dihentikan oleh pengguna.")

    finally:
        print("Mematikan sensor...")
        sensor.off()