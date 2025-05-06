import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


#connect database:
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://whatsap-6b581-default-rtdb.firebaseio.com/"
})
#create table:
ref = db.reference('students')
#add items :
data = {
    "125656": {
        "name": "Mohammed guessmi",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 6,
        "standing": "G",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    }, "741536": {
        "name": "elon musk",
        "major": "Robotics",
        "starting_year": 2017,
        "total_attendance": 15,
        "standing": "A",
        "year": 4,
        "last_attendance_time": "2022-12-11 00:54:34"
    }, "8645115": {
        "name": "Emna Trabelsi",
        "major": "Economics",
        "starting_year": 2020,
        "total_attendance": 12,
        "standing": "B",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    },"2001": {
        "name": "khawla Ferchichi",
        "major": "Informatic",
        "starting_year": 2022,
        "total_attendance": 1,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    },"20011": {
        "name": "Ameur  Bouagila",
        "major": "ING-A2-01",
        "starting_year": 2024,
        "total_attendance": 1,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    },"20012": {
        "name": "Fatma Abbassi ",
        "major": "ING-A2-01",
        "starting_year": 2024,
        "total_attendance": 1,
        "standing": "A",
        "year": 2,
        "last_attendance_time": "2022-12-11 00:54:34"
    }
}
for key,value in data.items():
    ref.child(key).set(value)

