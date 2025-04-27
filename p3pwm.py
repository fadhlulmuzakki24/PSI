import RPi.GPIO as GPIO
import time
import csv

# Konfigurasi GPIO untuk pembacaan PWM dari MH-Z19
PWM_PIN = 18  # Sesuaikan dengan pin GPIO yang digunakan

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.IN)

def read_co2_pwm(duration=1.004):
    """Membaca data CO2 dari sensor MH-Z19 melalui sinyal PWM"""
    start_time = time.time()
    high_time = 0
    low_time = 0

    while (time.time() - start_time) < duration:
        if GPIO.input(PWM_PIN) == GPIO.LOW:
            low_start = time.time()
            while GPIO.input(PWM_PIN) == GPIO.LOW:
                pass
            low_time += time.time() - low_start
        if GPIO.input(PWM_PIN) == GPIO.HIGH:
            high_start = time.time()
            while GPIO.input(PWM_PIN) == GPIO.HIGH:
                pass
            high_time += time.time() - high_start

    co2_ppm = 2000 * ((high_time - 0.002) / (high_time + low_time - 0.004))  # Konversi ke ppm (sesuaikan sesuai datasheet)
    return round(co2_ppm)

# Path lengkap untuk menyimpan CSV
csv_filename = "/home/tfc3/Downloads/co2_data.csv"

# Membuka file CSV sekali saja dan menulis header jika belum ada
with open(csv_filename, mode='a', newline='') as file:
    writer = csv.writer(file)
    file.seek(0, 2)  # Pindah ke akhir file
    if file.tell() == 0:  # Jika file kosong, tambahkan header
        writer.writerow(["Timestamp", "CO2 (ppm)"])

try:
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)

        while True:
            co2_concentration = read_co2_pwm()
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            if co2_concentration is not None:
                print(f"{timestamp} - CO2: {co2_concentration} ppm")

                # Simpan data ke CSV
                writer.writerow([timestamp, co2_concentration])
                file.flush()  # Pastikan data langsung tersimpan
            else:
                print("Gagal membaca data dari sensor.")

            time.sleep(0.5)  # Delay 0.5 detik sebelum membaca ulang

except KeyboardInterrupt:
    print("\nPengukuran dihentikan.")
finally:
    GPIO.cleanup()