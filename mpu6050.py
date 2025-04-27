import smbus
import time

# Alamat I2C untuk MPU6050
MPU6050_ADDR = 0x68

# Register pada MPU6050
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Inisialisasi I2C
bus = smbus.SMBus(1)  # Menggunakan I2C-1 pada Raspberry Pi

# Fungsi untuk membaca data 16-bit dari register
def read_raw_data(addr):
    # Membaca data tinggi dan rendah
    high = bus.read_byte_data(MPU6050_ADDR, addr)
    low = bus.read_byte_data(MPU6050_ADDR, addr + 1)
    # Menggabungkan data tinggi dan rendah
    value = (high << 8) | low
    # Mengonversi ke nilai signed (jika diperlukan)
    if value > 32768:
        value -= 65536
    return value

# Inisialisasi MPU6050
def init_mpu6050():
    # Bangunkan MPU6050 dari mode sleep
    bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# Fungsi utama untuk membaca data akselerometer dan giroskop
def read_mpu6050():
    # Membaca data akselerometer
    accel_x = read_raw_data(ACCEL_XOUT_H)
    accel_y = read_raw_data(ACCEL_XOUT_H + 2)
    accel_z = read_raw_data(ACCEL_XOUT_H + 4)

    # Membaca data giroskop
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_XOUT_H + 2)
    gyro_z = read_raw_data(GYRO_XOUT_H + 4)

    # Mengonversi data ke satuan fisik
    Ax = accel_x / 16384.0  # Akselerasi dalam g
    Ay = accel_y / 16384.0
    Az = accel_z / 16384.0

    Gx = gyro_x / 131.0  # Kecepatan sudut dalam derajat/detik
    Gy = gyro_y / 131.0
    Gz = gyro_z / 131.0

    return Ax, Ay, Az, Gx, Gy, Gz

# Program utama
try:
    init_mpu6050()
    print("MPU6050 siap. Membaca data...")

    while True:
        Ax, Ay, Az, Gx, Gy, Gz = read_mpu6050()
        print(f"Akselerasi: Ax={Ax:.2f}g, Ay={Ay:.2f}g, Az={Az:.2f}g")
        print(f"Giroskop: Gx={Gx:.2f}°/s, Gy={Gy:.2f}°/s, Gz={Gz:.2f}°/s")
        print("")
        time.sleep(1)

except KeyboardInterrupt:
    print("Program dihentikan.")