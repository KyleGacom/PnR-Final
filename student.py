import pigo
import time
import random
from gopigo import *

'''
This class INHERITS your teacher's Pigo class. That means Mr. A can continue to
improve the parent class and it won't overwrite your work.
'''


class GoPiggy(pigo.Pigo):
    # CUSTOM INSTANCE VARIABLES GO HERE. You get the empty self.scan array from Pigo
    # You may want to add a variable to store your default speed
    MIDPOINT = 96
    STOP_DIST = 20

    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        # self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        while True:
            self.stop()
            self.handler()

    ##### HANDLE IT
    def handler(self):
        ## This is a DICTIONARY, it's a list with custom index values
        # You may change the menu if you'd like
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    def superClear(self):
        set_speed(150)
        #check in front
        if not self.isClear():
            print('------------------------')
            print("Front is not clear")
            print('------------------------')
            return False
        #turn 90 right and print "checking right"
        self.encR(6)
        if not self.isClear():
            print('------------------------')
            print("Problem to the right")
            print('------------------------')
            return False
        #turn 90 right and print "checking behind"
        self.encR(6)
        if not self.isClear():
            print('------------------------')
            print("Behind is not clear")
            print('------------------------')
            return False
        #turn right 90 and check left
        self.encR(6)
        if not self.isClear():
            print('------------------------')
            print("Left is not clear")
            print('------------------------')
            return False
        #Turns to front and begins dance
        self.encR(6)
        return True

    # A SIMPLE DANCE ALGORITHM
    def dance(self):
        print("Piggy dance")
        ##### WRITE YOUR FIRST PROJECT HERE
        print('-----------------------')
        print('safe to dance?')
        print('-----------------------')
        #Starting speed
        x = 100
        #Tells robot to run super clear unless the speed is above 190
        while self.superClear() and x <= 190:
            #DANCE PIGGY DANCE
            self.encR(18)
            print('speed is set to:' + str(x))
            servo(20)
            set_speed(x)
            self.encB(5)
            self.encR(2)
            self.encL(2)
            self.encF(5)
            servo(120)
            self.encR(15)
            servo(20)
            self.encL(15)
            servo(120)
            self.encR(15)
            servo(20)
            self.encL(15)
            servo(120)
            self.encB(5)
            self.encL(2)
            self.encR(2)
            self.encF(5)
            servo(96)
            time.sleep(.1)
            #Adds 30 speed after it does the dance and dances again
            x += 30




    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        ##### WRITE YOUR FINAL PROJECT HERE
        #check if its clear
        while self.isClear():
            #move forward
            self.encF(10)
        #if false check turn right 90 and check again(Facing right)
        else:
            self.encR(5)
            while self.isClear():
                self.encF(10)
            # if not clear turns again and scans (facing backwards)
            else:
                self.encR(5)
                while self.isClear():
                    self.encF(10)
            #if not clear turns again and scans (facing left)
                else:
                    self.encR(5)
                    while self.isClear():
                        self.encF(10)
                        #should be clear by now for the robot to go






####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
