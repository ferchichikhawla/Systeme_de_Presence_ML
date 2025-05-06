import os
import numpy as np
import pickle
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
from firebase_admin.storage import bucket

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://whatsap-6b581-default-rtdb.firebaseio.com/",
    'storageBucket':"whatsap-6b581.appspot.com"
})







bucket=storage.bucket()
cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

imgBackground = cv2.imread('Ressources/Background2.jpg')

#importing the mode images into a liste


folderModePath ='Ressources/Models'
modePathList =os.listdir(folderModePath)
imgModeList= []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath,path)))
#print(len(imgModeList))

#load the encoding file:
print("Loading Encoded File ")
file = open("EncodeFile.p",'rb')
encodeListWithIds =pickle.load(file)
file.close()
encodeListKnown,studentIds = encodeListWithIds
#print(studentIds)
print("Loading Encoded Loaded ")

modeType=0
Counter=0
id = -1
imgStudent = []
while True:
    success,img=cap.read()

    # Resize the image
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)

    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect face locations and compute face encodings
    faceCureFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCureFrame)

    imgBackground[162:162+480,55:55+640]=img

    imgModeResized = cv2.resize(imgModeList[modeType], (414, 633))  # Resize to match the target dimensions

    imgBackground[44:44 + 633, 808:808 + 414] = imgModeResized


    if faceCureFrame:
        # Compare encodings and compute distances
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCureFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            #print("matches:", matches)
            #print("faceDis:", faceDis)
            matchIndex = np.argmin(faceDis)
           # print("MatchIndex:", matchIndex)
            if matches[matchIndex]:
                # print("known Face Detected")
                #print(studentIds[matchIndex])
                y1,x2,y2,x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55+x1 ,162+y1,x2-x1,y2-y1
                imgBackground=cvzone.cornerRect(imgBackground,bbox,rt=0)
                id = studentIds[matchIndex]
                print(id)
        #gérer les donneés dans le base de donnée
                if Counter ==0:
                     cvzone.putTextRect(imgBackground,"loading",(275,400))
                     cv2.imshow("Face Attendance", imgBackground)
                     cv2.waitKey(1)
                     Counter=1
                     modeType=1
        if Counter != 0:

            if Counter == 1:
                #get the data
               studentInfo = db.reference(f'students/{id}').get()
               print(studentInfo)
               #Get the Images from the Storage :

               blod =bucket.get_blob(f'Images/{id}.jpg')
               array = np.frombuffer(blod.download_as_string(),np.uint8)
               imgStudent=cv2.imdecode(array,cv2.COLOR_BGR2RGB)
             # Update data of attendance
               datatimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                 "%Y-%m-%d %H:%M:%S")
               secondsElapsed= (datetime.now()-datatimeObject).total_seconds()
               print(secondsElapsed)
               if secondsElapsed >30:
                   ref = db.reference(f'students/{id}')
                   studentInfo['total_attendance']+=1
                   ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                   ref.child('total_attendance').set(studentInfo['total_attendance'])
               else:
                   modeType=3
                   Counter=0
                   imgModeResized = cv2.resize(imgModeList[modeType], (414, 633))  # Resize to match the target dimensions

                   imgBackground[44:44 + 633, 808:808 + 414] = imgModeResized

            if modeType !=3:

                if 10<Counter<20:
                    modeType=2

                imgModeResized = cv2.resize(imgModeList[modeType], (414, 633))  # Resize to match the target dimensions

                imgBackground[44:44 + 633, 808:808 + 414] = imgModeResized

                if Counter <=10:


                   #add les informations dans les items graphics
                   cv2.putText(imgBackground,str(studentInfo['total_attendance']),(861,125),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                   cv2.putText(imgBackground,str(studentInfo['major']),(1006,550),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                   cv2.putText(imgBackground,str(id),(1006,493),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                   cv2.putText(imgBackground,str(studentInfo['standing']),(910,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                   cv2.putText(imgBackground,str(studentInfo['year']),(1025,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)
                   cv2.putText(imgBackground,str(studentInfo['starting_year']),(1125,625),cv2.FONT_HERSHEY_COMPLEX,0.6,(100,100,100),1)

                   (w,h), _ =cv2.getTextSize(studentInfo['name'],cv2.FONT_HERSHEY_COMPLEX,1,1)
                   offset =(414-w)//2
                   cv2.putText(imgBackground, str(studentInfo['name']), (830+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
                   # Resize imgStudent to match the target dimensions in imgBackground
                   imgStudent = cv2.resize(imgStudent, (216, 216))

                   # Now it should fit without any issues
                   imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                Counter+=1
                if Counter>=20:
                    Counter=0
                    modeType=0
                    studentInfo=[]
                    imgStudent=[]
                    imgModeResized = cv2.resize(imgModeList[modeType], (414, 633))  # Resize to match the target dimensions

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeResized
    else:
        modeType=0
        Counter=0
    # cv2.imshow("Webcam ",img)
    cv2.imshow("Face Attendance",imgBackground)
    cv2.waitKey(1)

