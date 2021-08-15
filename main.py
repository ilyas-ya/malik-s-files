import cv2
import pyzbar.pyzbar as pyzbar
import numpy
import mysql.connector
from guizero import App, TextBox, PushButton, Text, Box
import time

app = App(width=800, height=680, bg="white")

# Establishing mySQL cnx
datab = mysql.connector.connect(
    host="hm407216-001.dbaas.ovh.net",
    port="35537",
    user="lastepfritdb",
    passwd="Malikadmin2020",
    database="lastepfritdb"
)
# Creating a virtual API cursor
dbcursor = datab.cursor()
datastring = str()
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN
print("programme start")


def camture():
    global datastring
    datastring = ""
    while True:

        key = cv2.waitKey(1)
        if key == 27:
            cv2.destroyAllWindows()
            break

        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)
        dbcursor.execute("SELECT telephone FROM client")
        #   dbcursor.execute("SELECT nbre_chambres_disponibles FROM chambre_details")
        # fetch column and save to variable "dbresult"
        dbresult = dbcursor.fetchall()
        # clean data string & convert to list
        transdbresult = str(dbresult).strip('[]').replace("'", "").replace("(", "").replace(")", "").replace(",",
                                                                                                             "").split()
        # print(transdbresult)

        for obj in decodedObjects:
            datastring = str(obj.data)[1:].strip('[] ').replace("'", "")
            cv2.putText(frame, str(obj.data), (50, 50), font, 3, (0, 0, 255), 3)

        if decodedObjects != []:

            if datastring in transdbresult:
                print("Datastring value : ", datastring)
                decodedObjects = pyzbar.decode(frame)
                datastring = ""
                print(decodedObjects)
                print(datastring)
                cv2.destroyAllWindows()
                time.sleep(2)
                username.value = datastring
                # write_card()
                break

            else:
                print("who's me ?")
                cv2.destroyAllWindows()
                time.sleep(2)
                username.value = "Vous n'êtes malheureusement pas dans notre base de donnée, merci de vérifier votre réservation"
            break

        cv2.imshow("Frame", frame)


def write_card():
    while True:
        global datastring
        instruction.value = "En attente d'une carte"
        print("Now place your tag to write")
        print("Written")
        valcheck = Text(body, text="Merci, veuillez récupérer votre carte")
        break


def read_card():
    print("card check")


# UI Content starts here
hello = Text(app, text="Bonjour")
label = Text(app, "Placez votre carte sur le lecteur, puis scanner votre QR-code")
name = Text(app)
body = Box(app, height="fill")
valider = PushButton(body, text="valider", command=camture)
cardvalue = Text(app, text=datastring)
checkbutton = PushButton(app, text="vérifier carte", command=read_card)
instruction = Text(body, text="")
username = Text(body, text="")

app.display()





