import RPi.GPIO as GPIO
import time

leds = [40,38,36,37,35,33,31,32,29,11,12,13,15]
score_led = 31 #score indicating led
target_p1 = 15 #player 1 target led
target_p2 = 40 #player 2 target led

b1 = 16
b2 = 18


GPIO.setmode(GPIO.BOARD)

for led in leds:
	GPIO.setup(led,GPIO.OUT)
	GPIO.output(led,GPIO.LOW)

GPIO.setup(b1,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(b2,GPIO.IN, pull_up_down=GPIO.PUD_UP)

p1_score = 0
p2_score = 0

game = False
main_menu = True
game_over = False

def victory(player):
	for i in range(20):
		GPIO.output(player, GPIO.HIGH)
		time.sleep(0.1)
		GPIO.output(player, GPIO.LOW)
		time.sleep(0.1)

def score(loop):

	global score_led

	start = 0

	while start < loop:
		GPIO.output(score_led, GPIO.HIGH)
		time.sleep(0.2)
		GPIO.output(score_led, GPIO.LOW)
		time.sleep(0.2)
		start+=1

def warning():
	pass

def key_press():

	b1_state = GPIO.input(b1)
	b2_state = GPIO.input(b2)

	if b1_state == False and b2_state == False:
		return "multi"

	if b1_state == False:
		return "single_p1"

	if b2_state == False:
		return "single_p2"


def runner(timing):

	global main_menu
	global game
	global game_over
	global p1_score
	global p2_score
	global target_p1
	global target_p2

	for led in leds:

		state = key_press()

		GPIO.output(led,GPIO.HIGH)
		time.sleep(timing)
		GPIO.output(led,GPIO.LOW)

		if main_menu == True:
			if state == "multi":
				main_menu = False
				game = True
				break
		if game == True:
			if  state == "single_p1":
				GPIO.output(led,GPIO.HIGH)
				time.sleep(1.5)
				GPIO.output(led,GPIO.LOW)

				if led == target_p1 and p1_score < 5:
					print(p1_score)
					p1_score+=1
					score(p1_score)

				if p1_score == 5:
					game = False
					game_over = True


			if state == "single_p2":
				GPIO.output(led,GPIO.HIGH)
				time.sleep(1.5)
				GPIO.output(led,GPIO.LOW)

				if led == target_p2 and p2_score < 5:

					p2_score+=1
					score(p2_score)

				if p2_score == 5:
					game = False
					game_over = True

	leds.reverse()


try:
	#global p1_score
	#global p2_score
	while True:

		while main_menu == True:
			runner(0.5)

			#print(b1_state)
			#print(b2_state)


		while game_over == True:
			state = key_press()
			if p1_score == 5:
				victory(target_p2)

			if p2_score ==5:
				victory(target_p1)
			p1_score = 0
			p2_score = 0
			game_over = False
			game = False
			main_menu = True 


		while game == True:
			runner(0.03)

finally:
	#GPIO.setup(15,GPIO.OUT)
	#GPIO.output(15,GPIO.HIGH)
	GPIO.cleanup()
