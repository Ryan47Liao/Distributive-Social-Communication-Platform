#@title A2/DSU_Login {display-mode: "form"}
#Last Edit: 2020/11/27
from a1 import *
from a4 import * #NaClProfile

#@title Other Mod {display-mode: "form"}
def joinmsg(username, pwd):
    msg = '{"join": {"username":"'+username+'", "password":"'+pwd+'"}}'
    return msg

def biomsg(msg):
    msg = '{"bio": {"entry":"'+msg+'", "timestamp":"'+str(time.time())+'"}}'
    return msg

def postmsg(msg):
    msg = '{"post": {"entry":"'+msg+'", "timestamp":"'+str(time.time())+'"}}'
    return msg


def Log_In(uri,parent_address,prof):
    print("[LogIn Interface]")
    while True:
        cmd = input("""
    Press [X] to execute the corresponding commands 
    -[C]reate an Account
    -[L]oad an pre-existing DSU file to LogIn
    -[Q]uit to quit the program
                       """)
        if cmd == "C":
            User_Name = input("User Name:")
            temp = ""
            for i in User_Name.split(" "):
                temp += i + "_"
                User_Name = temp[0:-1]
                check_existance = 'L ' + parent_address + ' -r -s ' + "{}_user_file.dsu".format(User_Name)
            if File_Exp(check_existance,RETURN=True) != [] :
                print("ERROR! Name already token, please register with another name!")
                continue
            else:
                pass # Name avaliable
            prof = NaClProfile(uri,User_Name)
            prof.bio = input("Leave a Bio!Tell us more about yourself!")
            try:
                file_name = "{}_user_file".format(User_Name)
                entry = "C {} -n {}".format(parent_address,file_name)
                file_path = File_Exp(entry,RETURN= True)
                print("file_path:",file_path)
                prof.save_profile(file_path) #Dump the information into the file
            except:
                print("Error,fail to create account")
        elif cmd == "L":
            User_Name = input("Please Enter Your Account Name")
            temp = ""
            for i in User_Name.split(" "):
                temp += i + "_"
                User_Name = temp[0:-1]
                file_name = User_Name + "_user_file.dsu"
                entry = 'L ' + parent_address + ' -r -s ' + file_name
                try:
                    file_path = File_Exp(entry,True)[0]
                except IndexError:
                    print("Error,file not found.")
                    continue
                prof.load_profile(file_path)
                message = joinmsg(prof.private_key,prof.public_key)
                print(prof.get_posts())
                print("Welcome!!!")
                return message, file_path, prof
        elif cmd == "Q":
            return ("QUIT","QUIT",prof)
        else:
            print("Please LogIn First!")
