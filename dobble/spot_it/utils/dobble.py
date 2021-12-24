import random
import time
import csv

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
        card1 = self.cards_list[card_pair[0]]
        card2 = self.cards_list[card_pair[1]]

        common_image = [i for i in card1 if i in card2]
        return common_image

    def update_card(self):

        #image_mapping connect images path in csv and the image coordinates
        self.card1 ,self.card2 = self.cards_pairs_list[self.card_pair_no]
        self.common_image = self.get_common_image(self.card_pair_no)
        self.card_pair_no+=1
