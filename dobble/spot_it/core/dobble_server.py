import socket
from _thread import *
import sys
# from tkinter.constants import S
sys.path.append("./")

from spot_it.utils.dobble import Dobble
import pickle
import time
import pygame

clock = pygame.time.Clock()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 4096)

server = "0.0.0.0"
port = 8000


server_ip = socket.gethostbyname(server)

try:
    s.bind((server, port))

except socket.error as e:
    print(str(e))

s.listen(6)
print("[START] Waiting for a connection")

connections = 0

games = {0:Dobble()}

spectartor_ids = [] 
specs = 0

def read_specs():
    global spectartor_ids

    spectartor_ids = []
    try:
        with open("specs.txt", "r") as f:
            for line in f:
                spectartor_ids.append(line.strip())
    except:
        print("[ERROR] No specs.txt file found, creating one...")
        open("specs.txt", "w")


def threaded_client(conn, game, spec=False):
    global games, connections, specs
    
    if not spec:
        name = None
        dobble = games[game]

        if connections % 2 == 0:
            currentId = "p1"
        else:
            currentId = "p2"


        if currentId == "p2":
            dobble.ready = True
            dobble.startTime = time.time()
        dobble.card_pair_no = 0
        dobble.start_user = currentId

        # Pickle the object and send it to the server
        data_string = pickle.dumps(dobble)
        # print(data_string,len(data_string))
        conn.send(data_string)
        connections += 1

        while True:
            if game not in games:
                break

            try:
                reply = []
                # conn.settimeout(2.0)
                i=0
                packet =conn.recv(4*4096)
                reply.append(packet)
                # while True:
                #     try :
                #         print(i)
                #         packet =conn.recv(4096)
                #         print("packet",packet,len(packet))
                #         if len(packet)==0:
                #             print("no packet receieved")
                #             break
                #         reply.append(packet)
                #         i+=1
                #         if len(packet)<4096:
                #             break
                #     except Exception as e:
                #         print(e)
                #         break
                # conn.settimeout(None)
                d =b"".join(reply)
                print(len(d))
                data = pickle.loads(d)
                if len(data)==0:
                    break
                if "get" not in data:
                    print(conn,data)
                # if not d:
                #     print("breaking because of not d")
                #     break
                # else:
                if data.count("selected") > 0:
                    string = data.split(" ")
                    if string[1]=="card1" and int(string[2])==int(dobble.card1_common_image):
                        print("updating card")
                        if string[3]=="p1":
                            dobble.p1_points+=1
                        else:
                            dobble.p2_points+=1
                        dobble.update_card()
                    elif string[1]=="card2" and int(string[2])==int(dobble.card2_common_image):
                        print("updating card")
                        if string[3]=="p1":
                            dobble.p1_points+=1
                        else:
                            dobble.p2_points+=1
                        dobble.update_card()
                if dobble.winner is not None:
                    break

                if data =="tie game":
                    dobble.winner = "draw"
                    print("[GAME] draw", game)
                if data == "winner p2":
                    dobble.winner = "p2"
                    print("[GAME] Player p2 won in game", game)
                if data == "winner p1":
                    dobble.winner = "p1"
                    print("[GAME] Player p1 won in game", game)

                

                if data.count("width&height") == 1:
                    print("updating width and height")
                    string = data.split(" ")
                    dobble.Width = int(string[1])
                    dobble.Height = int(string[2])

                if data.count("name") == 1:
                    print("updating name")
                    name = data.split(" ")[1:]
                    name = " ".join(name)
                    if currentId == "p2":
                        dobble.p2name = name
                    elif currentId == "p1":
                        dobble.p1name = name

                # print("Recieved doble_game from", currentId, "in game", game)

                if dobble.ready and dobble.card_pair_no ==0:
                    # print("starting game")
                    # print(dobble.Width,dobble.Height)
                    dobble.update_card()
                sendData = pickle.dumps(dobble)
                # print("Sending doble_game to player", currentId, "in game", game)

                conn.sendall(sendData)

            except Exception as e:
                print(e)
        
        connections -= 1
        try:
            del games[game]
            print("[GAME] Game", game, "ended")
        except:
            pass
        print("[DISCONNECT] Player", name, "left game", game)
        conn.close()

    # else:
    #     available_games = list(games.keys())
    #     game_ind = 0
    #     dobble = games[available_games[game_ind]]
    #     dobble.start_user = "s"
    #     data_string = pickle.dumps(dobble)
    #     conn.send(data_string)

    #     while True:
    #         available_games = list(games.keys())
    #         dobble = games[available_games[game_ind]]
    #         try:
    #             d = conn.recv(128*8*8*12)
    #             data = d.decode("utf-8")
    #             if not d:
    #                 break
    #             else:
    #                 try:
    #                     if data == "forward":
    #                         print("[SPECTATOR] Moved Games forward")
    #                         game_ind += 1
    #                         if game_ind >= len(available_games):
    #                             game_ind = 0
    #                     elif data == "back":
    #                         print("[SPECTATOR] Moved Games back")
    #                         game_ind -= 1
    #                         if game_ind < 0:
    #                             game_ind = len(available_games) -1

    #                     dobble = games[available_games[game_ind]]
    #                 except:
    #                     print("[ERROR] Invalid Game Recieved from Spectator")

    #                 sendData = pickle.dumps(dobble)
    #                 conn.sendall(sendData)

    #         except Exception as e:
    #             print(e)

    #     print("[DISCONNECT] Spectator left game", game)
    #     specs -= 1
    #     conn.close()


while True:
    read_specs()
    if connections < 6:
        conn, addr = s.accept()
        spec = False
        g = -1
        print("[CONNECT] New connection")

        for game in games.keys():
            if games[game].ready == False:
                g=game

        if g == -1:
            try:
                g = list(games.keys())[-1]+1
                games[g] = Dobble()
            except:
                g = 0
                games[g] = Dobble()

        '''if addr[0] in spectartor_ids and specs == 0:
            spec = True
            print("[SPECTATOR DATA] Games to view: ")
            print("[SPECTATOR DATA]", games.keys())
            g = 0
            specs += 1'''

        print("[DATA] Number of Connections:", connections+1)
        print("[DATA] Number of Games:", len(games))

        start_new_thread(threaded_client, (conn,g,spec))
