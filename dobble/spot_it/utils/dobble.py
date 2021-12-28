import random
import time
import csv
import numpy as np
import math
# import tkinter
# root = tkinter.Tk()
# root.withdraw()
# width,height = root.winfo_screenwidth(), root.winfo_screenheight()

def read_csv(file_path):
    with open(file_path, newline='\n') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    return your_list

class Dobble:
    rect = (113,113,525,525)
    startX = rect[0]
    startY = rect[1]

    card_pack_path = "./generated/card_pack.csv"

    def __init__(self):

        self.ready = False
        # self.image_path = "path using pack_no"
        
        self.p1name = "Player1"
        self.p2name = "Player2"
        self.storedTime1 = 0
        self.storedTime2 = 0

        self.winner = None
        self.startTime = time.time()

        #self.16images_info = rectangle_coordinate
        self.card1_images = [[(0,0) for i in range(2)]for j in range(8)]
        self.card2_images = [[(0,0) for i in range(2)]for j in range(8)]



        #self.cards = get_cards_using_doble_utils_generate_cards  or read_from_a_csv_file
        self.cards_list = read_csv(self.card_pack_path)
        self.cards_pairs_list = self.get_cards_pairs_list()

        self.card_pair_no = 0


        self.Width = 1200
        self.Height = 900
    
    def compute_image_coordinates(self):
        global square1,square2

        r = (0.45/2)*self.Width
        d = r - (r/math.sqrt(2))
        h = (self.Height - 0.45*self.Width)/2

        x1  = d+(0.1/4)*self.Width
        x2 = x1 + math.sqrt(2)*r
        x3 = 2*r + (0.3/4)*self.Width + d
        x4 = x3 + math.sqrt(2)*r

        y1 = h+d
        y2 = h+d +math.sqrt(2)*r

        A = [x1,x2]
        B = [y1,y2]

        C = [x3,x4]
        D = [y1,y2]

        square1 = [[(a,b) for a in np.linspace(A[0],A[1],7)] for b in np.linspace(B[0],B[1],7) ]
        square2 = [[(a,b) for a in np.linspace(C[0],C[1],7)] for b in np.linspace(D[0],D[1],7) ]


    def get_cards_pairs_list(self):
        number_of_cards = len(self.cards_list)
        print("number_of_cards",number_of_cards)
        cards_pairs_list = []
        for i in range(0,len(self.cards_list)):
            for j in range(i+1,len(self.cards_list)):
                if i!=j:
                    cards_pairs_list.append((i,j))

        print(len(cards_pairs_list))
        cards_pairs_list = random.sample(cards_pairs_list,20)
        return cards_pairs_list
    
    def get_common_image(self,i):
        card_pair = self.cards_pairs_list[i]
        self.card1 = self.cards_list[card_pair[0]]
        self.card2 = self.cards_list[card_pair[1]]

        common_image = [i for i in self.card1 if i in self.card2]
        return common_image

    def update_card(self):

        #image_mapping connect images path in csv and the image coordinates
        card = [[0,0],[0,2],[0,4],[2,0],[2,2],[2,4],[4,0],[4,2],[4,4]]

        # if (self.card_pair_no==0):
        self.compute_image_coordinates()
        card1 = random.sample(card,8)
        card2 = random.sample(card,8)
        for i in range(len(self.card1_images)):
            u,v = card1[i]
            # print(u,v)
            # print([(a,b) for a in np.linspace(square2[u][v][0],square2[u+1][v+1][0],3)[1:3]for b in np.linspace(square2[u][v][1],square2[u+1][v+1][1],3)[1:3]])
            
            self.card1_images[i] = [random.choice([(a,b) for a in np.linspace(square1[u][v][0],square1[u+1][v+1][0],5)[1:3]for b in np.linspace(square1[u][v][1],square1[u+1][v+1][1],5)[3:5]]),random.choice([(a,b) for a in np.linspace(square1[u+1][v+1][0],square1[u+2][v+2][0],5)[1:3]for b in np.linspace(square1[u+1][v+1][1],square1[u+2][v+2][1],5)[3:5]])]
            # print(self.card1_images[i])
            u,v = card2[i]
            self.card2_images[i] = [random.choice([(a,b) for a in np.linspace(square2[u][v][0],square2[u+1][v+1][0],5)[1:3]for b in np.linspace(square2[u][v][1],square2[u+1][v+1][1],5)[3:5]]),random.choice([(a,b) for a in np.linspace(square2[u+1][v+1][0],square2[u+2][v+2][0],5)[1:3]for b in np.linspace(square2[u+1][v+1][1],square2[u+2][v+2][1],5)[3:5]])]
    
        # self.card1 ,self.card2 = self.cards_pairs_list[self.card_pair_no]
        self.common_image = self.get_common_image(self.card_pair_no)
        print(self.card1,self.card2)

        print(np.where(np.asarray(self.card1)==self.common_image),np.asarray(self.card1))
        self.card1_common_image = np.where(np.asarray(self.card1)==self.common_image[0])[0][0]
        self.card2_common_image = np.where(np.asarray(self.card2)==self.common_image[0])[0][0]
        print(self.common_image,self.card_pair_no)
        self.card_pair_no+=1
