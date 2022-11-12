import pyrebase
from pyasn1.compat.octets import null
import time
import calendar
from tqdm import tqdm
from cryptography.fernet import Fernet

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


def genFKey():
    key = Fernet.generate_key()
    with open('mykey.key',
              'wb') as mykey:  # Creates encryption key using Fernet algorithm for encryption and decryption
        mykey.write(key)


def EncryptFile(path, name):
    with open('mykey.key', 'rb') as mykey:  # Reads encryption key
        key = mykey.read()
    f = Fernet(key)
    with open(path, 'rb') as original_file:
        original = original_file.read()
    encryptedFile = f.encrypt(original)
    EFName = "Encrypted " + name
    with open(EFName, 'wb') as encryptedFileFile:
        encryptedFileFile.write(encryptedFile)


def DecryptFile(path, name):
    with open('mykey.key', 'rb') as mykey:  # Reads encryption key
        key = mykey.read()
    f = Fernet(key)
    with open(path, 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
    decryptedFile = f.decrypt(encrypted)
    DEFName = "Decrypted " + name
    with open(DEFName, 'wb') as encryptedFileFile:
        encryptedFileFile.write(decryptedFile)


firebase2 = pyrebase.initialize_app(config2)
database = firebase2.database()

current_GMT = time.gmtime()  # Get local GMT

isConnected = 0

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
storage = firebase.storage()

count = database.child("logs").child("PC B").child("count").get()
countD = count.val()

for key, value in countD.items():
    countL = value

id = database.child("logs").child("PC B").child("id").get()
idD = id.val()

for key, value in idD.items():
    id_AutoIncrement = value

# countData = {
#     "count": 1
# }
# database.child("logs").child("PC B").child("count").set(countData)

# IDData = {
#     "id": 1
# }
# database.child("logs").child("PC B").child("id").set(IDData)


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

anyString = "Log "

if isConnected == 1:
    print("\n                            PC B: CONNECTED \n")
    print("Please choose your desired option: \n")
    print("A- Upload Encrypted file \nB- Download Encrypted file\nC- Exit")
    choice = input()
    if choice == 'A' or choice == 'a':
        print("Please insert the name of the file")
        name = input()
        print("Please insert the local address of the file you want to upload: ")
        pathL = input()
        pathU = pathL
        path_local = pathU
        EncryptFile(path_local, name)
        print("Please insert the cloud address of the file you want to upload: ")
        pathCL = input()
        path_on_cloud = pathCL
        for i in tqdm(timer):
            time.sleep(0.7)
        EFName = "Encrypted " + name
        storage.child(path_on_cloud).put(EFName)
        id_AutoIncrement = id_AutoIncrement + 1
        actionType = 0
        time_stamp = calendar.timegm(current_GMT)
        data = {
            "log_id": id_AutoIncrement,
            "datetime": time_stamp,
            "action_type": actionType,
            "filename": name
        }
        database.child("logs").child("PC B").child("Log " + str(countL)).set(data)
        countL = countL + 1
        database.child("logs").child("PC B").child("count").update({"count": countL})
        database.child("logs").child("PC B").child("id").update({"id": id_AutoIncrement})


    elif choice == 'B' or choice == 'b':
        print("Please insert the name of the file you want to download: ")
        name = input()
        print("Please insert the address of the file you want to download: ")
        pathD = input()
        path_on_cloud = pathD
        for i in tqdm(timer):
            time.sleep(0.5)
        storage.child(path_on_cloud).download(path_on_cloud, name)
        DecryptFile(name, name)
        actionType = 1
        time_stamp = calendar.timegm(current_GMT)
        id_AutoIncrement = id_AutoIncrement + 1
        data = {
            "log_id": id_AutoIncrement,
            "datetime": time_stamp,
            "action_type": actionType,
            "filename": name
        }
        database.child("logs").child("PC B").child("Log " + str(countL)).set(data)
        countL = countL + 1
        database.child("logs").child("PC B").child("count").update({"count": countL})
        database.child("logs").child("PC B").child("id").update({"id": id_AutoIncrement})
    elif choice == "C" or choice == "c":
        exit()

    else:
        print("Invalid choice.")

else:
    print("PC B: DISCONNECTED \n")
    print("CONNECTION FAILED")
