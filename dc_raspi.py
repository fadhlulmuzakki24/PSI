import RPi.GPIO as GPIO
import spidev
import time

# Konfigurasi pin
PWM_PIN = 18  # Pin PWM untuk motor

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)

# Inisialisasi PWM
pwm = GPIO.PWM(PWM_PIN, 1000)  # Frekuensi PWM 1 kHz
pwm.start(0)

try:
    while True:
        user_input = input("Masukkan nilai PWM (0-100): ")
        try:
            pwm_value = float(user_input)
            if 0 <= pwm_value <= 100:
                print(f"Mengatur PWM ke: {pwm_value:.2f}%")
                pwm.ChangeDutyCycle(pwm_value)
            else:
                print("Harap masukkan nilai antara 0 dan 100.")
        except ValueError:
            print("Input tidak valid. Harap masukkan angka.")

except KeyboardInterrupt:
    print("Program dihentikan.")
    pwm.stop()
    GPIO.cleanup()
