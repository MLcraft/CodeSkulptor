# Implementation of classic arcade game Pong
# Made by MLcraft

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = []
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
paddle1_pos = [HALF_PAD_WIDTH, ((HEIGHT - PAD_HEIGHT) / 2) + HALF_PAD_HEIGHT]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
score1 = 0
score2 = 0
# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2, HEIGHT/2]
    if direction == RIGHT:
        ball_vel = [3, -3]
    elif direction == LEFT:
        ball_vel = [-3, 3]
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, v1, v2, v3, v4
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ((ball_pos[1] - BALL_RADIUS - 3 > 0) and (ball_pos[1] + BALL_RADIUS + 3 < HEIGHT)):
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif (ball_pos[1] - BALL_RADIUS - 3 <= 0) or (ball_pos[1] + BALL_RADIUS + 3 >= HEIGHT):
        ball_vel[1] = -ball_vel[1]
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    if ((ball_pos[0] - BALL_RADIUS - 3 > PAD_WIDTH) and (ball_pos[0] + BALL_RADIUS + 3 < (WIDTH - PAD_WIDTH))):
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif (ball_pos[0] - BALL_RADIUS - 3 <= PAD_WIDTH) and ((ball_pos[1] >= (paddle1_pos[1] - HALF_PAD_HEIGHT)) and (ball_pos[1] <= (paddle1_pos[1] + HALF_PAD_HEIGHT))):
        ball_vel[0] = -ball_vel[0]
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif (ball_pos[0] + BALL_RADIUS + 3 >= (WIDTH - PAD_WIDTH)) and ((ball_pos[1] >= (paddle2_pos[1] - HALF_PAD_HEIGHT)) and (ball_pos[1] <= (paddle2_pos[1] + HALF_PAD_HEIGHT))):
        ball_vel[0] = -ball_vel[0]
        ball_pos[0] += ball_vel[0]
        ball_pos[1] += ball_vel[1]
    elif (ball_pos[0] - BALL_RADIUS - 3 <= PAD_WIDTH):
        score2 += 1
        spawn_ball(RIGHT)
    elif (ball_pos[0] + BALL_RADIUS + 3 >= (WIDTH - PAD_WIDTH)):
        score1 += 1
        spawn_ball(LEFT)
    
        #ball_vel[0] = -ball_vel[0]
        #ball_pos[0] += ball_vel[0]
        #ball_pos[1] += ball_vel[1]
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_pos[1] - HALF_PAD_HEIGHT - 3 > 0) and (paddle1_pos[1] + HALF_PAD_HEIGHT + 3 < HEIGHT)):
        paddle1_pos[1] += paddle1_vel[1]
    elif (paddle1_pos[1] - HALF_PAD_HEIGHT - 3 <= 0):
        if paddle1_vel[1] == 3:
            paddle1_pos[1] += paddle1_vel[1]
    elif (paddle1_pos[1] + HALF_PAD_HEIGHT + 3 >= HEIGHT):
        if paddle1_vel[1] == -3:
            paddle1_pos[1] += paddle1_vel[1]
    if ((paddle2_pos[1] - HALF_PAD_HEIGHT - 3 > 0) and (paddle2_pos[1] + HALF_PAD_HEIGHT + 3 < HEIGHT)):
        paddle2_pos[1] += paddle2_vel[1]
    elif (paddle2_pos[1] - HALF_PAD_HEIGHT - 3 <= 0):
        if paddle2_vel[1] == 3:
            paddle2_pos[1] += paddle2_vel[1]
    elif (paddle2_pos[1] + HALF_PAD_HEIGHT + 3 >= HEIGHT):
        if paddle2_vel[1] == -3:
            paddle2_pos[1] += paddle2_vel[1]
    # draw paddles
    v1 = paddle1_pos[1] - HALF_PAD_HEIGHT
    v2 = paddle1_pos[1] + HALF_PAD_HEIGHT	
    v3 = paddle2_pos[1]- (PAD_HEIGHT / 2)
    v4 = paddle2_pos[1] + (PAD_HEIGHT / 2)
    canvas.draw_polygon([[0, v1], [PAD_WIDTH, v1], [PAD_WIDTH, v2], [0, v2]], 1, "White", "White")
    canvas.draw_polygon([[WIDTH - PAD_WIDTH, v3], [WIDTH - PAD_WIDTH, v4], [WIDTH, v4], [WIDTH, v3]], 1, "White", "White")
    
    # draw scores
    canvas.draw_text(str(score1), [(WIDTH / 4), 40], 24, "White")
    canvas.draw_text(str(score2), [3 * (WIDTH / 4), 40], 24, "White")    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if simplegui.KEY_MAP["s"] == key:
            paddle1_vel[1] = 3
    if simplegui.KEY_MAP["w"] == key:
        paddle1_vel[1] = -3   
    if simplegui.KEY_MAP["down"] == key:
            paddle2_vel[1] = 3
    if simplegui.KEY_MAP["up"] == key:
            paddle2_vel[1] = -3
def keyup(key):
    global paddle1_vel, paddle2_vel
    if (simplegui.KEY_MAP["w"] == key) or (simplegui.KEY_MAP["s"] == key):
        paddle1_vel[1] = 0
    if (simplegui.KEY_MAP["up"] == key) or (simplegui.KEY_MAP["down"] == key):
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)


# start frame
new_game()
frame.start()
