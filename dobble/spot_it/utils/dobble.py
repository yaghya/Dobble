import random
import time

class Dobble:
    rect = (113,113,525,525)
    startX = rect[0]
    startY = rect[1]

    pack_list = [1,2,3]

    def __init__(self):

        self.pack_no = random.choice(self.pack_list)
        self.ready = False
        self.image_path = "path using pack_no"
        
        self.p1name = "Player1"
        self.p2name = "Player2"
        self.storedTime1 = 0
        self.storedTime2 = 0

        self.winner = None
        self.startTime = time.time()

        #self.16images_info = rectangle_coordinate

        #self.cards = get_cards_using_doble_utils_generate_cards  or read_from_a_csv_file

        self.current_card_no = 0


    def show_card(self):

        #image_mapping connect images path in csv and the image coordinates

        self.current_card_no +=1
