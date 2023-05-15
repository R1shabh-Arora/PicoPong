import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
import random

# Initialize PicoDisplay
WIDTH = 240
HEIGHT = 135
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)
display.set_backlight(0.5)
display.set_font("bitmap8")
paddle_thick = 5

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)
def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()
clear()

# Initialize buttons
button_up = Button(12)
button_down = Button(13)
button_left = Button(14)
button_right = Button(15)
p1points = 0
p2points = 0

# Initialize game objects
player_1_pos = 60
player_2_pos = 60
ball_pos = [120, 67]
ball_dir = [random.choice([-2, 2]), random.choice([-2, 2])]

# Game loop
while True:
    display.set_pen(BLACK)
    display.clear()
    # Handle button inputs
    if button_up.read():
        player_1_pos -= 9
    elif button_down.read():
        player_1_pos += 9
    if button_left.read():
        player_2_pos -= 9
    elif button_right.read():
        player_2_pos += 9

    # Move ball
    ball_pos[0] += ball_dir[0]
    ball_pos[1] += ball_dir[1]

    # Check for ball collision with walls
    if ball_pos[1] < 0 or ball_pos[1] > HEIGHT:
        ball_dir[1] = -ball_dir[1]
    if ball_pos[0] < 0:
        player_1_pos = 60
        player_2_pos = 60
        ball_pos = [120, 67]
        ball_dir = [random.choice([-2, 2]), random.choice([-2, 2])]
        p2points=p2points+1
        
        
    if ball_pos[0] > WIDTH:
        player_1_pos = 60
        player_2_pos = 60
        ball_pos = [120, 67]
        ball_dir = [random.choice([-2, 2]), random.choice([-2, 2])]
        p1points=p1points+1
        

    # Check for ball collision with players
    if (ball_pos[0] == 12 and player_1_pos <= ball_pos[1] <= player_1_pos + 40) or (ball_pos[0] == 228 and player_2_pos <= ball_pos[1] <= player_2_pos + 40):
        ball_dir[0] = -ball_dir[0]
        display.set_pen(CYAN)
    else:
        display.set_pen(WHITE)

    # Draw game elements on PicoDisplay
    display.rectangle(5, player_1_pos, 5, 40)
    display.rectangle(WIDTH-paddle_thick, player_2_pos, 5, 40)
    display.circle(ball_pos[0], ball_pos[1],2)
    display.text(str(p1points),10,5,2,2)
    display.text(str(p2points),230,5,2,2)
    display.update()

    #Paddles don't get off the screen
    if player_1_pos < 0:
        player_1_pos = 0
    if player_1_pos > 95:
        player_1_pos = 95
    if player_2_pos < 0:
        player_2_pos = 0
    if player_2_pos > 95:
        player_2_pos = 95


    #if ball_pos[1] > player_2_pos + 1:
     #   player_2_pos += 3
    #if ball_pos[1] < player_2_pos + 1:
     #   player_2_pos -= 3

    if ball_pos[1] > player_1_pos + 1:
        player_1_pos += 3
    if ball_pos[1] < player_1_pos + 1:
        player_1_pos -= 3


    
    


    #If the score is 10, the game ends
    if p1points == 10:
        display.set_pen(WHITE)
        display.text("Computer Wins!", 30, 50, 230, 3)
        display.update()
        time.sleep(5)
        p1points = 0
        p2points = 0
    
    if p2points == 10:
        display.set_pen(WHITE)
        display.text("Player2 Wins!", 30, 50, 230, 3)
        display.update()
        time.sleep(5)
        p1points = 0
        p2points = 0

    # Pause to control game speed
    time.sleep(0.0001)

