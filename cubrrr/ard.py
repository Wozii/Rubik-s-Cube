import serial
import time

ard = serial.Serial(port='COM4', baudrate=9600, timeout=.1)


def write_read(x):
    ard.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = ard.readline()
    return data

while True:

    steps = input("Enter steps: ")
    value = write_read(steps)

    print("input: ", value.decode("utf-8"))
    print("steps", ard.readline().decode("utf-8"))
    print("motor", ard.readline().decode("utf-8"))