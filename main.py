import time
from TrafficLightController import *
time.sleep(0.1) # Wait for USB to become ready

print("Hello, Pi Pico!")

tlc = TrafficLightController()
tlc.run()

