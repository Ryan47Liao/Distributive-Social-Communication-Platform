# Covid 19 API
from API_handling import *
import numpy as np
import pandas as pd

class COVID19:
    def __init__(self, api_key="c2c1339702msh2b30e056ce2f94ep1d6a83jsne47095d65bf8"):
        self.headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }
        self.get_countries()

    def get_countries(self):
        "Collect a list of countries avaliable to search for"
        url = "https://covid-19-data.p.rapidapi.com/help/countries"
        response = requests.request("GET", url, headers=self.headers)
        n = len(response.text.split("},{"))
        columns = ['name', 'alpha2code', 'alpha3code', 'latitude', 'longitude']
        L = np.array([columns])
        count = 0
        try:
            for i in range(n):
                temp = response.text.split("},{")[i].split(',')
                L1 = []
                try:
                    for j in temp:
                        L1.append(j.split(":")[1].strip('"'))
                    L1 = np.array([L1])
                    L = np.concatenate((L, L1), axis=0)
                    count += 1
                except:
                    pass
        except IndexError:
            print(temp)
        index = [f'{num}' for num in range(count)]
        self.countries = pd.DataFrame(L[1:, :], columns=columns, index=index)

    def country_rec(self, entry):
        "Recommend option Based on Entry"
        alternatives = list(self.countries['name'])
        return search_list(entry, alternatives)

    def report_by_c(self, country_name: str):
        url = "https://covid-19-data.p.rapidapi.com/country"
        if country_name in list(self.countries['name']):
            pass
        else:
            print("Name ERROR. Avaliable Country Names:")
            print(self.country_rec(country_name))
            country_name = input("Please enter the Correct name of the Country that you wish to QUERY:")

        querystring = {"name": country_name}
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        self.data_by_c = json_to_dict(response.text)
        return (self.data_by_c)
