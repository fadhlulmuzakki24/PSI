import minimalmodbus

# Configure the instrument
instrument = minimalmodbus.Instrument('/dev/ttyUSB0', slaveaddress=1)  # Update port
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1

# Read holding registers
try:
    registers = instrument.read_registers(0, 1)  # Start at 0, read 1 registers
    print("Received data:", registers)
except Exception as e:
    print("Error:", e)