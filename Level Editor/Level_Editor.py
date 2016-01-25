import pygame, math, sys

from pygame.locals import *

screen = pygame.display.set_mode((1024, 768))
clock = pygame.time.Clock()
running = True

#Each object in this list is a list containing [pygame.Rect, (r,g,b)]
boxes = []

box_colour = (255, 0, 0)
box_selected_colour = (0, 255, 0)
selected_box_index = -1

def Initialise():
    boxes.append([pygame.Rect(10, 10, 10, 10), (255, 0, 0)])
    boxes.append([pygame.Rect(30, 30, 30, 30), (255, 0, 0)])
    return

def Place_Box():
    mouse_pos = pygame.mouse.get_pos()

    boxes.append([pygame.Rect(mouse_pos[0], mouse_pos[1], 10, 10), box_colour])

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

    inflate_amount = 1
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

def Render():
    screen.fill((0,0,0))

    for box in boxes:
        pygame.draw.rect(screen, box[1], box[0])

    pygame.display.flip()
    return

def Input():
    inflate_width_key = pygame.K_q
    deflate_width_key = pygame.K_a

    inflate_height_key = pygame.K_w
    deflate_height_key = pygame.K_s

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

    pressed = pygame.key.get_pressed()

    if pressed[inflate_width_key]:
        Change_Box_Size(True, "Width")
    elif pressed[deflate_width_key]:
        Change_Box_Size(False, "Width")

    if pressed[inflate_height_key]:
        Change_Box_Size(True, "Height")
    elif pressed[deflate_height_key]:
        Change_Box_Size(False, "Height")

if __name__ == "__main__":
   
    Initialise()

    while running:
        Input()
        Render()