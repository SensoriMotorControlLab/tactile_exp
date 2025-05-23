import time
from serial import Serial

TVFU = Serial( port     = '/dev/ttyACM0',
               baudrate = 115200          )

TVFU.write(bytes('M2.', 'utf-8'))
time.sleep(0.01)
TVFU.write(bytes('S123.', 'utf-8'))
time.sleep(0.01)
TVFU.write(bytes('D200.', 'utf-8'))
time.sleep(0.01)
TVFU.write(bytes('G2.', 'utf-8'))
time.sleep(0.01)

