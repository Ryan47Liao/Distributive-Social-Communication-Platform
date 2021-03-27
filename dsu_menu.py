#My Mods:
from a1 import *
from a4 import * #New Profile
import time

#A3 new packages:
from DSU_Transclusion import *

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

def main_menu(prof,file_path):
    print("[Main Menu]")
    Menu_script = '''
     [Menu] 
     Press [X] to execute the corresponding commands 
    -[B]io to send (Update) your bio
    -[P]ost to enter Post Configurations
    -[Q]uit the program
                  '''
    message = ""
    print(Menu_script)
    cmd = input("Enter Cmds here:\n")
    if cmd == "Q":
        # "Quit the program"
        try:
            prof.save_profile(file_path)
            print("File Saved!")
        except:
            print("ERROR!File Fail to Save")
            pass
        return ["QUIT",prof]

    elif cmd == 'B':
        message = biomsg(input("What is your bio? "))
        prof.bio = message

    elif cmd == "P":
        OPTION_script = """
    [P]ost to post an new post
    [G]et all Posts
    [D]elete the Post by its index
    [R]eturn to return to previous section
                 """
        while True:
            option = input(OPTION_script)
            if option == "R":
                break
                
            elif option == "P":
                new_post = Post()
                trans = DSU_Transclusion()
                entry = trans.text_editor()
                new_post.setpost(entry)
                prof.add_post(new_post)
                message = postmsg(entry)
                break

            elif option == "G":
                for post in prof.get_posts():
                    print(post)
            elif option == "D":
                prof.del_post(int(input("Enter the ith index to delete the post.(Integer Only)")))
            else:
                message = ''

    return message,prof