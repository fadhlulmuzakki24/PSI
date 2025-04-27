import time
import glob

class DS18B20:
    def __init__(self):
        # Cari file sensor di direktori 1-Wire
        base_dir = "/sys/bus/w1/devices/"
        device_folder = glob.glob(base_dir + "28*")[0]  # Ambil perangkat pertama dengan ID 28-
        self.device_file = device_folder + "/w1_slave"

    def read_raw_data(self):
        """Membaca data mentah dari sensor"""
        with open(self.device_file, "r") as file:
            return file.readlines()

    def read_temperature(self):
        """Mengambil dan mengonversi data suhu dari sensor"""
        lines = self.read_raw_data()

        # Pastikan data valid (baris pertama harus diakhiri dengan "YES")
        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self.read_raw_data()

        # Ambil data suhu dari baris kedua
        temp_str = lines[1].split("t=")[-1]
        temperature = float(temp_str) / 1000.0  # Konversi ke Celsius
        return temperature

# Loop utama untuk membaca suhu
def main():
    sensor = DS18B20()

    try:
        while True:
            temperature = sensor.read_temperature()
            print(f"Temperature: {temperature:.2f} °C")
            time.sleep(2)  # Tunggu 2 detik sebelum pembacaan berikutnya

    except KeyboardInterrupt:
        print("Terminating program")

if __name__ == "__main__":
    main()
