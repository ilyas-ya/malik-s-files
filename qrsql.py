import cv2
import pyzbar.pyzbar as pyzbar
import numpy
import mysql.connector

#Establishing mySQL cnx
datab = mysql.connector.connect(
    host="hm407216-001.dbaas.ovh.net",
    port="35537",
    user="lastepfritdb",
    passwd="Malikadmin2020",
    database="lastepfritdb"
)
#Creating a virtual API cursor
dbcursor = datab.cursor()

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

while True:
    key = cv2.waitKey(1)
    if key == 27:
        break

    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)
    dbcursor.execute("SELECT telephone FROM client")
#    dbcursor.execute("SELECT nbre_chambres_disponibles FROM chambre_details")
    # fetch column and save to variable "dbresult"
    dbresult = dbcursor.fetchall()
    # clean data string & convert to list
    transdbresult = str(dbresult).strip('[]').replace("'", "").replace("(", "").replace(")", "").replace(",",
                                                                                                         "").split()
    print(transdbresult)

    for obj in decodedObjects:
        datastring = str(obj.data)[1:].strip('[] ').replace("'", "")
        cv2.putText(frame, str(obj.data), (50,50), font, 3, (0,0,255),3)

    if decodedObjects != []:
        print(datastring)

        if datastring in transdbresult:
            print ("I am here")
            cv2.destroyAllWindows()
        else:
            print ("who's me ?")
        break

    cv2.imshow("Frame", frame)
