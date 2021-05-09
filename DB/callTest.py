import Getuser

access = ""
secret = ""
myKey = Getuser.Login()
access = myKey[0]
secret = myKey[1]

while True :
    Getuser.SetPerOrder()