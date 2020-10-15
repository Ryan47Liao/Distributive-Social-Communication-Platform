from pathlib import Path

## When The CMD == 'L'
# When option is equal to "-f"
def file_only_Return(all_object_names):
    "【Purpose】Return a string containing the names of all files in a directory\n【Input】Path of the Directory\n【Output】a string containing the names of all files in this directory"
    all_object_names = all_object_names.split("\n")
    OUTPUT = ""
    for path in all_object_names:
        if Path(path).is_dir():
            pass
        else:
            OUTPUT += "\n" +path 
    return OUTPUT[1:len(OUTPUT)]

# When option is equal to "-r"
def filename_Return(dir_path,show_all = False,):
    "【Purpose】Return all files in a directory including all subdirectories and its files\n【Input】Path of the Directory,Optional:show all folders \n【Output】a string containing the names of all files and folders"
    OUTPUT = ""
    p = Path(dir_path) 
    #Return all the NONE Dir first
    for object in p.iterdir():
        if object.is_dir():
            pass
        else:
            OUTPUT += "\n"+ (str(object))
    #Now that all files in the destination are already returned
    for object in p.iterdir():
        if object.is_dir():
            sub_foo_path = str(object)
            OUTPUT += "\n"+(sub_foo_path)
            if show_all:
                OUTPUT += "\n" + (filename_Return(sub_foo_path))
        else:
            pass #Already Returned
    
    return OUTPUT[1:len(OUTPUT)]

# When option is equal to "-r" "-s"
def file_search_byName(file_name,all_object_names):
    "【Purpose】Search the directory by name Recursivelly\n【Input】all_object_names,\n【Output】the directories of the files that matched the file_name"
    all_object_names = all_object_names.split("\n")
    OUTPUT = ""
    for path in all_object_names:
        if path.split("\\")[-1] == file_name:
            OUTPUT += "\n" +path 
    return OUTPUT[1:len(OUTPUT)]

# When option is equal to "-r" "-e"
def file_search_bySuffix (file_suffix,all_object_names):
    "【Purpose】Search the directory by Suffix Recursivelly\n【Input】all_object_names,\n【Output】the directories of the files that matched the file_name"
    all_object_names = all_object_names.split("\n")
    OUTPUT = ""
    for path in all_object_names:
        try:
            if path.split("\\")[-1].split(".")[1] == file_suffix:
                OUTPUT += "\n" +path
        except:
            pass
            
    return OUTPUT[1:len(OUTPUT)]

## When the CMD == "C"
# Create a file with name -n xxx
def file_add(dir_path,file_name):
    "Add a file at designated file path"
    file_name += '.dsu'
    p = Path(dir_path)
    f = p / file_name
    if not f.exists():
        w = f.open("w")
        w.close()
    print(f)
## When the CMD == "D"
# Delete a the file at designated file path
def file_delete(file_path):
    "Delete a file at designated file path"
    if file_path == "":
        return 
    if file_path.split("\\")[-1].split(".")[-1] == "dsu":
        f = Path(file_path)
        Path.unlink(f)
        print(file_path+" DELETED")
        return
    else:
        file_path_revised = input("ERROR")
        file_delete (file_path_revised)   
## When the CMD == 'R':
# Read the file 
def file_read(file_path):
    "Read a file"
    try:
        if file_path == "":
            return 
        if file_path.split("\\")[-1].split(".")[-1] == "dsu":
            f = Path(file_path)
            r = f.open('r')
            LINES = r.readlines()
            if LINES == []:
                print("EMPTY")
            else:
                for line in LINES:
                    print (line.strip("\n"))
            r.close()
            return
        else:
            print("ERROR")
    except FileNotFoundError as fnfe:
        file_path_revised = input("ERROR")
        file_read (file_path_revised)  

# File Explore Shell
def File_Exp(entry = None,test_mod = False):
    "This is a 'Shell' for the program which takes cmd inputs from the user and directs to corresponding functions"
    while True:
        entry = input()
        if entry == "Q":
            break
        try:
            entry = entry.split(" ")
            # Collect Cmd Info
            cmd = entry[0]
            INPUT1 = entry[1]
            INPUT2 = entry[-1]
            OPTION = []
            for item in entry: 
                    if item[0] == "-":
                        OPTION.append(item)
            PASS = True
        except:
            print("ERROR")
            PASS = False
        
        if PASS:
            try:
                # Functions
                if cmd == "L":
                    dir_path = INPUT1
                    file_path = entry[1]
                    all_object_names =  result = filename_Return(dir_path)
                    for opt in OPTION:
                        if opt == "-f":#-f Output only files, excluding directories in the results.
                            all_object_names= result = file_only_Return(all_object_names)
                        elif opt == "-r": #-r Output directory content recursively.
                            all_object_names = result = filename_Return(dir_path,show_all = True)  
                        elif opt == "-s":#-s Output only files that match a given file name.
                            file_name = INPUT2
                            result = file_search_byName(file_name,all_object_names)
                        elif opt == "-e":#-e Output only files that match a give file extension.
                            file_suffix = INPUT2
                            result = file_search_bySuffix(file_suffix,all_object_names)
                    print(result)#Finally
                elif cmd == "C":
                    dir_path = INPUT1
                    opt = OPTION[0]
                    if opt == "-n":
                        file_name = INPUT2
                    file_add(dir_path,file_name)
                elif cmd == "D":
                    file_path = INPUT1
                    file_delete(file_path)
                elif cmd == "R":
                    file_path = INPUT1
                    file_read(file_path)
            except:
                print("ERROR")
            
        #Finally 
        if test_mod:
                break
    
        
# Testing Mod
TEST = {}
#Part 1
TEST["test0"] = "Q"
TEST["test1"] = "L C:\\Test"
TEST["test2"] = "L C:\\Test -r"
TEST["test3"] = "L C:\\Test -f"
TEST["test4"] = "L C:\\Test -r -s file1-2-1.txt"
TEST["test5"] = "L C:\\Test -s file1-2-1.txt"
TEST["test6"] = "L C:\\Test -r -e txt"
TEST["test7"] = "L C:\\Test -e txt"
#Part 2
TEST["test8"] = "C C:\\Test\\foo2\\foo2-1 -n LeonidasLiao"
TEST["test9"] = "R C:\\Test\\foo2\\foo2-1\\LeonidasLiao.dsu"
TEST["test10"] = "D C:\\Test\\foo2\\foo2-1\\LeonidasLiao.dsu"

def a1_test(TEST):
    "Test a series of cmds, captured in TEST dictionary"
    for test in TEST.keys():
        entry = TEST[test]
        print(test,end = " ") #Which test 
        print("entry【{}】\n".format(entry))#What was the test entry
        File_Exp(entry,test_mod = True)
        print("✅")

File_Exp()    
