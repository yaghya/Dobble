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

# board = pygame.transform.scale(pygame.image.load(os.path.join("img","board_alt.png")), (750, 750))
starting_image =  pygame.image.load(os.path.join("./data/starting_image.png"))
white = (255,255,255)
card_num = 0

def menu_screen(win, name):
    global dobble, starting_image
    run = True
    offline = False

    while run:
        starting_image = pygame.transform.scale(starting_image, (width, height))
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
                    dobble = connect()
                    dobble.Width = width
                    dobble.Height = height
                    print("connection established")
                    run = False
                    main()
                    break
                except:
                    print("Server Offline")
                    offline = True

def display_image(coord,gameDisplay,colour):
    coord1 =coord[0]
    coord2 = coord[1]
    # print(coord[0][0])
    # import pdb; pdb.set_trace()
    rect = pygame.Rect(coord1[0][0],coord1[0][1],coord2[0][0]-coord1[0][0],coord2[0][1]-coord1[0][1])
    pygame.draw.rect(gameDisplay, pygame.Color(colour), rect)

    return
    card_img_name = f'{self.card_dir}/card_{card_no}.png'
    card_img = pygame.image.load(card_img_name)
    card_img = pygame.transform.scale(card_img, (400, 400))
    gameDisplay.blit(card_img, (coord[0],coord[1]))


def load_images(dobble,win):

    # card = [[0,0],[0,2],[0,4],[2,0],[2,2],[2,4],[4,0],[4,2],[4,4]]
    # card = random.sample(card,8)
    # print(len(dobble.card1_images),len(dobble.card2_images),len(square1),len(square2))
    for i in range(len(dobble.card1_images)):
        # u,v = card[i]
        # print(u,v)
        # len(random.choice([[(a,b) for a in np.linspace(square2[u][v][0],square2[u+1][v+1][0],3)[1:2]]for b in np.linspace(square2[u][v][1],square2[u+1][v+1][1],3)[1:2]]))
        # dobble.card1_images[i] = random.choice([[(a,b) for a in np.linspace(square1[u][v][0],square1[u+1][v+1][0],3)[1:2]]for b in np.linspace(square1[u][v][1],square1[u+1][v+1][1],3)[1:2]]),random.choice([[(a,b) for a in np.linspace(square1[u+1][v+1][0],square1[u+2][v+2][0],3)[1:2]]for b in np.linspace(square1[u+1][v+1][1],square1[u+2][v+2][1],3)[1:2]])
        # print(dobble.card1_images[i])
        display_image(dobble.card1_images[i],win,"red")
        # dobble.card2_images[i] = [random.choice([[(a,b) for a in np.linspace(square2[u][v][0],square2[u+1][v+1][0],3)[1:2]]for b in np.linspace(square2[u][v][1],square2[u+1][v+1][1],3)[1:2]]),
                            # random.choice([[(a,b) for a in np.linspace(square2[u+1][v+1][0],square2[u+2][v+2][0],3)[1:2]]for b in np.linspace(square2[u+1][v+1][1],square2[u+2][v+2][1],3)[1:2]])]
        # print(dobble.card2_images[i])
        display_image(dobble.card2_images[i],win,"yellow")


