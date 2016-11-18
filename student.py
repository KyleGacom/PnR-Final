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
    RIGHT_SPEED = 105
    LEFT_SPEED = 104
    TIME_PER_DEGREE = 0.00733333333
    turn_track = 0


    # CONSTRUCTOR
    def __init__(self):
        print("Piggy has be instantiated!")
        # this method makes sure Piggy is looking forward
        # self.calibrate()
        # let's use an event-driven model, make a handler of sorts to listen for "events"
        self.setSpeed(self.LEFT_SPEED, self.RIGHT_SPEED)
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
                "5": ("Cruise", self.cruise),
                "q": ("Quit", quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        #
        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()

    def widerScan(self):
        # dump all values
        self.flushScan()
        for x in range(self.MIDPOINT - 60, self.MIDPOINT + 60, +10):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            time.sleep(.01)

    def choosePath2(self) -> str:
        print('Considering options...')
        if self.isClear():
            return "fwd"
        else:
            self.widerScan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT - 60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is ' + str(avgRight) + 'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT + 60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    def cruise(self):
        print('------------------------')
        print(" is it clear in front? ")
        print('------------------------')
        #made a front clear which only scans the front
        clear = self.isClear()
        print(clear)
        print('------------------------')
        print("------- Moving ---------")
        print('------------------------')
        if clear:
            fwd()
        while True:
            #once its no longer clear it stops and checks which way to go
            if us_dist(15) < self.STOP_DIST:
                print('------------------------')
                print("--------- Stop ---------")
                print('------------------------')
                self.stop()
                self.pathChooser()
                time.sleep(.05)

    def pathChooser(self):
        answer = self.choosePath2()
        # if left is more clear it goes left other wise it turns right
        if answer == "left":
            self.turnL(90)
        elif answer == "right":
            self.turnR(90)

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
    #Other code for TurnR and L
        #adjusting the tracker so we know how many degrees away our exit is
        #self.turn_track += deg
        #print("The exit is " + str(self.turn_track) + " degrees away.")
        #self.setSpeed(self.LEFT_SPEED,self.RIGHT_SPEED)
        #Turns
        #right_rot()
        #time.sleep(deg * self.TIME_PER_DEGREE)
        #self.stop
        #sets speed to normal
        #self.setSpeed(self.LEFT_SPEED,self.RIGHT_SPEED)


    #new turn methods more precise than encR and L
    def turnR(self, deg):
        #new instance
        # TIME_PER_DEGREE - the answer to todays email =  0.00733333333
        print("Let's turn" +str(deg)+ " degrees right")
        print("that means i turn for"+str(deg*self.TIME_PER_DEGREE)+ " seconds")

        right_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)


    def turnL(self, deg):
        # new instance
        # TIME_PER_DEGREE - the answer to todays email =  0.00733333333
        print("Let's turn" + str(deg) + " degrees right")
        print("that means i turn for" + str(deg * self.TIME_PER_DEGREE) + " seconds")

        left_rot()
        time.sleep(deg * self.TIME_PER_DEGREE)


    def setSpeed(self, left, right):
        print("Left speed: " +str(left))
        print("Right speed: " + str(right))
        set_left_speed(left)
        set_right_speed(right)
        time.sleep(.05)



    # AUTONOMOUS DRIVING
    def nav(self):
        print("Piggy nav")
        #check if its clear
        while True:
            while self.isClear():
                #if clear moves forward
                self.encF(7)
            #checks which way is clear
            answer = self.choosePath()
            if answer == "left":
                self.encL(3)
            elif answer == "right":
                self.encR(3)







####################################################
############### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


####################################################
######## THE ENTIRE APP IS THIS ONE LINE....
g = GoPiggy()
