import sensel
import os
from playsound import playsound
from timeit import default_timer
from datetime import datetime, time



exit_requested = False
initialTime = 0
timeElapsed = 0
distanceCovered = 0
nosOn = False
startNosTime = 0

def checkNos():
    #print (startNosTime - timeElapsed)
    if abs((startNosTime - timeElapsed) > 4):
        nosOn = False


def setTimeDistance(time, speed):
    global timeElapsed
    global distanceCovered

    if time > timeElapsed:
        timeElapsed =+ 1
        distanceCovered += speed
        distanceCovered += int(distanceCovered/100000000000)
        if(int(distanceCovered)<=100000):
            print "Distance Covered - {}/100000".format(int(distanceCovered))
            return False
        else:
            print "Distance Covered - 100000/100000"
            print "Congratulations!! You completed in {} seconds\n\n".format(time)
            return True




def setTime():
    global initialTime
    now = datetime.now()
    beginning_of_day = datetime.combine(now.date(), time(0))
    initialTime =  (now - beginning_of_day).seconds


def runSensel():

    global nosOn
    nos = 2
    applyNos = 0
    sensel_device = sensel.SenselDevice()
    global startNosTime

    start = default_timer()

    # do stuff

    duration = default_timer() - start

    if not sensel_device.openConnection():
        print("Unable to open Sensel sensor!")
        exit()

    else:
        print ("It is working")

    # Enable contact sending
    sensel_device.setFrameContentControl(sensel.SENSEL_FRAME_CONTACTS_FLAG)

    # Enable scanning
    sensel_device.startScanning()

    # define car speed
    car_speed = 0;

    # store the force applied
    last_force = 0 ;

    #playsound('carstartgarage.wav')

    while True:

        frame = sensel_device.readFrame()

        if frame:
            (lost_frame_count, forces, labels, contacts) = frame


            if len(contacts) == 0:
                continue

            # validate feet
            if len(contacts) < 6:
                os.system('clear')
                print "Please put your feet on the pad."
                continue

            current_force = 0
            xmin = 500;
            xmax = 0

            for c in contacts:
                #print("Contact ID %d, mm coord: (%f, %f), force=%.3f, "
                #      "major=%f, minor=%f, orientation=%f" %
                #      (c.id, c.x_pos, c.y_pos, c.total_force,
                #      c.major_axis, c.minor_axis, c.orientation))

                current_force += c.total_force
                xmin = min(xmin, c.x_pos)
                xmax = max(xmax, c.x_pos)
                if c.x_pos in range(0, 80):
                    applyNos = 60
                    if nosOn:
                        nosOn = False
                    else:
                        nosOn = True
                        startNosTime = timeElapsed
                    #print timeElapsed

            checkNos()

            #print startNosTime

            mid = xmin + (xmax - xmin)/2

            if nosOn:
                speed = (current_force / 70)+ applyNos

            else:
                speed = (current_force / 70)

            speedbar = ""

            os.system('clear')

            for i in range(0, int(speed)):
                speedbar = speedbar + "=>"

            LeftForce = 0
            RightForce = 0



            for c in contacts:
                if(c.x_pos>=mid):
                    RightForce += c.total_force

                else:
                    LeftForce += c.total_force

            if(abs(RightForce - LeftForce)<=500):
                direction = "Going Straight"

            elif(RightForce>LeftForce):
                direction = "Going Right"

            else:
                direction = "Going Left"


            print speedbar + " " + str(int(speed)) + " MPH "
            print "\n" + direction

            #if nosOn:
            #    print "NOS on"
            #else:
            #    print "NOS off"

            now = datetime.now()
            beginning_of_day = datetime.combine(now.date(), time(0))
            timeElapsed = (now - beginning_of_day).seconds - initialTime
            print "Time Elapsed {}".format(timeElapsed)
            if setTimeDistance(timeElapsed, speed):
                break


            #if len(contacts) > 0:
            #    print("****     ")


if __name__ == "__main__":
    setTime()
    runSensel()