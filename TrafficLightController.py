"""
A basic template file for using the Model class in PicoLibrary
This will allow you to implement simple Statemodels with some basic
event-based transitions.

Currently supports only 4 buttons (hardcoded to BTN1 through BTN4)
and a TIMEOUT event for internal tranisitions.

For processing your own events such as sensors, you can implement
those in your run method for transitions based on sensor events.
"""

# Import whatever Library classes you need - Model is obviously needed
import time
import random
from Model import *
from Button import *
from Counters import *
from myclasses import *
from Displays import *
from Lights import *


"""
This is the template Model Runner - you should rename this class to something
that is supported by your class diagram. This should associate with your other
classes, and any PicoLibrary classes. If you are using Buttons, you will implement
buttonPressed and buttonReleased.

To implement the model, you will need to implement 3 methods to support entry actions,
exit actions, and state actions.

This template currently implements a very simple state model that uses a button to
transition from state 0 to state 1 then a 5 second timer to go back to state 0.
"""

class TrafficLightController:

    def __init__(self):
        
        # Instantiate whatever classes from your own model that you need to control
        # Handlers can now be set to None - we will add them to the model and it will
        # do the handling
        self._display = LCDDisplay(sda=20, scl=21, i2cid=0)
        self._button1 = Button(12, "crosswalkbutton1", buttonhandler=None)
        #self._button2 = Button(19, "crosswalkbutton2", buttonhandler=None)
        self._redled1 = Light(0, "Red Light 1")
        self._greenled1 = Light(3, "Green Light 1")
        self._yellowled1 = Light(8, "Yellow Light 1")
        self._redled2 = Light(28, "Red Light 2")
        self._greenled2 = Light(22, "Green Light 2")
        self._yellowled2 = Light(18, "Yellow Light 2")
        self._pir = MotionSensor(28)
        
        
        
        
        # Instantiate a Model. Needs to have the number of states, self as the handler
        # You can also say debug=True to see some of the transitions on the screen
        # Here is a sample for a model with 4 states
        self._model = Model(4, self, debug=True)
        
        # Up to 4 buttons and a timer can be added to the model for use in transitions
        # Buttons must be added in the sequence you want them used. The first button
        # added will respond to BTN1_PRESS and BTN1_RELEASE, for example
        self._model.addButton(self._button1)
        #self._model.addButton(self._button2)
        # add other buttons (up to 3 more) if needed
        
        # Add any timer you have.
        
        
        # Now add all the transitions that are supported by my Model
        # obvously you only have BTN1_PRESS through BTN4_PRESS
        # BTN1_RELEASE through BTN4_RELEASE
        # and TIMEOUT
        
        
        # This method calls all the buttons and the different states that the traffic light goes through
        self._model.addTransition(0, BTN1_PRESS, 1)
        self._model.addTransition(1, BTN1_PRESS, 2)
        self._model.addTransition(2, BTN1_PRESS, 3)
        self._model.addTransition(3, BTN1_PRESS, 0)
        #self._model.addTransition(2, BTN2_PRESS, 3)
        #self._model.addTransition(3, BTN2_PRESS, 0)

        
       
    """
    Create a run() method - you can call it anything you want really, but
    this is what you will need to call from main.py or someplace to start
    the state model.
    """

    def run(self):
        # The run method should simply do any initializations (if needed)
        # and then call the model's run method.
        # You can send a delay as a parameter if you want something other
        # than the default 0.1s. e.g.,  self._model.run(0.25)
        self._model.run()

    """
    stateDo - the method that handles the do/actions for each state
    """
    def stateDo(self, state):
            
        # Now if you want to do different things for each state you can do it:
        if state == 0:
            self._greenled1.on()
            self._display.showText(str("Don't Walk"),0,0)
            self._display.showText(str("Walk"),1,0)
            self._redled2.on()
            #time.sleep(3)
            if self._pir.motionDetected():
                self._model.gotoState(1) 
        elif state == 1:
            # State 2 do/actions
            self._greenled1.off()
            self._yellowled1.on()
            self._redled2.on()
            time.sleep(2)
            self._model.gotoState(2)
        elif state == 2:
            self._yellowled1.off()
            self._redled1.on()
            time.sleep(.5)
            self._redled2.off()
            self._greenled2.on()
            self._display.reset()
            self._display.showText(str("Walk"),0,0)
            self._display.showText(str("Don't Walk"),1,0)
            time.sleep(2)
            self._model.gotoState(3)
        elif state == 3:
            self._greenled2.off()
            self._yellowled2.on()
            time.sleep(3)
            self._yellowled2.off()
            self._display.reset()
            self._model.gotoState(0)
        

       

    """
    stateEntered - is the handler for performing entry/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    """
    def stateEntered(self, state):
        # Again if statements to do whatever entry/actions you need
        if state == 0:
            # entry actions for state 0
            print('State 0 entered')
   
        elif state == 1:
            # entry actions for state 1
            print('State 1 entered')

        elif state == 2:
            # entry actions for state 2
            print('State 2 entered')
        
        elif state == 3:
            # entry actions for state 2
            print('State 3 entered')
            
           
    """
    stateLeft - is the handler for performing exit/actions
    You get the state number of the state that just entered
    Make sure actions here are quick
    
    This is just like stateEntered, perform only exit/actions here
    """

    def stateLeft(self, state):
        if state == 0:
            print('Leaving state 0')
            pass
        elif state == 1:
            print('Leaving state 1')
            pass
        elif state == 2:
            print('Leaving state 2')
            pass
        elif state == 3:
            print('Leaving state 3')
            pass
        

# Test your model. Note that this only runs the template class above
# If you are using a separate main.py or other control script,
# you will run your model from there.
if __name__ == '__main__':
    TrafficLightController().run()