from COV19_API import  *
from OpenWeather import *

class DSU_Transclusion:
    def __init__(self):
        self.Methods = ['weather', 'covid', 'kanye']
        self.open_weather = None
        self.covid19 = None
        self.guide()

    def guide(self):
        print("""
              Use @[option] to enable Transclusion feature:
              e.g: 'Hi, in US, @covid people have recovered from covid19, great news!''
              will generate 'Hi, in US, 7243488 people have recovered from covid19, great news!''
              ____________________________________________________________________________________
              Avaliable Features:
              [weather]:provides weather info at a given location
              [covid]: provide covid info at a specific contry
              [kanye]:a random kanye quote
              ____________________________________________________________________________________
              In order to enable this feature, make sure that you make space between each word:
              e.g:
              ✅"Hi, in US, @covid people"
              ❌"Hi, in US,@covid people"
              """)

    def OPTION_detector(self, entry) -> str:
        try:
            OPTIONS = {}
            words = entry.split(' ')
            for word in words:
                if word[0] == "@":
                    opt = word.strip("@")
                    if opt in self.Methods:
                        OPTIONS[opt] = words.index(word)
                    else:
                        suggestion = search_list(opt, self.Methods)
                        if suggestion != []:
                            print("Do You mean:")
                            print(suggestion)
                        else:
                            print("Avaliable Methods:")
                            print(self.Methods)
            print("Detected Options:")
            print(OPTIONS)
            return (OPTIONS)
        except:
            return []

    def text_editor(self) -> str:
        entry = input("Enter Your message Here:")
        OPTIONS = self.OPTION_detector(entry)
        if OPTIONS == []:  # If no Options detected:
            return entry
        else:  # If options detected
            entry = entry.split(" ")
            for opt in list(OPTIONS.keys()):
                method = getattr(self, opt)
                transluded_message = method()  # Call Method
                entry[OPTIONS[opt]] = transluded_message
        new_message = STR(entry)
        print(new_message)
        Q = input("Are you sure about the message above? Press [Y] to continue, anything to revise").upper()
        if Q == "Y":
            return new_message
        else:
            print(STR(entry))
            self.text_editor()  # Continue Editing The message

    # Method weatherdescription
    def weather(self):
        print("For Weather Feat")
        OPTIONS = ['description', 'temperature', 'high_temperature', 'low_temperature', 'longitude', 'latitude',
                   'humidity', 'sunset']
        if self.open_weather is None:
            self.open_weather = OpenWeather(input("Enter your zip code here:"), "US")  # Assume The User is in USA
        try:
            if self.open_weather.status:
                while True:
                    print(OPTIONS)
                    opt = input("The above are the avaliable options for weather, which you would you like to envoke?")
                    if opt in OPTIONS:
                        break
                return getattr(self.open_weather, opt)
            else:
                print("ZIPCODE Not Supported")
                return ""
        except:
            return ""

    def covid(self):
        OPTIONS = ["confirmed", "recovered", "critical", "lastUpdate", "deaths"]
        if self.covid19 is None:
            self.covid19 = COVID19()
        self.data_by_c = self.covid19.report_by_c(input("What's Country's Name that you wish to Query?"))
        if self.data_by_c is None:
            return ""
        else:
            while True:
                print(OPTIONS)
                opt = input("The above are the avaliable options for weather, which you would you like to envoke?")
                if opt in OPTIONS:
                    break
        try:
            OUT = self.data_by_c[opt]
        except:
            print(self.data_by_c)
            OUT = ""
        return OUT

    def kanye(self):
        "Return a Random Quote By Kanye West!"
        return requests.request("GET", "https://api.kanye.rest?format=text").text

if __name__ == '__main__':
    test = DSU_Transclusion()
    test.text_editor()