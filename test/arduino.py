import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 9600)
while True:
    if ser.readable():
        val = input('start(1) / stop(0) : ')
        if val == '1':
            val = val.encode('utf-8')
            ser.write(val)
            print('START')
            time.sleep(0.5)

        elif val == '0':
            val = val.encode('utf-8')
            ser.write(val)
            print('STOP')
            time.sleep(0.5)