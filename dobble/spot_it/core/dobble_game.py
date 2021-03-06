from operator import xor
from numpy.lib.type_check import imag

from numpy.testing._private.utils import import_nose
import pygame
import os
import time
import math
import numpy as np
import random
import sys
sys.path.append("./")
from spot_it.utils.dobble_client import Network
import pickle
pygame.font.init()
background_colour = (248,248,248)

# board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
starting_image =  pygame.image.load(os.path.join("data/starting_image.png"))
white = background_colour
card_num = 0

card_names = open(os.path.join('data','image_names.txt'),'r+').readlines()


def menu_screen(win):
    global dobble, starting_image, card_num
    run = True
    offline = False

    while run:
        card_num = 0
        starting_image = pygame.transform.scale(starting_image, (width, height))
        win.fill(white)
        win.blit(starting_image, (0,0))
        small_font = pygame.font.SysFont("comicsans", 50)
        
        msg = small_font.render("Click to start", 1, (255, 0, 0))
        if offline:
            msg = small_font.render("Server Offline, Try Again Later...", 1, (255, 0, 0))

        
        win.blit(msg, (width / 2 - msg.get_width() / 2, 500))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                offline = False
                try:
                    print("trying to connect")
                    dobble = connect()
                    # dobble.Width = width
                    # dobble.Height = height
                    print("connection established")
                    # run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True
                    break

def display_image(coord,image_path, gameDisplay):
    coord1 =coord[0]
    coord2 = coord[1]
    # print(coord1,coord2)
    # print(coord[0][0])
    # import pdb; pdb.set_trace()
    # print(os.path.join(str(image_path)))
    img= pygame.image.load(os.path.join(image_path))
    img = pygame.transform.scale(img, (coord2[0]-coord1[0],coord2[1]-coord1[1]))
    win.blit(img, (coord1[0],coord1[1]))
    # rect = pygame.Rect(coord1[0],coord1[1],coord2[0]-coord1[0],coord2[1]-coord1[1])
    # pygame.draw.rect(gameDisplay, pygame.Color(colour), rect)


def load_images(dobble,win):

    # card = [[0,0],[0,2],[0,4],[2,0],[2,2],[2,4],[4,0],[4,2],[4,4]]
    # card = random.sample(card,8)
    # print(len(dobble.card1_images),len(dobble.card2_images),len(square1),len(square2))
    r = int((0.45/2)*width)
    h = (height - 0.45*width)/2
    # print(int(r+(0.1/4)*width),int(h+r),int(3*r+(0.3/4)*width),int(h+r),r,h)
    pygame.draw.circle(win, "black", (int(r+(0.1/4)*width),int(h+r) ), r, int(width/100))
    pygame.draw.circle(win, "black", (int(3*r+(0.3/4)*width),int(h+r) ), r, int(width/100))

    for i in range(len(dobble.card1_images)):
        # u,v = card[i]
        # print(u,v)
        # len(random.choice([[(a,b) for a in np.linspace(square2[u][v][0],square2[u+1][v+1][0],3)[1:2]]for b in np.linspace(square2[u][v][1],square2[u+1][v+1][1],3)[1:2]]))
        # dobble.card1_images[i] = random.choice([[(a,b) for a in np.linspace(square1[u][v][0],square1[u+1][v+1][0],3)[1:2]]for b in np.linspace(square1[u][v][1],square1[u+1][v+1][1],3)[1:2]]),random.choice([[(a,b) for a in np.linspace(square1[u+1][v+1][0],square1[u+2][v+2][0],3)[1:2]]for b in np.linspace(square1[u+1][v+1][1],square1[u+2][v+2][1],3)[1:2]])
        # print(dobble.card1_images[i])
        display_image(dobble.card1_images[i],str(dobble.card_names[int(dobble.card1[i])-1])[:-1],win)
        # display_image(dobble.card1_images[i],str(card_names[int(dobble.card1[i])-1])[:-1],win)
        # dobble.card2_images[i] = [random.choice([[(a,b) for a in np.linspace(square2[u][v][0],square2[u+1][v+1][0],3)[1:2]]for b in np.linspace(square2[u][v][1],square2[u+1][v+1][1],3)[1:2]]),
                            # random.choice([[(a,b) for a in np.linspace(square2[u+1][v+1][0],square2[u+2][v+2][0],3)[1:2]]for b in np.linspace(square2[u+1][v+1][1],square2[u+2][v+2][1],3)[1:2]])]
        # print(dobble.card2_images[i])
        display_image(dobble.card2_images[i],str(dobble.card_names[int(dobble.card2[i])-1])[:-1],win)
        # display_image(dobble.card2_images[i],str(card_names[int(dobble.card2[i])-1])[:-1],win)


