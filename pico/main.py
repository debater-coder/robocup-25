from sys import stdin
from select import poll, POLLIN
from time import sleep
from machine import Pin

poller = poll()
led = Pin(25, Pin.OUT)

led.toggle()
poller.register(stdin, POLLIN)
print("boot")

line = ""
count = 0
while True:
    events = poller.poll(0)
    if events:
        char = stdin.read(1)
        if char == "\n":
            print(line)
            line = ""
        else:
            line += char

    if count > 10000:
        led.toggle()
        count = 0
    count += 1
