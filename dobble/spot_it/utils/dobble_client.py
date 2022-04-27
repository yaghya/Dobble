import socket
import pickle
import time

# from matplotlib.pyplot import bar_label

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "ec2-3-111-146-4.ap-south-1.compute.amazonaws.com"
        self.port = 8000
        self.addr = (self.host, self.port)
        print(self.addr)
        data_string = self.connect()
        data_string =b"".join(data_string)
        # print("recieved",data_string,len(data_string))
        self.dobble = pickle.loads(data_string)
        print("dobble")

    def connect(self):
        self.client.connect(self.addr)
        self.client.settimeout(0.2)
        print("trying to receive")
        data = []
        while True:
            print("getting_packet")
            try :
                packet =self.client.recv(4*4096)
                print("packet",len(packet))
                if not packet: break
                data.append(packet)
            except Exception as e:
                print(e)
                break
        self.client.settimeout(None)
        return data

    def disconnect(self):
        self.client.close()

    def send(self, data, pick=True):
        """
        :param data: str
        :return: str
        """
        start_time = time.time()
        while time.time() - start_time <8:
            try:
                if pick:
                    # print(data)
                    self.client.send(pickle.dumps(data))
                else:
                    self.client.send(str.encode(data))
                reply = []
                self.client.settimeout(0.2)
                # i=0
                while True:
                    try :
                        # print(i)
                        packet =self.client.recv(4*4096)
                        print("packet",len(packet))
                        if not packet: 
                            print("no packet receieved")
                            break
                        reply.append(packet)
                        # i+=1
                        # if len(packet)<4096:
                        #     break
                    except Exception as e:
                        print(e)
                        break
                self.client.settimeout(None)
                reply =b"".join(reply)
                try:
                    reply = pickle.loads(reply)
                    break
                except Exception as e:
                    print(e)

            except socket.error as e:
                print(e)


        return reply