# def redraw_gameWindow(win, dobble, p1, p2, color, ready):
def redraw_gameWindow(win, dobble, color, ready):

    global card_num
    
    font = pygame.font.SysFont("comicsans", 30)

    if color == "s":
        txt3 = font.render("SPECTATOR MODE", 1, (255, 0, 0))
        win.blit(txt3, (width/2-txt3.get_width()/2, 50))

    if not ready:
        show = "Waiting for Opponent"
        if color == "s":
            show = "Waiting for Players"
        font = pygame.font.SysFont("comicsans", 80)
        txt = font.render(show, 1, (255, 0, 0))
        win.blit(txt, (width/2 - txt.get_width()/2, 300))

    if color == "p1":
        txt3 = font.render("YOU ARE PLAYER1", 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
    elif color == "p2":
        txt3 = font.render("YOU ARE PLAYER2", 1, (255, 0, 0))
        win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
    
    if ready and card_num !=dobble.card_pair_no:
        win.fill(white)
        if color == "p1":
            txt3 = font.render("YOU ARE PLAYER1", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
        else:
            txt3 = font.render("YOU ARE PLAYER2", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
        p1_points = font.render(str(dobble.p1name)+" "+str(dobble.p1_points), 2, (255, 0, 0))
        win.blit(p1_points, ((0.1)*width / 2 , 100))
        p2_points = font.render(str(dobble.p2name)+" "+str(dobble.p2_points), 2, (255, 0, 0))
        win.blit(p2_points, (width -(0.1)*width/2 - txt3.get_width() / 2, 100))

        print(dobble.card_pair_no ,card_num)
        load_images(dobble,win)
        card_num +=1
    pygame.display.update()

    


def main():
    global dobble, name

    color = dobble.start_user
    print("color",color)
    count = 0

    dobble = n.send("name " + name)
    print(dobble.p1name,dobble.p2name)
    dobble = n.send("width&height "+str(width) +" "+str(height))
    clock = pygame.time.Clock()
    run = True
    win.fill(white)

    while run:
        if not color=='s':
            dobble = n.send("")
        try:
            redraw_gameWindow(win, dobble, color, dobble.ready) #draw images depending on card_no info in dobble object

        except Exception as e:
            print("redraw_gameWindow error",e)
            end_screen(win, "Other player left")
            time.sleep(0.1)
            run = False
            break

        if not color == "s" and dobble.card_pair_no ==6:
            if dobble.p1_points > dobble.p2_points:
                dobble = n.send("winner p1")
            elif dobble.p1_points < dobble.p2_points:
                dobble = n.send("winner p2")
            else :
                dobble = n.send("tie game")

        if dobble.winner == "p1":
            end_screen(win, f"{dobble.p1name} is the Winner!")
            run = False
            time.sleep(0.5)
            break
        elif dobble.winner == "p2":
            end_screen(win, f"{dobble.p2name} is the winner")
            run = False
            time.sleep(0.5)
            break
        elif dobble.winner == "draw":
            end_screen(win, f"Game Draw")
            run = False
            time.sleep(0.5)
            break
        
        mouse = pygame.mouse.get_pos()
        highlight(mouse)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break
                # pygame.quit()


            #MOUSEBUTTONDOWN Send the image selected info and get results it is a winner or not
            if event.type == pygame.MOUSEBUTTONDOWN and color != "s":
                if dobble.ready:
                    pos = pygame.mouse.get_pos()
                    # print(pos)
                    card_number,image_num = click(pos) # depending on the pos select the image
                    if image_num!=-1:
                        print(image_num)
                        check(image_num,card_number)
                        count =0
                        pygame.display.update()
                        dobble = n.send("selected " + card_number+" "+ str(image_num) + " " +color)
    
    n.disconnect()
    dobble = 0
    menu_screen(win)

def click(pos):
    """
    return selected image
    """
    x = pos[0]
    y = pos[1]

    for i,coord in enumerate(dobble.card1_images):
        A = coord[0]
        B = coord[1]
        if A[0]<=x<=B[0] and A[1]<=y<=B[1]:
            return "card1",i
    
    for i,coord in enumerate(dobble.card2_images):
        A = coord[0]
        B = coord[1]
        if A[0]<=x<=B[0] and A[1]<=y<=B[1]:
            return "card2",i
    
    return "no_card",-1

def highlight(mouse):
    x = mouse[0]
    y = mouse[1]


    for i,coord in enumerate(dobble.card1_images):
        A = coord[0]
        B = coord[1]
        if A[0]<=x<=B[0] and A[1]<=y<=B[1]:
            pygame.draw.rect(win, [0,0,255], [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
        else:
            pygame.draw.rect(win, white, [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
    
    for i,coord in enumerate(dobble.card2_images):
        A = coord[0]
        B = coord[1]
        if A[0]<=x<=B[0] and A[1]<=y<=B[1]:
            pygame.draw.rect(win, [0,0,255], [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
        else:
            pygame.draw.rect(win, white, [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
    

def check(image_num,card_number):
    print(int(image_num),card_number)
    if card_number=="card1":
        coord = dobble.card1_images[int(image_num)]
        A = coord[0]
        B = coord[1]
        if  int(image_num)==int(dobble.card1_common_image):
            pygame.draw.rect(win, [0,255,0], [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
            print("green")
        else:
            pygame.draw.rect(win, [255,0,0], [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
            print("red")

    elif card_number=="card2":
        coord = dobble.card2_images[int(image_num)]
        A = coord[0]
        B = coord[1]
        if  int(image_num)==int(dobble.card2_common_image):
            pygame.draw.rect(win, [0,255,0], [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
            print("green")
        else:
            pygame.draw.rect(win, [255,0,0], [A[0]-2,A[1]-2,B[0]-A[0]+2,B[1]-A[1]+2],2)
            print("red")

    print("done")
    

        
        

def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
    win.fill(white)
    txt = font.render(text,1, (255,0,0))
    win.blit(txt, (width / 2 - txt.get_width() / 2, 300))
    pygame.display.update()

    pygame.time.set_timer(pygame.USEREVENT+1, 3000)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                run = False
            elif event.type == pygame.KEYDOWN:
                run = False
            elif event.type == pygame.USEREVENT+1:
                run = False


def connect():
    global n
    n = Network()
    return n.dobble


name = input("Please type your name: ")
win = pygame.display.set_mode()
width, height = win.get_size()
pygame.display.set_caption("Dobble Game")
menu_screen(win)