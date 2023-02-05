import RPi.GPIO as GPIO
import time
from threading import Thread


# GPIO to LCD mapping
LCD_RS = 21 # Pi pin
LCD_RW = 26 # Pi pin
LCD_E  = 20 # Pi pin
LCD_D4 = 16 # Pi pin
LCD_D5 = 19 # Pi pin
LCD_D6 = 13 # Pi pin
LCD_D7 = 12 # Pi pin
 
# Device constants
LCD_CHR = True # Character mode
LCD_CMD = False # Command mode
LCD_WIDTH = 16    # Maximum characters per line

LCD_LINE_1 = 0x80 # LCD memory location for 1st line
LCD_LINE_2 = 0xC0 # LCD memory location 2nd line
 
# Timing constants
E_PULSE = 0.00005
E_DELAY = 0.00005

led1pin = 24
led2pin = 22
led3pin = 23
led4pin = 27

button1Pin = 6
button2Pin = 1
button3Pin = 7
button4Pin = 8

    
def main():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    
    GPIO.setmode(GPIO.BCM) # Use BCM GPIO numbers
    GPIO.setup(LCD_E, GPIO.OUT) # Set GPIO's to output mode
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_RW, GPIO.OUT, initial = 0)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    GPIO.setup(led1pin, GPIO.OUT, initial = 0)
    GPIO.setup(led2pin, GPIO.OUT, initial = 0)
    GPIO.setup(led3pin, GPIO.OUT, initial = 0)
    GPIO.setup(led4pin, GPIO.OUT, initial = 0)
    
    GPIO.setup(button1Pin, GPIO.IN)
    GPIO.setup(button2Pin, GPIO.IN)
    GPIO.setup(button3Pin, GPIO.IN)
    GPIO.setup(button4Pin, GPIO.IN)

    GPIO.setup(led1pin, GPIO.OUT, initial = 0)

    GPIO.setup(button1Pin, GPIO.IN)
    
    sost_1 = 0
    
    #wh1 = True

   #while True:
        #lcd_write(0x01, LCD_CMD) # Clear display
            
    if GPIO.input(button1Pin) == True:
        while GPIO.input(button1Pin) == True:
            time.sleep(0.01)
            
        sost_1 = not sost_1
        
        print("init LCD start")
        lcd_init() # Initialize display
        print("init LCD Ok")

        string = "Toggled 1"
        
        lcd_text(string, len(string))
        time.sleep(1)
        
        if sost_1 == 0:
            GPIO.output(led1pin, GPIO.LOW)
        else:
            GPIO.output(led1pin, GPIO.HIGH)
    
    #wh1 = False
    time.sleep(0.2)
    
    lcd_write(0x01, LCD_CMD) # Clear display
    
        #-------------------------------------------------------------#
    #wh1 = True
    #wh2 = True
    
    #while True:
        #lcd_write(0x01, LCD_CMD) # Clear display
            
    if GPIO.input(button2Pin) == True:
        while GPIO.input(button2Pin) == True:
            time.sleep(0.01)
            
        sost_1 = not sost_1
        
        print("init LCD start")
        lcd_init() # Initialize display
        print("init LCD Ok")

        string = "Toggled 2"
        
        lcd_text(string, len(string))
        time.sleep(1)
        
        if sost_1 == 0:
            GPIO.output(led1pin, GPIO.LOW)
        else:
            GPIO.output(led1pin, GPIO.HIGH)
    
    #wh2 = False
    
    time.sleep(0.2)
    
    lcd_write(0x01, LCD_CMD) # Clear display
    #wh2 = True
        #-------------------------------------------------------------#        
        
        
                
def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)



 
def lcd_init():
    # Initialise display
    lcd_write(0x33, LCD_CMD) # Initialize
    lcd_write(0x32, LCD_CMD) # Set to 4-bit mode
    lcd_write(0x06, LCD_CMD) # Cursor move direction
    lcd_write(0x0C, LCD_CMD) # Turn cursor off
    lcd_write(0x06, LCD_CMD) # 2 line display
    lcd_write(0x01, LCD_CMD) # Clear display
    time.sleep(0.0005) # Delay to allow commands to process


def lcd_write(bits, mode):
    GPIO.output(LCD_RS, mode) # RS

    # High bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    
    if bits & 0x10 == 0x10:
        GPIO.output(LCD_D4, True)
    if bits & 0x20 == 0x20:
        GPIO.output(LCD_D5, True)
    if bits & 0x40 == 0x40:
        GPIO.output(LCD_D6, True)
    if bits & 0x80 == 0x80:
        GPIO.output(LCD_D7, True)
 
    # Toggle 'Enable' pin
    lcd_toggle_enable()
 
    # Low bits
    GPIO.output(LCD_D4, False)
    GPIO.output(LCD_D5, False)
    GPIO.output(LCD_D6, False)
    GPIO.output(LCD_D7, False)
    
    if bits & 0x01 == 0x01:
        GPIO.output(LCD_D4, True)
    if bits & 0x02 == 0x02:
        GPIO.output(LCD_D5, True)
    if bits & 0x04 == 0x04:
        GPIO.output(LCD_D6, True)
    if bits & 0x08 == 0x08:
        GPIO.output(LCD_D7, True)
  
    # Toggle 'Enable' pin
    lcd_toggle_enable()


def lcd_text(message, line):
 # Send text to display
    message = message.ljust(LCD_WIDTH, " ")
    lcd_write(line, LCD_CMD)
    for i in range(LCD_WIDTH):
      lcd_init()
    for i in range(line):
        lcd_write(ord(message[i]), LCD_CHR)
        

try:
    main()
 
except KeyboardInterrupt:
    print("Exit pressed Ctrl+C")
except:
    print("Other Exception")
finally:
    lcd_write(0x01, LCD_CMD)
    lcd_text("End of program", LCD_LINE_1)
    lcd_text("Waiting...", LCD_LINE_2)
    GPIO.cleanup()
    print("End of program")