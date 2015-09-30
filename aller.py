#!/usr/bin/python
# coding: utf-8
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from array import array
import random
import gps

# Initialize the LCD plate.  Should auto-detect correct I2C bus.  If not,
# pass '0' for early 256 MB Model B boards or '1' for all later versions
lcd = Adafruit_CharLCDPlate()

# Clear display and show greeting, pause 1 sec
lcd.clear()

def startup():
	text = 'Machine starting up...'
	#text = 'a'
	sleep(2)
	i = 0
	for x in text:
    		lcd.message(x)
    		sleep(.2)
    		i += 1
    		if i == 16:
        		lcd.message('\n')
    		if i == 32:
        		i = 0
        		sleep(1)
	lcd.clear()
	sleep(2)
	lcd.message('Waiting for\na command.')
	return

def rint(txt, i):
	lcd.clear()
        lcd.message(txt)


def rotate(str):
	pit = len(str)

	start = 1;
	while True:
		if lcd.buttonPressed(lcd.LEFT):
			break
		elif start == 1:
			start = 0
			for i in range(1,pit+17):
				if lcd.buttonPressed(lcd.LEFT):
					break
				else:
					sleep(.2)
					if i < 16 and i <= pit:
						txt = str[:i].rjust(16, ' ')
						rint(txt, i)
					elif i < 16 and i > pit:
						txt = str.rjust((16-i+pit), ' ')
						txt = txt.ljust(16, ' ')
						rint(txt, i)
					else:
						txt = str[i-16:16].ljust(16, ' ')
						rint(txt, i)
			start = 1

startup()

# ........Suomi24x 15, 16 pit 7 i = 7  16-i 9
# .......Suomi24xx 14, 16 pit 7 i = 8  16-i 8
# ......Suomi24xxx 13, 16 pit 7 i = 9  16-i 7
# .....Suomi24xxxx 12, 16 pit 7 i = 10 16-i 6

# Poll buttons, display message & set backlight accordingly
#btn = ((lcd.LEFT  , 'Red Red Wine'              , lcd.RED),
#       (lcd.UP    , 'Sita sings\nthe blues'     , lcd.BLUE),
#       (lcd.DOWN  , 'I see fields\nof green'    , lcd.GREEN),
#       (lcd.RIGHT , 'Purple mountain\nmajesties', lcd.VIOLET),
#       (lcd.SELECT, ''                          , lcd.ON))

prev = -1

session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    if lcd.buttonPressed(lcd.SELECT):
        countdown = 5
        for y in range(0,countdown):
            lcd.clear()
            lcd.message('Shutting down in\n' + str(countdown-y) + ' seconds')
            sleep(1)
        lcd.clear()
        sleep(5)
	startup()
    if lcd.buttonPressed(lcd.RIGHT):
        lcd.clear()
	col = (('Red' , lcd.RED) , ('Yellow', lcd.YELLOW), ('Green' , lcd.GREEN),
           ('Teal', lcd.TEAL), ('Blue'  , lcd.BLUE)  , ('Violet', lcd.VIOLET), ('Acid', lcd.RED), ('Colors', lcd.YELLOW))
        text = 'moro poro ja joku muu rullaava test text joka ei lopu koskaan'
	i = 0
	while True:
		if lcd.buttonPressed(lcd.LEFT):
			break
		else:
        		for x in text:
				if lcd.buttonPressed(lcd.LEFT):
					break
				else:
               				lcd.message(x)
               				sleep(.1)
             	  			i += 1
               				if i == 16:
                       				lcd.message('\n')
               				if i == 32:
						lcd.clear()
                        			i = 0
                        			sleep(1)
						lcd.backlight(col[random.randint(0,7)][1])

    if lcd.buttonPressed(lcd.UP):
	lcd.clear()
        lcd.message('*** @Duukkis ****\n** in da house **')
        while True:
		if lcd.buttonPressed(lcd.LEFT):
			lcd.clear()
			sleep(3)
			break
		else:
			for g in range(0,5):
				if lcd.buttonPressed(lcd.LEFT):
					break
				else:
	        	        	report = session.next()
        	        	# Wait for a 'TPV' report and display the current time
                		# To see all report data, uncomment the line below
                		# print report
                			if report['class'] == 'TPV':
                        			if hasattr(report, 'lat'):
                                			lcd.clear()
                                			lcd.message('Lat:' + str(report.lat) + '\n' + 'Lon:' + str(report.lon))
                                                        # write location data into local file
							f = open('/home/pi/lsd/location.txt', 'w')
							f.write("lat={}&lng={}".format(report.lat, report.lon));
							f.close()
							sleep(1)
			col = (lcd.RED, lcd.YELLOW, lcd.GREEN, lcd.TEAL, lcd.BLUE, lcd.VIOLET)
			for c in col:
                		lcd.backlight(c)
                		sleep(0.5)
			lcd.clear()
			lcd.message('*** @Duukkis ***\n** in da house **')
			sleep(2)

    if lcd.buttonPressed(lcd.DOWN):
        lcd.clear()
	rotate('Suomi24')


    if lcd.buttonPressed(lcd.LEFT):
	lcd.clear()
	lcd.message('** Aller Party! **!\n**** 2015 ****')
	

lcd.backlight(lcd.OFF)
lcd.clear()

