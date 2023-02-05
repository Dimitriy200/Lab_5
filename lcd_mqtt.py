#!/usr/bin/python

# Pinout of the LCD:
# 1 : GND
# 2 : 5V power
# 3 : Display contrast - Connect to middle pin potentiometer 
# 4 : RS (Register Select)
# 5 : R/W (Read Write) - Ground this pin (important)
# 6 : Enable or Strobe
# 7 : Data Bit 0 - data pin 0, 1, 2, 3 are not used
# 8 : Data Bit 1 - 
# 9 : Data Bit 2 - 
# 10: Data Bit 3 - 
# 11: Data Bit 4
# 12: Data Bit 5
# 13: Data Bit 6
# 14: Data Bit 7
# 15: LCD Backlight +5V
# 16: LCD Backlight GND

import RPi.GPIO as GPIO
import time
from threading import Thread
import random
from paho.mqtt import client as mqtt_client

broker = 'broker.hivemq.com'
topic = "Alex_MQTT"
client_id = f'python-mqtt-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        string = msg.payload.decode()
        lcd_text(string, len(string))
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message

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

# Define main program code
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


    print("init LCD start")
    lcd_init() # Initialize display
    print("init LCD Ok")
    
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
    
    while True:
        time.sleep(1)
   
    # End of main program code
 
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
  
def lcd_toggle_enable():
    time.sleep(0.0005)
    GPIO.output(LCD_E, True)
    time.sleep(0.0005)
    GPIO.output(LCD_E, False)
    time.sleep(0.0005)
 
def lcd_text(message, line):
 # Send text to display
    message = message.ljust(LCD_WIDTH, " ")
    #lcd_write(line, LCD_CMD)
    #for i in range(LCD_WIDTH):
    lcd_init()
    for i in range(line):
        lcd_write(ord(message[i]), LCD_CHR)

#Begin program
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
