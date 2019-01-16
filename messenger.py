# ------------------------------------------------------------------------------
# Control Nexus Mecanum 4WD robot using PlayStation 3 controller - Python3
# Bill Griffith - G-Tech SF - 2019
# WARNING: EXPERIMENTAL! unintended movements may occur.
# Mapped Controls: 
# Left Stick Up/Down = Forward/Reverse
# Right Stick Left/Right = Slide Left/Right
# X Button + Left Stick Left/Right = Rotate Left/Right
# Square Button = Stop Motors
# ------------------------------------------------------------------------------
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
import PyCmdMessenger, time, pygame

#Speed Multiplier - Set between 200-1000+
speedMult = 250

# Initialize an ArduinoBoard instance.
arduino = PyCmdMessenger.ArduinoBoard("/dev/ttyUSB0",baud_rate=9600)

# List of command names (and formats for their associated arguments). These must
# be in the same order as in the sketch.
commands = [["turn_left","s"],
            ["turn_right","s"],
            ["rotate_right","s"],
            ["rotate_left","s"],
            ["forward","s"],
            ["backward","s"],
            ["StopMotors","s"],
            ["error","s"]]
# Initialize the messenger
c = PyCmdMessenger.CmdMessenger(arduino,commands)

# Function to control multi-directional movement
def moveRobot ( params ):
    global c
    direction = params[0]
    speed = params[1]
    c.send (direction, speed)
    print ("MOVE: ",direction, speed)
    return
# params = ["forward","100"]
# moveRobot(params)

# Initialize pygame for Joystick
pygame.init()

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

if pygame.joystick.get_count() == 0:
    print("No joysticks found")
    done = True
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("Initialized %s" % (joystick.get_name()))
    print("Number of buttons %d. Number of axis %d, Number of hats %d" %
          (joystick.get_numbuttons(), joystick.get_numaxes(),
           joystick.get_numhats()))

left_trigger_initialized = False
right_trigger_initialized = False
lastBSpeed = int(0)
lastFSpeed = int(0)
lastTLSpeed = int(0)
lastTRSpeed = int(0)
lastRTRSpeed = int(0)
lastRTLSpeed = int(0)


# -------- Main Program Loop -----------
while not done:
    # EVENT PROCESSING STEP

    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

    #X Button + LEFT STICK,RIGHT-LEFT rotate_right rotate_left
    if joystick.get_button(14) == 1:
        print("X Button - Hold to Rotate")
         
        if abs(joystick.get_axis(0)) > 0.05 or abs(joystick.get_axis(0)) > 0.05:
            print("Left stick %f, %f" % (joystick.get_axis(0),
                                         joystick.get_axis(0)))
                                     
        #CONVERT JOYSTICK DATA INTO USABLE VALUES
        RTspeed = joystick.get_axis(0)*speedMult
        RTspeed = round(RTspeed,0)
        RTspeed = int(RTspeed)

        #ROTATE ROBOT LEFT
        if  RTspeed < -100 and RTspeed != lastRTLSpeed:
            #RTspeed = abs(RTspeed)
            print ("ROTATE LEFT:", RTspeed, " last:", lastRTLSpeed)
            c.send("rotate_left",abs(RTspeed))
            lastRTLSpeed = RTspeed
        elif -60 >= RTspeed >= 0:
            print ("ROTATE LEFT ZERO",RTspeed," last:", lastRTLSpeed)
            c.send("turn_left",0)
            lastRTLSpeed = RTspeed
            
        #ROTATE ROBOT RIGHT
        if RTspeed > 100 and RTspeed != lastRTRSpeed:
            #RTspeed = abs(RTspeed)
            print ("ROTATE RIGHT:", RTspeed, " last:", lastRTRSpeed)
            c.send("rotate_right",abs(RTspeed))
            lastRTRSpeed = RTspeed 
        elif 0 <= RTspeed <= 60:
            print ("ROTATE RIGHT ZERO",RTspeed," last:", lastRTRSpeed)
            c.send("turn_right",0)
            lastRTRSpeed = RTspeed

    #SQUARE BUTTON ON PS3 CONTROLLER - STOP MOTORS
    if joystick.get_button(15) == 1:
        print("SQUARE BUTTON - STOP")
        c.send("StopMotors","1")

    #LEFT STICK, UP/DOWN backward forward
    if abs(joystick.get_axis(0)) > 0.05 or abs(joystick.get_axis(1)) > 0.05:
        print("Left stick %f, %f" % (joystick.get_axis(0),
                                     joystick.get_axis(1)))
                                     
        #CONVERT JOYSTICK DATA INTO USABLE VALUES
        FBspeed = joystick.get_axis(1)*speedMult
        FBspeed = round(FBspeed,0)
        FBspeed = int(FBspeed)

        #MOVE ROBOT BACKWARD
        if FBspeed <= -100 and FBspeed != lastFSpeed:
            FBspeed = abs(FBspeed)
            print ("BACKWARD:", FBspeed, " last:", lastBSpeed)
            c.send("backward",FBspeed)
            lastBSpeed = FBspeed
        elif (-60 <= FBspeed <= 0) and joystick.get_button(14) == 0:
            print ("BACKWARD ZERO",FBspeed," last:", lastBSpeed)
            c.send("backward",0)
            lastBSpeed = FBspeed
            
        #MOVE ROBOT FORWARD
        if FBspeed >= 100 and FBspeed != lastBSpeed:
            FBspeed = abs(FBspeed)
            print ("FORWARD:", FBspeed, " last:", lastFSpeed)
            c.send("forward",FBspeed)
            lastFSpeed = FBspeed
        elif 0 <= FBspeed <= 60 and joystick.get_button(14) == 0:
            print ("FORWARD ZERO",FBspeed," last:", lastFSpeed)
            c.send("forward",0)
            lastFSpeed = FBspeed
                        
    #RIGHT STICK, LEFT/RIGHT turn_left turn_right
    if abs(joystick.get_axis(2)) > 0.05 or abs(joystick.get_axis(4)) > 0.05:
        print("Right stick %f, %f" % (joystick.get_axis(3),
                                      joystick.get_axis(4)))
        
        #CONVERT JOYSTICK DATA INTO USABLE VALUES
        LRspeed = joystick.get_axis(2)*speedMult
        LRspeed = round(LRspeed,0)
        LRspeed = int(LRspeed)
        
        #MOVE ROBOT SLIDE RIGHT
        if LRspeed >= 100 and LRspeed != lastTRSpeed:
            LRspeed = abs(LRspeed)
            print ("SLIDE RIGHT",LRspeed," last:", lastTRSpeed)
            c.send("turn_right",LRspeed)
            lastTRSpeed = LRspeed
        elif 0 <= LRspeed <= 60:
            print ("SLIDE RIGHT ZERO",LRspeed," last:", lastTRSpeed)
            c.send("turn_right",0)
            lastTRSpeed = LRspeed
            
        #MOVE ROBOT SLIDE LEFT
        if LRspeed <= -100 and LRspeed != lastTLSpeed:
            LRspeed = abs(LRspeed)
            print ("SLIDE LEFT", LRspeed, " last:", lastTLSpeed)
            c.send("turn_left",LRspeed)
            lastTLSpeed = LRspeed
        elif -60 <= LRspeed <= 0:
            print ("SLIDE LEFT ZERO", LRspeed," last:", lastTLSpeed)
            c.send("turn_left",0)
            lastTLSpeed = LRspeed
            
    # Limit to 20 frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()




