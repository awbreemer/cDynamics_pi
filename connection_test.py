import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
    ser.reset_input_buffer()

    while True:
        ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('ascii').rstrip()
        print(line)
        time.sleep(1)