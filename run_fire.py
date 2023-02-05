import RPi.GPIO as GPIO
import time
from threading import Thread

'''led1pin = 24
led2pin = 22
led3pin = 23
led4pin = 27'''

list_leds = [24, 22, 23, 27]

button1Pin = 6

last_state = False


def run():
    global last_state
    while True:
        if last_state == False:
            
            for i in list_leds:
                GPIO.output(i, GPIO.LOW)
            
            last_led = 3;
            cur_led = 0;

            while True:
                GPIO.output(list_leds[cur_led], GPIO.HIGH)
                GPIO.output(list_leds[last_led], GPIO.LOW)
                cur_led += 1
                if cur_led > 3:
                    cur_led = 0

                last_led += 1
                if last_led > 3:
                    last_led = 0

                time.sleep(0.2)
                if last_state != False:
                    break
                
        else:
            for i in list_leds:
                GPIO.output(i, GPIO.LOW)
            
            last_led = 0;
            cur_led = 3;

            while True:
                GPIO.output(list_leds[cur_led], GPIO.HIGH)
                GPIO.output(list_leds[last_led], GPIO.LOW)
                cur_led -= 1
                if cur_led < 0:
                    cur_led = 3

                last_led -= 1
                if last_led < 0:
                    last_led = 3

                time.sleep(0.2)
                if last_state != True:
                    break



runThread = Thread(target=run, args=())



def main():
    
    global last_state

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
    GPIO.cleanup()

    GPIO.setup(list_leds[0], GPIO.OUT, initial = 0)
    GPIO.setup(list_leds[1], GPIO.OUT, initial = 0)
    GPIO.setup(list_leds[2], GPIO.OUT, initial = 0)
    GPIO.setup(list_leds[3], GPIO.OUT, initial = 0)

    GPIO.setup(button1Pin, GPIO.IN)
    
    last_state = GPIO.input(button1Pin)
    
    runThread.start()
    
    while True:
        
        if GPIO.input(button1Pin) == True:
            while GPIO.input(button1Pin) == True:
                time.sleep(0.01)
                
            last_state = not last_state
            
        time.sleep(0.2)
          

try:
    main()
 
except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except:
    print("Other Exception")
finally:
    print("End of program")
