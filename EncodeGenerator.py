import cv2
import face_recognition
import  pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from firebase_admin.storage import bucket

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://whatsap-6b581-default-rtdb.firebaseio.com/",
    'storageBucket':"whatsap-6b581.appspot.com"
})

#importing student Images
folderPath ='Images'
PathList =os.listdir(folderPath)
print(PathList)
imgList= []

studentIds = []
for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIds.append(os.path.splitext(path)[0])

    #Add images to storage to database :
    filaName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob = bucket.blob(filaName)
    blob.upload_from_filename(filaName)




    #print(path)
    #print(os.path.splitext(path)[0])
print(studentIds)

def FindEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
print("Encoding Started.....")

encodeListKnown = FindEncodings(imgList)
encodeListWithIds=[encodeListKnown,studentIds]
print("Encoding complete")
file=open('EncodeFile.p','wb')
pickle.dump(encodeListWithIds, file)
file.close()
print("File saved ")
