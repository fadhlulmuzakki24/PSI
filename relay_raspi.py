import RPi.GPIO as GPIO
from time import sleep

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
pin = 7  # Ganti dengan nomor pin yang ingin Anda kontrol
GPIO.setup(pin, GPIO.OUT)

try:
    while True:
        # Mengatur pin ke HIGH
        GPIO.output(pin, GPIO.HIGH)
        print(f"Relay pada pin {pin} diatur ke HIGH")
        sleep(1)  # Menunggu 1 detik

        # Mengatur pin ke LOW
        GPIO.output(pin, GPIO.LOW)
        print(f"Relay pada pin {pin} diatur ke LOW")
        sleep(1)  # Menunggu 1 detik

except KeyboardInterrupt:
    # Membersihkan pengaturan GPIO saat program dihentikan
    GPIO.cleanup()
    print("\nProgram dihentikan dan GPIO dibersihkan.")