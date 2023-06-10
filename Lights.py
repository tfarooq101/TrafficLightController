"""
# Lights.py
# implementation of different types of lights
# both digitally controlled (on/off)
# or PWM-controlled (dimming) to set brightness
# Author: Arijit Sengupta
"""

import utime
from machine import Pin, PWM
import _thread
MAX = 65535

baton = _thread.allocate_lock()

class Light:
    """
    The Light base class - just an LED controlled by a digital IO
    Pin. Save the pin in an instance variable
    """
    
    def __init__(self, pin, name="Unnamed"):
        """
        Light constructor - save the pin and set it to OUTPUT mode
        pin is the NUMBER of the pin that the LED is connected to. So
        if connecting to GP21, pass the value 21 to pin        
        name is an optional name of the light
        """
            
        print(f"Light: constructor")
        self._name = name
        self._pin = pin
        self._blinking = False
        self._led = Pin(self._pin, Pin.OUT)  # We need this to use the IO functions

    def on(self):
        """ on: Turn the light on """
        
        print(f"Light: turning on {self._name} light at pin {self._pin}")
        self._led.value(1)

    def off(self):
        """ off: turn the light off """
        
        print(f"Light: turning off {self._name} light at pin {self._pin}")
        self._led.value(0)

    def flip(self):
        """ flip: turn off if it was on, on if it was off """
        
        print(f"Light: Toggling {self._name} light at pin {self._pin}")
        self._led.toggle()
        

class DimLight(Light):
    """
    The Dimmable Light subclass - will have the standard on off methods
    and in addition will have the ability to set brightness
    """

    def __init__(self, pin, name="Unnamed"):
        """ Dimmable light constructor """

        print("Dimmable light constructor")
        super().__init__(pin, name)
        self._pwm = PWM(self._led)  # Create an instance of PWM object (pulse-width modulation)
        self._pwm.freq(100000)   # set frequency to 100 khz

    def on(self):
        """ Turn on - full brightness max is 255 """
        
        print(f"Dimlight: turn Light {self._name} on (full brightness)")
        self.setBrightness(MAX)

    def off(self):
        """  Turn off - set brightness to 0 """

        print(f"Dimlight - turn Light {self._name} off (brightness 0)")
        self.setBrightness(0)

    def setBrightness(self, brightness):
        """ Set brightness to a specific level 0-255 """

        print(f"Dimlight: setting Light {self._name} brightness to {brightness}")
        if (brightness == MAX):
            self._pwm.duty_u16(MAX)
        else:
            self._pwm.duty_u16(brightness * brightness)

    def upDown(self):
        """
        # Do a quick demo of going up and down full brightness levels
        # Here it is better to use ChangeDutyCycle
        """
        
        print(f"Dimlight: do an up-down demo on Light {self._name}")
        dc = 0
        for i in range (0, 25):
            dc += 10
            self.setBrightness(dc)
            utime.sleep(100)

        for i in range (0, 25):
            dc -= 10
            self.setBrightness(dc)
            utime.sleep(100)