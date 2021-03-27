from API_handling import *

class OpenWeather:
    def __init__(self, zipcode: str, ccode: str, apikey="36f15b789d6b73f417209f02ec902ab7"):
        """
        [Class Initialziation]
        zipcode: string, zip code of the area of interest
        ccode : string, country code
        apikey: authorized api key
        """
        self.status = False
        self.zipcode = zipcode
        self.ccode = ccode
        self.apikey = apikey
        # Get Url
        url = "https://api.openweathermap.org/data/2.5/weather?zip={0},{1}&appid={2}".format(
            self.zipcode,
            self.ccode,
            self.apikey
        )
        print(url)
        # Fetch Data
        self.weather_obj = download_url(url)
        # get attr
        self.get_attr()

    def get_attr(self):
        "Get Attributes From the fetched data"
        if self.weather_obj != None:
            # Temperature
            self.temperature = self.weather_obj['main']['temp']
            # High Temperature
            self.high_temperature = self.weather_obj['main']['temp_max']
            # Low Temperature
            self.low_temperature = self.weather_obj['main']['temp_min']
            # Coord-longitude
            self.longitude = self.weather_obj['coord']['lon']
            # Coord-Latitude
            self.latitude = self.weather_obj['coord']['lat']
            # Current Weather
            self.description = self.weather_obj['weather'][0]['description']
            # humidity
            self.humidity = self.weather_obj['main']['humidity']
            # sun_set
            self.sunset = self.weather_obj['sys']['sunset']
            # city
            self.city = self.weather_obj['name']
            self.status = True
        else:
            print("❌Failed to fetch data")
