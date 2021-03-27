import re
import requests
import  json
import urllib
from urllib import request,error

def STR(list_of_strings)->str:
    "Take a list of strings and return a string of all its elements"
    OUT = ""
    for i in list_of_strings:
        try:
            OUT += str(i) + " "
        except:
            print("ERROR:{}Failed to Concatenate".format(i))
    return OUT

def LST_UNCAP(list)->list:
    "UNCapitalize all elements in a list"
    OUT = []
    for i in list:
        try:
            OUT.append(i.lower())
        except SyntaxError:
            OUT.append(i)
        except:
            print("Syntax Error")
    return OUT

def search_list(key,list_of_keys)-> list:
    "Take in a keyword, and search through the list for ones that share the keywords"
    list_of_keys.append('temp')
    OUTPUT = []
    found = False
    cpat = re.compile(key+"\S*,")
    #First, Assume that there is no capitalization needed.
    r1 = cpat.findall(str(list_of_keys))
    for result in r1:
        item = result.strip("',")
        if item in list_of_keys:
            OUTPUT.append(item)
    if OUTPUT != []:
        found = True
    #Next, Assume that there is capitalization needed.
    if found:
        pass
    else:
        L_uncaped = LST_UNCAP(list_of_keys)
        r2 = re.findall(key.lower()+"\S*,",str(L_uncaped))
        for result in r2:
            result_low = result.strip("',")
            if result_low in L_uncaped:
                og_idx = LST_UNCAP(list_of_keys).index(result_low)
                OUTPUT.append(list_of_keys[og_idx])
    return OUTPUT

def json_to_dict(json_str) -> dict:
    """
    Take in a json string and convert it into a dictionary
    """
    DIC = {}
    for i in json_str.split(","):
        try:
            j = i.split(":")
            DIC[j[0].strip('[{"}]')] = j[1].strip('[{"}]')
        except:
            pass
    return DIC

def connected_to_internet() -> bool:
    print("Checking Internet Connection...")
    url = "https://www.bowenliao.com/"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        if request.status_code == 200:
            print("Status:✅ Connected to the Internet")
            return True
        else:
            print("Status:❌ No internet connection.")
        return False
    except (requests.ConnectionError, requests.Timeout) as exception:
        print("Status:❌ No internet connection.")
        return False


def download_url(url_to_download: str) -> dict:
    "Down Load Content of Jason format and convert it into dict from a given url"
    response = None
    r_obj = None
    timeout = 10

    # Check Internet Connection:
    if connected_to_internet():
        print("Fetching Response from URL...")
        try:
            response = urllib.request.urlopen(url_to_download)

            if response.status == 404 or response.status == 503:
                print("❌ remote API is unavailable")

            json_result = response.read()
            r_obj = json.loads(json_result)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))

        except ValueError as e:
            print("❌ Invalid URL")

        finally:
            if response != None:
                response.close()

    return r_obj