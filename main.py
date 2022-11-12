import pyrebase
from pyasn1.compat.octets import null
import time
import calendar
from tqdm import tqdm

config = {
    "apiKey": "AIzaSyAx7NZxGLVxIprlcuAO_vglT0cWx9MXBJM",
    "authDomain": "pyende-81f9c.firebaseapp.com",
    "databaseURL": "gs://pyende-81f9c.appspot.com",
    "projectId": "pyende-81f9c",
    "storageBucket": "pyende-81f9c.appspot.com",
    "messagingSenderId": "82787672529",
    "appId": "1:82787672529:web:d739c74b00901d291cc0f0"
}

config2 = {
    "apiKey": "AIzaSyAx7NZxGLVxIprlcuAO_vglT0cWx9MXBJM",
    "authDomain": "pyende-81f9c.firebaseapp.com",
    "databaseURL": "https://pyende-81f9c-default-rtdb.firebaseio.com/",
    "projectId": "pyende-81f9c",
    "storageBucket": "pyende-81f9c.appspot.com",
    "messagingSenderId": "82787672529",
    "appId": "1:82787672529:web:d739c74b00901d291cc0f0"
}

firebase2 = pyrebase.initialize_app(config2)
database = firebase2.database()

current_GMT = time.gmtime()  # Get local GMT

isConnected = 0

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()

print("                                 Login\n")
print("Email: ")
email = input()
print("Password: ")
password = input()

try:
    user = auth.sign_in_with_email_and_password(email, password)
except:
    print("WRONG CREDENTIALS!" + "  program terminating...")
    exit()

if firebase != null and firebase2 != null:
    isConnected = 1

timer = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
actionType = 3  # 3 is the default value
time_stamp = calendar.timegm(current_GMT)
id_AutoIncrement = -1

if isConnected == 1:
    print("\n                            PC B: CONNECTED \n")
    print("Please choose your desired option: \n")
    print("A- Upload Encrypted file \nB- Download Encrypted file\n")
    choice = input()
    if choice == 'A' or choice == 'a':
        print("Please insert the name of the file")
        name = input()
        print("Please insert the local address of the file you want to upload: ")
        pathL = input()
        pathU = pathL
        path_local = pathU
        print("Please insert the cloud address of the file you want to upload: ")
        pathCL = input()
        path_on_cloud = pathCL
        for i in tqdm(timer):
            time.sleep(1)
        storage.child(path_on_cloud).put(path_local)
        id_AutoIncrement = id_AutoIncrement + 1
        actionType = 0
        time_stamp = calendar.timegm(current_GMT)
        data = {
            "log_id": id_AutoIncrement,
            "datetime": time_stamp,
            "action_type": actionType,
            "filename": name
        }
        database.child("logs").child("PC B").set(data)


    elif choice == 'B' or choice == 'b':
        print("Please insert the name of the file you want to download: ")
        name = input()
        print("Please insert the address of the file you want to download: ")
        pathD = input()
        path_on_cloud = pathD
        for i in tqdm(timer):
            time.sleep(1)
        storage.child(path_on_cloud).download(path_on_cloud, name)
        actionType = 1
        time_stamp = calendar.timegm(current_GMT)
        id_AutoIncrement = id_AutoIncrement + 1
        data = {
            "log_id": id_AutoIncrement,
            "datetime": time_stamp,
            "action_type": actionType,
            "filename": name
        }
        database.child("logs").child("PC B").set(data)

    else:
        print("Invalid choice.")
else:
    print("PC B: DISCONNECTED \n")
    print("CONNECTION FAILED")
