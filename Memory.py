# implementation of card game - Memory
# Made by MLcraft
try:
    from user27_5LlszPPJxQHFMbk import assert_position
    from user33_Bhc7VzXKbXGVQV1 import FPS
    from user34_7pdNdCOBbyLqAZs import Loader

    import simplegui

    SIMPLEGUICS2PYGAME = False
except ImportError:
    from SimpleGUICS2Pygame.codeskulptor_lib import assert_position
    from SimpleGUICS2Pygame.simplegui_lib_fps import FPS
    from SimpleGUICS2Pygame.simplegui_lib_loader import Loader

    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
lst = [0, 1, 2, 3, 4, 5, 6, 7]
lst2 = lst + lst
exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
pos1 = [0, 0]
clicked = []
turns = 0
# helper function to initialize globals
def new_game():
    global state, turns, clicked, exposed
    state = 0
    random.shuffle(lst2)
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    clicked = []
    turns = 0
    #print lst2
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global state, exposed, clicked, turns
    for i in range(16):
        if (pos[0] > pos1[0] + 50 * i) and (pos[0] < pos1[0] + 50 * (i + 1)):
            if (pos[1] > 0) and (pos[1] < 100):
                if state == 0:
                    if exposed[i] != True:
                        exposed[i] = True
                        clicked.append(i)
                        state = 1
                elif state == 1:
                    if exposed[i] != True:	
                        exposed[i] = True
                        clicked.append(i)
                        state = 2
                        turns += 1
                else:
                    if len(clicked) != 0:
                        if lst2[clicked[0]] != lst2[clicked[1]]:
                            exposed[clicked[0]] = False
                            exposed[clicked[1]] = False
                        clicked = []
                       
                    if exposed[i] != True:
                        exposed[i] = True
                        clicked.append(i)
                        state = 1                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i] != True:
            canvas.draw_polygon([(pos1[0] + 50 * i, pos1[1]), (pos1[0] + 50 * (i + 1), pos1[1]), (pos1[0] + 50 * (i + 1), pos1[1] + 100), (pos1[0] + 50 * i, pos1[1] + 100)], 2, "Black", "Green")      
        else:
            canvas.draw_text(str(lst2[i]), (pos1[0] + 50 * i + 13, 80), 54, "White")
    label.set_text("Turns = " + str(turns))
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
