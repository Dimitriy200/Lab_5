import RPi.GPIO as GPIO
import time

led1pin = 24

button1Pin = 6

def main():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
    GPIO.cleanup()

    GPIO.setup(led1pin, GPIO.OUT, initial = 0)

    GPIO.setup(button1Pin, GPIO.IN)
    
    sost_1 = 0

    while True:
            
        if GPIO.input(button1Pin) == True:
            while GPIO.input(button1Pin) == True:
                time.sleep(0.01)
                
            sost_1 = not sost_1
            
            if sost_1 == 0:
                GPIO.output(led1pin, GPIO.LOW)
            else:
                GPIO.output(led1pin, GPIO.HIGH)
        
        time.sleep(0.2)
                

try:
    main()
 
except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except:
    print("Other Exception")
finally:
    print("End of program")

