import socket
import threading
import os

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] Nouveau thread pour {} {}".format(self.ip, self.port,))

    def run(self):
        global rep
        print("Connexion de {} {}".format(self.ip, self.port,))
        r = self.clientsocket.recv(50000)
        r2 = (str(r))[2:-1]
        print(r2)

        if r2 == "get_list":
            os.makedirs(rep, exist_ok=True)
            lst = os.listdir('csv/')
            data = str(lst)

            self.clientsocket.send(data.encode())
        elif ".csv" in r2:
            print("Ouverture du fichier: ", r2, "...")
            fp = open(rep + r2, 'rb')
            self.clientsocket.send(fp.read())

        else:
            os.makedirs(rep, exist_ok=True)
            n = self.clientsocket.recv(50000)
            n2 = (str(n))[2:-1]
            print(n2)
            print("Ecriture dans le fichier: " + rep + n2 + "...")
            with open(rep + n2, "wb") as fp:
                fp.write(r)
                self.clientsocket.send("0".encode())

        print("Client déconnecté...")


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", 123))
rep = "csv/"
os.makedirs(rep, exist_ok=True)

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()