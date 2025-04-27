# Set up libraries and overall settings
import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
from time import sleep   # Imports sleep (aka wait or pause) into the program
GPIO.setmode(GPIO.BOARD) # Sets the pin numbering system to use the physical layout

# Set up pin 11 for PWM
GPIO.setwarnings(False)
GPIO.setup(11,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
p = GPIO.PWM(11, 50)     # Sets up pin 11 as a PWM pin
p.start(0)               # Starts running PWM on the pin and sets it to 0

def angle_to_duty_cycle(angle):
    # Mengonversi sudut (0-180) menjadi duty cycle (2-12)
    return 2 + (angle / 18)

try:
    while True:
        # Meminta input sudut dari pengguna
        angle = float(input("Masukkan sudut (0-180): "))
        
        if 0 <= angle <= 180:
            duty_cycle = angle_to_duty_cycle(angle)
            p.ChangeDutyCycle(duty_cycle)
            sleep(1)  # Menunggu 1 detik untuk memberikan waktu bagi servo untuk bergerak
        else:
            print("Sudut harus antara 0 dan 180 derajat.")

except KeyboardInterrupt:
    # Membersihkan pengaturan GPIO saat program dihentikan
    p.stop()
    GPIO.cleanup()