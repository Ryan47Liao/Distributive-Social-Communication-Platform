#My Mods:
from a4 import *
from dsu_login import Log_In
from dsu_menu import main_menu
from API_handling import *

#Other Packages
import asyncio, time
import websockets
import pathlib
import nest_asyncio

async def DSU_online():
    global prof
    global file_path
    #http://168.235.86.101:9997/
    uri = "ws://168.235.86.101:9997/ws"
    prof = NaClProfile(uri)
    Parent = pathlib.Path("D:/DSU/dsu_saves/").mkdir(parents=True, exist_ok=True) #Create the Folder for saving
    parent_address = "D:/DSU/dsu_saves/"
    message = ""
    #Initialization Complete
    async with websockets.connect(uri) as websocket:
        #Pre Login
        if True:
            # Log_In
            message, file_path, prof = Log_In(uri,parent_address,prof)
            if message == "QUIT":
                pass
            else:
                await websocket.send(message)
                print(f"> {message}")

                response = await websocket.recv()
                #Get the public Key:
                dsu_pk = get_pk(response)
                if dsu_pk is None:
                    pass
                else:
                    prof.get_public_key(dsu_pk)
                print(f"< {response}")

            # Main Menu
        while True:
                if message == "QUIT":
                    print("Good Bye!")
                    break
                else:
                    message,prof = main_menu(prof,file_path)
                    await websocket.send(message)
                    print(f"> {message}")

                    response = await websocket.recv()
                    print(f"< {response}")

def DSU_main():
    if True:
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(DSU_online())
            

