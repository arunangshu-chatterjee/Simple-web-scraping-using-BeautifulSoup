__author__     = "Arunangshu Chatterjee"
import requests
import pandas
from bs4 import BeautifulSoup


r = requests.get("http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c = r.content

soup = BeautifulSoup(c, "html.parser")

all = soup.find_all("div", {"class":"propertyRow"}) # These details can be found when we inspect a webpage

all[0].find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")

pages = soup.find_all("a",{"class":"Page"})[-1].text # Grabs the last page number


l = []
base_url = "http://www.pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
for page in range(0, int(pages) * 10, 10):
    print(base_url + str(page) +  ".html")
    r = requests.get(base_url + str(page) + ".html")
    c = r.content
    soup = BeautifulSoup(c, "html.parser")
    all = soup.find_all("div", {"class":"propertyRow"})                                       # These details can be found when we inspect a webpage
    for item in all:
        d = {}
        d["Address"] = item.find_all("span", {"class":"propAddressCollapse"})[0].text
        try:
            d["Locality"] = item.find_all("span", {"class":"propAddressCollapse"})[1].text
        except:
            d["Locality"] = None
        d["Price"] = item.find("h4", {"class":"propPrice"}).text.replace("\n","").replace(" ","")

        try:
            d["Beds"] = item.find("span", {"class":"infoBed"}).find("b").text                 # Stores the number of beds
        except:
            d["Beds"] = None
        try:
            d["Area"] = item.find("span", {"class":"infoSqFt"}).find("b").text                # Stores the square feet area
        except:
            d["Area"] = None
        try:
            d["Full Baths"] = item.find("span", {"class":"infoValueFullBath"}).find("b").text # Stores the number of full baths
        except:
            d["Full Baths"] = None
        try:
            d["Half Baths"] = item.find("span", {"class":"infoValueHalfBath"}).find("b").text # Stores the number of half baths
        except:
            d["Half Baths"] = None

        for column_group in item.find_all("div", {"class":"columnGroup"}):                    # Iterate to get the lot size parameter
            for feature_group, feature_name in zip(column_group.find_all("span", {"class":"featureGroup"}),column_group.find_all("span", {"class":"featureName"})):
                print(feature_group.text, feature_name.text)
                if "Lot Size" in feature_group.text:
                    d["Lot Size"] = feature_name.text
        l.append(d)
df = pandas.DataFrame(l)
df.to_csv("Output.csv")