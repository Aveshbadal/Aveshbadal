import mysql.connector
import json
import requests
import time
from selenium import webdriver
def get_latlang(LatLngAPI):
    vecapi=requests.get(LatLngAPI)
    data=vecapi.text
    prasevec=json.loads(data)
    mydtb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="Avesh@123",
      database="veichels"
    )
    c=mydtb.cursor()
    c.execute("DROP TABLE Rider")
    c.execute("CREATE TABLE Rider (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), latitude VARCHAR(255), longitude VARCHAR(255), idg int);")
    for i in range(len(prasevec)):
        x="INSERT INTO Rider (name, latitude, longitude, idg) VALUES('{vin}','{lat}','{lng}','{idf}');".format(vin=prasevec[i]['vin'] , lat=prasevec[i]['lat'] , lng=prasevec[i]['lng'] , idf=prasevec[i]['id'])
        c.execute(x)
    latlang=[]
    c.execute("SELECT latitude, longitude FROM Rider;")
    my_result=c.fetchall()
    for i in my_result:
        latlang.append(list(i))
    return latlang
def get_locationsurl(latlang):
    APIKEY="AIzaSyC_5IGc6wP7zpV6G52yCDee1bgldm9sJ5k"
    url="https://maps.googleapis.com/maps/api/staticmap?size=400x400&markers=color:blue%7Clabel:S"
    for i in latlang:
        url+="|"+str(i[0])+","+str(i[1])
    url+="|&key=AIzaSyC_5IGc6wP7zpV6G52yCDee1bgldm9sJ5k"
    return url
LatLngAPI="https://617ab003cb1efe001700ffc7.mockapi.io/vehicles"
driver = webdriver.Chrome()
while True:
    latlang=get_latlang(LatLngAPI)
    url=get_locationsurl(latlang)
    driver.get(url)
    time.sleep(5)
    driver.refresh()
driver.quit()
