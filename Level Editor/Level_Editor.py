import pygame, math, sys, input_box

from pygame.locals import *
from input_box import ask
from builtins import int, str, print

screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
pygame.key.set_repeat(600, 600)
running = True

#Each object in this list is a list containing [pygame.Rect, (r,g,b)]
boxes = []

player_entry = pygame.Rect(-255,-255,0,0)
player_exit = pygame.Rect(-255,-255,0,0)

box_colour = (255, 0, 0)
box_selected_colour = (0, 255, 0)
selected_box_index = -1

def my_round(x, base=10):
    return int(base * round(float(x)/base))

def Serialise(file_name):
    global boxes
    global player_entry
    global player_exit

    if file_name.find(".txt", len(file_name) - 3) is -1:
        file_name += ".txt"

    file_out = open(file_name, "w")

    width = screen.get_width()
    height = screen.get_height()

    centre_pos = (my_round(width/ 2), my_round(height/ 2))

    for numX in range(int(-width / 2), int(width / 2), 10):
        for numY in range(int(-height / 2), int(height / 2), 10):
            file_out.write("GRASS (" + str(numX) + ",-1.779," + str(numY) + ") (10,1,10) (1.51,0,0)\n")
    

    if player_entry.left != -255:
        y_position = "1.5"
        x_pos = player_entry.x - centre_pos[0]
        z_pos = centre_pos[1] - player_entry.y

        pos_string = "(" + str(x_pos) + "," + y_position + "," + str(z_pos) + ")"
        file_out.write("PLAYER " + pos_string + "\n")

    if player_exit.left != -255:
        y_position = "1.5"
        x_pos = player_exit.x - centre_pos[0]
        z_pos = centre_pos[1] - player_exit.y

        pos_string = "(" + str(x_pos) + "," + y_position + "," + str(z_pos) + ")"
        file_out.write("EXIT " + pos_string + "(0.2,0.2,0.2) (0,0,0)\n")

    for box_object in boxes:
        box = box_object[0]
        size_string = "(" + str(abs(box.width)) + "," + str(max(box.width, box.height)) + "," + str(abs(box.height)) + ")"
        
        y_position = "-0.48"
        x_pos = box.x - centre_pos[0]
        z_pos = centre_pos[1] - box.y

        pos_string = "(" + str(x_pos) + "," + y_position + "," + str(z_pos) + ")"
        print("Crate " + pos_string + " " + size_string + " (0,0,0)")
        file_out.write("CRATE " + pos_string + " " + size_string + " (0,0,0)\n")

    file_out.close()

def Initialise():
    pygame.font.init()
    return

def Place_Box():
    mouse_pos = pygame.mouse.get_pos()

    boxes.append([pygame.Rect(my_round(mouse_pos[0]), my_round(mouse_pos[1]), 10, 10), box_colour])

def Select_Box():
    global selected_box_index

    mouse_pos = pygame.mouse.get_pos()
    
    for box in boxes:
        if box[0].collidepoint(mouse_pos):
            #Trying to select the box 
            if box[1] == box_colour:
                #Deselect currently selected box, if it exists
                if selected_box_index is not -1:
                    boxes[selected_box_index][1] = box_colour

                #Select correct box
                box[1] = box_selected_colour
                selected_box_index = boxes.index(box)
            else:
                #Otherwise, we're trying to deselect the box
                box[1] = box_colour
                selected_box_index = -1
            return True

    return False

"""
inflate is boolean to indicate if the dimesion is getting larger or smaller
axis is string; either "Width" or "Height"
"""
def Change_Box_Size(inflate = True, axis = "Width"):
    global selected_box_index
  
    if selected_box_index is -1:
        return

    inflate_amount = 10
    if not inflate:
        inflate_amount = inflate_amount * -1


    if axis is "Width":
        if boxes[selected_box_index][0].width + inflate_amount > 1:
            boxes[selected_box_index][0].width += inflate_amount
    elif axis is "Height":
        if boxes[selected_box_index][0].height + inflate_amount > 1:
            boxes[selected_box_index][0].height += inflate_amount
    else:
        return

def render_grid(screen):
    grid_size = 10
    x = 0
    while x < screen.get_width():
        pygame.draw.line(screen, (0,0,255), (x, 0), (x, screen.get_height()))
        x = x + grid_size

    y = 0
    while y < screen.get_height():
        pygame.draw.line(screen, (0,0,255), (0, y), (screen.get_width(), y))
        y = y + grid_size

def Render():
    screen.fill((0,0,0))

    render_grid(screen)
    for box in boxes:
        pygame.draw.rect(screen, box[1], box[0])

    if player_entry.left != -255:
        pygame.draw.rect(screen, (255, 255, 0), player_entry)

    if player_exit.left != -255:
        pygame.draw.rect(screen, (0, 0, 255), player_exit)

    centre_pos = (screen.get_width() / 2, screen.get_height() / 2)
    pygame.draw.rect(screen, (255, 255, 0), pygame.Rect(centre_pos[0], centre_pos[1], 10, 10))

    help_string = "q - increase width; a - decrease width; w - increase height; s - decrease height; p - place player entry; e - place player exit"
    font = pygame.font.Font(None, 15)
    help_text = font.render(help_string, True, (255,255,255), None)
    screen.blit(help_text, (5, screen.get_height() - help_text.get_height() - 5))
    
    pygame.display.flip()

def Input():
    inflate_width_key = pygame.K_q
    deflate_width_key = pygame.K_a

    inflate_height_key = pygame.K_w
    deflate_height_key = pygame.K_s

    make_player_entry = pygame.K_p
    make_player_exit = pygame.K_e

    global player_entry
    global player_exit
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global running
                running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Select_Box()
                elif event.button == 3:
                    Place_Box()
            
            if event.type == pygame.KEYDOWN:
                if event.key == inflate_width_key:
                    Change_Box_Size(True, "Width")
                elif event.key == deflate_width_key:
                    Change_Box_Size(False, "Width")
                if event.key == inflate_height_key:
                    Change_Box_Size(True, "Height")
                elif event.key == deflate_height_key:
                    Change_Box_Size(False, "Height")
                elif event.key == make_player_entry:
                    mouse_pos = pygame.mouse.get_pos()
                    player_entry = pygame.Rect(my_round(mouse_pos[0]), my_round(mouse_pos[1]), 10, 10)
                elif event.key == make_player_exit:
                    mouse_pos = pygame.mouse.get_pos()
                    player_exit = pygame.Rect(my_round(mouse_pos[0]), my_round(mouse_pos[1]), 10, 10)
                
                if event.key == pygame.K_f:
                    file_name = ask(screen, "Desired file name?")     
                    Serialise(file_name)          

if __name__ == "__main__":
   
    Initialise()

    while running:
        Input()
        Render()

    pygame.quit()