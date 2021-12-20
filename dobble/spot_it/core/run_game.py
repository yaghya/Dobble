import pygame
import os,sys
import csv
import random
sys.path.append('./')


class DobbleGame:

    def __init__(self,card_dir):
        self.display_width = 1200
        self.display_height = 800

        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('chartreuse4')
        
        self.card_dir = card_dir
        self.cards_list = [os.path.join(self.card_dir,card) for card in os.listdir(self.card_dir) if '.png' in card ]
        self.svg_dir = self.card_dir.split('_png')[0]
        self.card_names = open(os.path.join(self.svg_dir,'image_names.txt'),'r+').readlines()
        
        self.icons = self.get_icons()
        self.cards_pairs_list = self.get_cards_pairs_list()
        self.cards_image_list = self.get_card_names()
        self.score = 0

    def get_icons(self):
        icons = {'quit':[1100,50,'quit'],'score':[640,40],'img1':[120,80],'img2':[720,80]}
        for i in range(1,8):
            button_name =f'button_{i}'
            x = (i-1)*(1200/7) + 20
            y = 500
            icons[button_name]=[x,y,'']
        for i in range(8,16):
            button_name =f'button_{i}'
            x = (i-8)*(1200/8) + 5
            y = 600
            icons[button_name]=[x,y,'']
        return icons
    
    def get_card_names(self):
        
        file = open(os.path.join(self.svg_dir,'card_pack.csv'), "r")
        csv_reader = csv.reader(file)

        cards_image_list = []
        for row in csv_reader:
            cards_image_list.append(row)
        return cards_image_list

    def get_cards_pairs_list(self):
        number_of_cards = len(self.cards_list)
        print("number_of_cards",number_of_cards)
        cards_pairs_list = []
        for i in range(0,len(self.cards_list)):
            for j in range(i+1,len(self.cards_list)):
                if i!=j:
                    cards_pairs_list.append((i,j))

        print(len(cards_pairs_list))
        cards_pairs_list = random.sample(cards_pairs_list,100)
        return cards_pairs_list
            
    def display_image(self,coord,card_no,gameDisplay):
        card_img_name = f'{self.card_dir}/card_{card_no}.png'
        card_img = pygame.image.load(card_img_name)
        card_img = pygame.transform.scale(card_img, (400, 400))
        gameDisplay.blit(card_img, (coord[0],coord[1]))

    def create_button(self,gameDisplay,icon,mouse):
        x = icon[0]
        y = icon[1]
        input_rect = pygame.Rect(x, y, 140, 32)

        # if mouse is hovered on a button it
        # changes to lighter shade 
        if x <= mouse[0] <= x+140 and y <= mouse[1] <= y+32:
            pygame.draw.rect(gameDisplay, self.color_passive, input_rect)
        else:
            pygame.draw.rect(gameDisplay, self.color_active, input_rect)

        text_surface = self.smallfont.render(icon[2], True, (255, 255, 255))
        
        # render at position stated in arguments
        gameDisplay.blit(text_surface, (input_rect.x+5, input_rect.y+5))
    
    def get_common_image(self,i):
        card_pair = self.cards_pairs_list[i]
        card1 = self.cards_image_list[card_pair[0]]
        card2 = self.cards_image_list[card_pair[1]]

        common_image = [i for i in card1 if i in card2]
        j = 1
        for image_no in card1:
            button_name = f'button_{j}'
            # print(str(self.card_names[int(image_no)-1])[:-1])
            self.icons[button_name][2] = str(self.card_names[int(image_no)-1])[:-1]
            j+=1
        for image_no in card2:
            if image_no!=common_image[0]:
                # print(str(self.card_names[int(image_no)-1])[:-1])
                button_name = f'button_{j}'
                self.icons[button_name][2] = str(self.card_names[int(image_no)-1])[:-1]
                j+=1
        return str(self.card_names[int(common_image[0])-1])[:-1]
        
    def start_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        #create a screen
        gameDisplay = pygame.display.set_mode((self.display_width,self.display_height))
        pygame.display.set_caption('Dobble')
        self.smallfont = pygame.font.SysFont('Corbel',20)


        crashed = False
        i = 0
        common_image_name = self.get_common_image(i)
        print(common_image_name)
        while not crashed:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    crashed = True
                
                #checks if a mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    #if the mouse is clicked on the
                    # button the game is terminated
                    x = self.icons['quit'][0]
                    y = self.icons['quit'][1]
                    if x <= mouse[0] <= x+140 and y <= mouse[1] <= y+40:
                        crashed = True

                    for button_name in self.icons:
                        if 'button' in button_name:
                            x = self.icons[button_name][0]
                            y = self.icons[button_name][1]
                            if x <= mouse[0] <= x+140 and y <= mouse[1] <= y+32:
                                if common_image_name == self.icons[button_name][2]:
                                    self.score+=1
                                i+=1
                                common_image_name = self.get_common_image(i)
                                print(common_image_name)

            card_pair = self.cards_pairs_list[i]

            # it will set background color of screen
            gameDisplay.fill((255, 255, 255))
            currentScore = self.smallfont.render('Score: '+ str(self.score),1,(0,0,0))
            gameDisplay.blit(currentScore, (self.icons['score'][0] - currentScore.get_width()/2, self.icons['score'][1]))

            # stores the (x,y) coordinates into
            # the variable as a tuple
            mouse = pygame.mouse.get_pos()

            # draw rectangle and argument passed which should
            # be on screen
            for button_name in self.icons:
                if 'button' in button_name:
                    self.create_button(gameDisplay,self.icons[button_name],mouse)

            # quit button
            self.create_button(gameDisplay,self.icons['quit'],mouse)

            self.display_image(self.icons['img1'],card_pair[0],gameDisplay)
            self.display_image(self.icons['img2'],card_pair[1],gameDisplay)

            pygame.display.update()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    card_dir = './generated/2_png'
    dobble = DobbleGame(card_dir)
    dobble.start_game()