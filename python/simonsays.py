#########Simon Says#################
####################################
#####Copyright 2013-Alex Stange#####

#This is a game designed for a raspberry pi connected to a circuit using the GPIO pins. 
#The computer will randomly come up with a sequence of Red, Yellow, or Green lights which the user must correctly repeat.
#After each successful completion the sequence grows by 1 in length

from time import sleep, clock, time
import RPi.GPIO as GPIO
import random
import os

red = 21
green = 16
yellow = 20
button1 = 19
button2 = 26
button3 = 13


GPIO.setmode(GPIO.BCM)

def start():			#will run when the program starts
	print "Start"
#		light("R")
#		sleep(.05)
#		light("Y")
#		sleep(.05)
#		light("G")
#		sleep(.05)
#		allOff()
#		sleep(.05)


def lost():				#will run when the user loses
	print "lost"


def light(color):		#function which takes a string: R, Y or G and fires the corresponding GPIO pin and sound file
	GPIO.setup(red, GPIO.OUT) #red
	GPIO.setup(yellow, GPIO.OUT) #yellow
	GPIO.setup(green, GPIO.OUT) #green
	if color == "R":
		GPIO.output(red, GPIO.HIGH)
		os.system('aplay /do/simon/wavs/redSound.wav')
	if color == "Y":
		GPIO.output(yellow, GPIO.HIGH)
		os.system('aplay /do/simon/wavs/yellowSound.wav')
	if color == "G":
		GPIO.output(green, GPIO.HIGH)
		os.system('aplay /do/simon/wavs/greenSound.wav')

		
def allOff():			#turns all GPIO pins to low
	GPIO.setup(red, GPIO.OUT) #red
	GPIO.setup(yellow, GPIO.OUT) #yellow
	GPIO.setup(green, GPIO.OUT) #green
	GPIO.output(red, GPIO.LOW)
	GPIO.output(yellow, GPIO.LOW)
	GPIO.output(green, GPIO.LOW)		


def chosen():			#this function will switch the GPIOs to input mode and return which button is pressed
	
	condition=True
	
	GPIO.setup(button1, GPIO.IN, pull_up_down=GPIO.PUD_UP) #red
	GPIO.setup(button2, GPIO.IN, pull_up_down=GPIO.PUD_UP) #yellow
	GPIO.setup(button3, GPIO.IN, pull_up_down=GPIO.PUD_UP) #green

	while (condition):
		
		red_prev_input_value=True
		red_input_value=GPIO.input(button1)
		
		yellow_prev_input_value=True
		yellow_input_value=GPIO.input(button2)
			
		green_prev_input_value=True
		green_input_value=GPIO.input(button3)
		
		

		if ((red_prev_input_value) and not red_input_value):
			os.system('aplay /do/simon/wavs/redSound.wav')
			return "R"
			red_prev_input_value=red_input_value
			sleep(0.1)
			condition=False
			
		if ((yellow_prev_input_value) and not yellow_input_value):
			os.system('aplay /do/simon/wavs/yellowSound.wav')
			return "Y"
			yellow_prev_input_value=yellow_input_value
			sleep(0.1)
			condition=False
		
		if ((green_prev_input_value) and not green_input_value):
			os.system('aplay /do/simon/wavs/greenSound.wav')
			return "G"
			green_prev_input_value=green_input_value
			sleep(0.1)
			condition=False
			


def showScore(r):			#this function tells the user their score by lighting R for ones, Y for tens, and G for hundreds
	ones = r%10
	tens = (r%100 - r%10)/10
	hundreds = (r - r%100)/100
	
	for x in range(0, hundreds):
		light("G")
		sleep(.1)
		allOff()
		sleep(.1)
		
	for x in range(0, tens):
		light("Y")
		sleep(.1)
		allOff()
		sleep(.1)
	
	for x in range(0, ones):
		light("R")
		sleep(.1)
		allOff()
		sleep(.1)

########THE GAME#############

playing = True
round = 0
sequence = [None]*100
start()

while playing: #this loop is one round of play

	sequence[round] = random.choice(["R","Y","G"])
	
	for x in range(0, (round+1)):
		light(sequence[x])
		#BEEP?
		sleep(.3)
		allOff()
		sleep(.3)
		
	for x in range(0,100):				#the sequence is printed to a command line...don't look at your monitor if you want to play for real!
		if (sequence[x] != None):
			print(sequence[x])
				
	sleep(.2);
	
	i = 0;
	while (i < (round+1)):   #this loop checks user's input sequence and will continue of correct or end if incorrect

		userChoice = chosen()
		print("user: "+userChoice)
		
		if ((userChoice != sequence[i]) and (userChoice != None)):
			print("WRONG")
			os.system('aplay /do/simon/wavs/wrong.wav')
			playing = False
			i=round+1
		else:
			print("Correct")
			sleep(.4)
			i += 1

			
	sleep(1);
	round += 1;
	
sleep(.5)
lost()
os.system('/do/tts/espeak "Your score is "' + str(round))
#showScore(round)

allOff();
GPIO.cleanup()
