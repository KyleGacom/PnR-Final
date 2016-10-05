# STUDENTS SHOULD NOT EDIT THIS FILE. IT WILL MAKE UPDATING MORE DIFFICULT

from gopigo import *
import time


##########################################################
#################### PIGO PARENT CLASS
#### (students will make their own class & inherit this)

class Pigo(object):
    MIDPOINT = 77
    STOP_DIST = 20
    scan = [None] * 180

    def __init__(self):
        # this makes sure the parent handler doesn't take over student's
        if __name__ == "__main__":
            print('-----------------------')
            print('------- PARENT --------')
            print('-----------------------')
            # let's use an event-driven model, make a handler of sorts to listen for "events"
            while True:
                self.stop()
                self.handler()

    ########################################
    #### FUNCTIONS REPLACED IN CHILD CHILD
    #Parent's handler is replaced by child's
    def handler(self):
        menu = {"1": ("Navigate forward", self.nav),
                "2": ("Rotate", self.rotate),
                "3": ("Dance", self.dance),
                "4": ("Calibrate servo", self.calibrate),
                "5": ("Forward", self.encF),
                "q": ("Quit", quit)
                }
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])

        ans = input("Your selection: ")
        menu.get(ans, [None, error])[1]()


    def nav(self):
        print("Parent nav")
        while True:
            choice = self.choosePath()
            if choice == "fwd":
                self.encF(18)
                while self.isClear():
                    self.encF(18)
            elif choice == "right":
                self.encR(6)
            elif choice == "left":
                self.encL(6)
            else:
                print("Can't find a path ahead.")
                break

    ##DANCING IS FOR THE CHILD CLASS
    def dance(self):
        print('Parent dance is lame.')
        for x in range(self.MIDPOINT-20, self.MIDPOINT+20, 5):
            servo(x)
            time.sleep(.1)
        self.encB(5)
        self.encR(5)
        self.encL(5)
        self.encF(5)
        for x in range(self.MIDPOINT-20, self.MIDPOINT+20, 10):
            servo(x)
            time.sleep(.1)



    ########################################
    ##### FUNCTIONS NOT INTENDED TO BE OVERWRITTEN
    def encF(self, enc):
        print('Moving '+str((enc/18))+' rotation(s) forward')
        enc_tgt(1, 1, enc)
        fwd()
        time.sleep((enc/18)*1.8)
        stop()

    def encR(self, enc):
        print('Moving '+str((enc/18))+' rotation(s) right')
        enc_tgt(1, 1, enc)
        right_rot()
        time.sleep((enc/18)*1.8)
        stop()

    def encL(self, enc):
        print('Moving '+str((enc/18))+' rotation(s) left')
        enc_tgt(1, 1, enc)
        left_rot()
        time.sleep((enc/18)*1.8)
        stop()

    def encB(self, enc):
        print('Moving '+str((enc/18))+ ' rotations(s) backwards')
        enc_tgt(1, 1, enc)
        bwd()
        time.sleep((enc/18)*1.8)
        stop()

    #HELP STUDENTS LEARN HOW TO PORTION ENCODE VALUES
    def rotate(self):
        #initial encoder value = 1 wheel rotation
        enc = 18
        while True:
            select = input('Right, left or encode? (r/l/e): ')
            if select == 'r':
                self.encR(enc)
            elif select == 'l':
                self.encL(enc)
            elif select == 'e':
                enc = int(input('New encode value: '))
            else:
                break

    ##DUMP ALL VALUES IN THE SCAN ARRAY
    def flushScan(self):
        self.scan = [None]*180

    #SEARCH 120 DEGREES COUNTING BY 2's
    def wideScan(self):
        #dump all values
        self.flushScan()
        for x in range(self.MIDPOINT-60, self.MIDPOINT+60, +2):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            #double check the distance
            scan2 = us_dist(15)
            #if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                #take another scan and average the three together
                scan1 = (scan1+scan2+scan3)/3
            self.scan[x] = scan1
            print("Degree: "+str(x)+", distance: "+str(scan1))
            time.sleep(.01)

    def isClear(self) -> bool:
        for x in range((self.MIDPOINT - 15), (self.MIDPOINT + 15), 5):
            servo(x)
            time.sleep(.1)
            scan1 = us_dist(15)
            time.sleep(.1)
            # double check the distance
            scan2 = us_dist(15)
            time.sleep(.1)
            # if I found a different distance the second time....
            if abs(scan1 - scan2) > 2:
                scan3 = us_dist(15)
                time.sleep(.1)
                # take another scan and average the three together
                scan1 = (scan1 + scan2 + scan3) / 3
            self.scan[x] = scan1
            print("Degree: " + str(x) + ", distance: " + str(scan1))
            if scan1 < self.STOP_DIST:
                print("Doesn't look clear to me")
                return False
        return True

    #DECIDE WHICH WAY TO TURN
    def choosePath(self) -> str:
        print('Considering options...')
        if self.isClear():
            return "fwd"
        else:
            self.wideScan()
        avgRight = 0
        avgLeft = 0
        for x in range(self.MIDPOINT-60, self.MIDPOINT):
            if self.scan[x]:
                avgRight += self.scan[x]
        avgRight /= 60
        print('The average dist on the right is '+str(avgRight)+'cm')
        for x in range(self.MIDPOINT, self.MIDPOINT+60):
            if self.scan[x]:
                avgLeft += self.scan[x]
        avgLeft /= 60
        print('The average dist on the left is ' + str(avgLeft) + 'cm')
        if avgRight > avgLeft:
            return "right"
        else:
            return "left"

    def stop(self):
        print('All stop.')
        for x in range(3):
            stop()
        servo(self.MIDPOINT)
        time.sleep(0.05)
        disable_servo()

    def calibrate(self):
        print("Calibrating...")
        servo(self.MIDPOINT)
        response = input("Am I looking straight ahead? (y/n): ")
        if response == 'n':
            while True:
                response = input("Turn right, left, or am I done? (r/l/d): ")
                if response == "r":
                    self.MIDPOINT += 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                elif response == "l":
                    self.MIDPOINT -= 1
                    print("Midpoint: " + str(self.MIDPOINT))
                    servo(self.MIDPOINT)
                    time.sleep(.01)
                else:
                    print("Midpoint now saved to: " + str(self.MIDPOINT))
                    break


########################
#### STATIC FUNCTIONS

def error():
    print('Error in input')


def quit():
    raise SystemExit


p = Pigo()