# def redraw_gameWindow(win, dobble, p1, p2, color, ready):
def redraw_gameWindow(win, dobble, color, ready):

    global card_num
    # win.blit(board, (0, 0))
    # bo.draw(win, color)

    # formatTime1 = str(int(p1//60)) + ":" + str(int(p1%60))
    # formatTime2 = str(int(p2 // 60)) + ":" + str(int(p2 % 60))
    # if int(p1%60) < 10:
    #     formatTime1 = formatTime1[:-1] + "0" + formatTime1[-1]
    # if int(p2%60) < 10:
    #     formatTime2 = formatTime2[:-1] + "0" + formatTime2[-1]

    font = pygame.font.SysFont("comicsans", 30)
    # try:
    #     txt = font.render(bo.p1Name + "\'s Time: " + str(formatTime2), 1, (255, 255, 255))
    #     txt2 = font.render(bo.p2Name + "\'s Time: " + str(formatTime1), 1, (255,255,255))
    # except Exception as e:
    #     print(e)
    # win.blit(txt, (520,10))
    # win.blit(txt2, (520, 700))

    # txt = font.render("Press q to Quit", 1, (255, 255, 255))
    # win.blit(txt, (10, 20))

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

    if not color == "s":
        if color == "p1":
            txt3 = font.render("YOU ARE PLAYER1", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
        else:
            txt3 = font.render("YOU ARE PLAYER2", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
    
    if ready and card_num !=dobble.card_pair_no:
        win.fill('white')
        if color == "p1":
            txt3 = font.render("YOU ARE PLAYER1", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
        else:
            txt3 = font.render("YOU ARE PLAYER2", 1, (255, 0, 0))
            win.blit(txt3, (width / 2 - txt3.get_width() / 2, 100))
        print(dobble.card_pair_no ,card_num)
        load_images(dobble,win)
        card_num +=1
    pygame.display.update()
        # if bo.turn == color:
        #     txt3 = font.render("YOUR TURN", 1, (255, 0, 0))
        #     win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))
        # else:
        #     txt3 = font.render("THEIR TURN", 1, (255, 0, 0))
        #     win.blit(txt3, (width / 2 - txt3.get_width() / 2, 700))

    


def main():
    global turn, dobble, name

    color = dobble.start_user
    print("color",color)
    count = 0

    # dobble = n.send("show_card")
    # print("card_updated")
    dobble = n.send("name " + name)
    print(dobble.p1name,dobble.p2name)
    clock = pygame.time.Clock()
    run = True
    win.fill(white)

    while run:
        if not color == "s":
            # # p1Time = dobble.time1
            # # p2Time = dobble.time2
            if count == 60:
                dobble = n.send("get")
                count = 0
            else:
                count += 1
            clock.tick(30)

        try:
            # redraw_gameWindow(win, dobble, p1Time, p2Time, color, dobble.ready) 
            redraw_gameWindow(win, dobble, color, dobble.ready) #draw images depending on card_no info in dobble object

        except Exception as e:
            print(e)
            end_screen(win, "Other player left")
            run = False
            break

        # if not color == "s":
        #     if p1Time <= 0:
        #         dobble = n.send("winner b")
        #     elif p2Time <= 0:
        #         dobble = n.send("winner w")

        #     if dobble.check_mate("b"):
        #         dobble = n.send("winner b")
        #     elif dobble.check_mate("w"):
        #         dobble = n.send("winner w")

        if dobble.winner == "p1":
            end_screen(win, f"{dobble.p1name} is the Winner!")
            run = False
        elif dobble.winner == "p2":
            end_screen(win, f"{dobble.p2name} is the winner")
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                # pygame.quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_q and color != "s":
            #         # quit game
            #         if color == "p1":
            #             dobble = n.send("winner p1")
            #         else:
            #             dobble = n.send("winner p2")

            #     if event.key == pygame.K_RIGHT:
            #         dobble = n.send("forward")

            #     if event.key == pygame.K_LEFT:
            #         dobble = n.send("back")


            #MOUSEBUTTONDOWN Send the image selected info and get results it is a winner or not
            if event.type == pygame.MOUSEBUTTONUP and color != "s":
                if  dobble.ready:
                    pos = pygame.mouse.get_pos()
                    # i, j = click(pos) # depending on the pos select the image
                    dobble = n.send("select " + str(pos[0]) + " " + str(pos[1]) + " " + color)
                    # check whether it is correct or not and highlight the image with red or green colour
    
    n.disconnect()
    dobble = 0
    menu_screen(win)

def end_screen(win, text):
    pygame.font.init()
    font = pygame.font.SysFont("comicsans", 80)
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
menu_screen(win, name)