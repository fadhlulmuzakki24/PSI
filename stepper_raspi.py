import RPi.GPIO as GPIO
import time
 
out1 = 17
out2 = 22
out3 = 23
out4 = 24
 
# careful lowering this, at some point you run into the mechanical limitation of how quick your motor can move

rotation_speed = int(input( "How fast? (1-10) " ))

step_sleep = 1/ (50*rotation_speed) 

print("Step count note:\n"
"1.8 degree each step\n"
"positive for clockwise\n"
"negative for counterclockwise\n"
"200 steps for one full rotation"
)

step_count = int(input( "How many steps? " ))
 
# setting up
GPIO.setmode( GPIO.BCM )
GPIO.setup( out1, GPIO.OUT )
GPIO.setup( out2, GPIO.OUT )
GPIO.setup( out3, GPIO.OUT )
GPIO.setup( out4, GPIO.OUT )
 
# initializing
GPIO.output( out1, GPIO.LOW )
GPIO.output( out2, GPIO.LOW )
GPIO.output( out3, GPIO.LOW )
GPIO.output( out4, GPIO.LOW )
 
 
def cleanup():
    GPIO.output( out1, GPIO.LOW )
    GPIO.output( out2, GPIO.LOW )
    GPIO.output( out3, GPIO.LOW )
    GPIO.output( out4, GPIO.LOW )
    GPIO.cleanup()
 
 
# the meat
try:
    i = 0
    if step_count > 0:
        for i in range(step_count):
            if i%4==0:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
    
            time.sleep( step_sleep )

    elif step_count < 0:
        for i in range(abs(step_count)):
            if i%4==0:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.HIGH )
            elif i%4==1:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.HIGH )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==2:
                GPIO.output( out4, GPIO.LOW )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.HIGH )
                GPIO.output( out1, GPIO.LOW )
            elif i%4==3:
                GPIO.output( out4, GPIO.HIGH )
                GPIO.output( out3, GPIO.LOW )
                GPIO.output( out2, GPIO.LOW )
                GPIO.output( out1, GPIO.LOW )
    
            time.sleep( step_sleep )
 
    else:
        print( "You didn't enter a number of steps to take!" )

except KeyboardInterrupt:
    cleanup()
    exit( 1 )
 
cleanup()
exit( 0 )