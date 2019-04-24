#Set this up as a cron job, rather than an endless loop
import pyowm
import time
import RPi.GPIO as GPIO

owm=pyowm.OWM('0c75491a1f80ff0e5cade3e330ac1017')

def check_soil():
    """check soil moisture, return True if needs watering, return False if it is wet
enough already"""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2,GPIO.IN)
    #test - just read the value every second 10 times
    for a in range 10:
        print(GPIO.input(2))
        time.sleep(1)
    #when reading correctly, this is the real code (wet = high?):
    #if GPIO.input(2):
        #return False
    return True

def check_weather():
    """check weather, return True if it will rain in the next 24 hours, return False if
it will not rain"""
    fc=owm.three_hours_forecast('Morris Plains')
    f=fc.get_forecast()
    x=0
    for weather in f:
        if x<7:
            if weather.get_status()=="Rain":
                return True
            x+=1
    return False

def water_plants():
    """open the bibcock to water for *some* minutes.  Return True if it completed
successfully."""
    print("Watering for "+str(time)+" minutes")
    GPIO.setup(3,GPIO.OUT)
    GPIO.output(3,GPIO.HIGH)
    time.sleep(300)
    GPIO.output(3,GPIO.LOW)
    return True

if check_soil():
    print("Soil is too dry")
    if not check_weather():
        print("No rain in the next day")
        water_time=5
        water_plants()    
GPIO.cleanup()
