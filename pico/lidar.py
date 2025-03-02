from machine import Pin, UART, Timer
from Makerverse_Motor_2ch import motor
from time import sleep

# constants
HEAD_BYTE = 0xfa
PACKET_SIZE = 22

lidar_uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))
lidar_uart.init(115200, bits=8, parity=None, stop=1)
lidar_motor = motor(6, 7)

while True:
    if lidar_uart.any() > 0:
        print(lidar_uart.read(1))
# # start motor at max speed
# lidar_motor.speed(100)
# sleep(2)
# lidar_motor.speed(50) # slow down for PID's sake
"""
# packet decoding loop
while True:
    # wait until head byte
    while lidar_uart.read(1)[0] != HEAD_BYTE:
        pass

    # fill up packet (- 1 because head byte)
    packet = lidar_uart.read(PACKET_SIZE - 1)

    if HEAD_BYTE in packet:
       print("error: head byte found in packet")
       continue # can't have head byte in packet

    print(f"packet: {packet.hex()}")
"""
