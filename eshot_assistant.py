#!/usr/bin/env python
# -*- coding: utf-8 -*-

# github.com/cancakar35


"""
    TODO:
    1) Sesli komutla (speechrecognition) işlem alma ve gtts ile sesli cevap özelliği eklenecek.
    2) Qt Gui yapılacak.
"""

import requests
import speech_recognition as sr
import gtts
from datetime import datetime
from bs4 import BeautifulSoup

now = datetime.now().strftime("%H:%M")
dy = "week"
if datetime.today().weekday() < 5:
    dy = "week"
elif datetime.today().weekday() == 5:
    dy = "sat"
else:
    dy = "sun"

x = input("Otobüs hattı girin: ")

res = requests.get("https://www.eshot.gov.tr/tr/UlasimSaatleri/{}/288".format(x))
soup = BeautifulSoup(res.content, "html.parser")

gzg = soup.find_all("p",{"class":"bus-direction"})[0].text.split("  ")

gd = input("{} -> {} (gidiş yönü)\nGidiş/Dönüş? (Gidiş:g/Dönüş:d): ".format(gzg[0], gzg[1])).lower()

tm = soup.find_all("ul",{"class":"timescape"})
times = []
if gd == "g":
    if dy == "week":
        times = []
        for i in tm[0].findAll("li")[1:]:
            times.append(i.text.strip("\n"))
    elif dy == "sat":
        times = []
        for i in tm[2].findAll("li")[1:]:
            times.append(i.text.strip("\n"))
    elif dy == "sun":
        times = []
        for i in tm[4].findAll("li")[1:]:
            times.append(i.text.strip("\n"))
elif gd == "d":
    if dy == "week":
        times = []
        for i in tm[1].findAll("li")[1:]:
            times.append(i.text.strip("\n"))
    elif dy == "sat":
        times = []
        for i in tm[3].findAll("li")[1:]:
            times.append(i.text.strip("\n"))
    elif dy == "sun":
        times = []
        for i in tm[5].findAll("li")[1:]:
            times.append(i.text.strip("\n"))
else:
    print("Hatalı giriş")

for i in times:
    if i[:2] == now[:2]:
        if not int(i[3:]) < int(now[3:]):
            print(i, "\t Otobüsünüz {}dk içerisinde kalkıyor!".format(int(i[3:])-int(now[3:])))
            break
    elif int(i[:2]) == int(now[:2])+1:
        print(i,"\t Otobüsünüz {}dk içerisinde kalkıyor!".format((int(i[:2])-int(now[:2]))*60+int(i[3:])-int(now[3:])))
        break
