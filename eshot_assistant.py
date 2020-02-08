#!/usr/bin/python3
# -*- coding: utf-8 -*-

# github.com/cancakar35


"""
    TODO:
    1) Django ile web app şeklinde ayarlanacak.
    2) Fonksiyonları başka dosyaya yükleyerek modül olarak kullan. main.py içerisinde proje toparlanacak.
"""
import time
import requests
import speech_recognition as sr
from gtts import gTTS
from datetime import datetime
from bs4 import BeautifulSoup

r = sr.Recognizer()

def connect_eshot():
    dy = "week"
    if datetime.today().weekday() < 5:
        dy = "week"
    elif datetime.today().weekday() == 5:
        dy = "sat"
    else:
        dy = "sun"
    
    try:
        print("Otobüs hattını söyleyin...")
        with sr.Microphone() as src:
            audio = r.listen(src)

        x = r.recognize_google(audio, language="tr")

        print(x)


        res = requests.get("https://www.eshot.gov.tr/tr/UlasimSaatleri/{}/288".format(x))
        soup = BeautifulSoup(res.content, "html.parser")

        gzg = soup.find_all("p",{"class":"bus-direction"})[0].text.split("  ")

        print("{} -> {} (gidiş yönü)\nGidiş mi dönüş mü?: ".format(gzg[0], gzg[1]), end="\t")
        with sr.Microphone() as src:
            audio = r.listen(src)

        gd = r.recognize_google(audio, language="tr")
        print(gd)
        tm = soup.find_all("ul",{"class":"timescape"})
        times = []
        if gd == "gidiş":
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
        elif gd == "dönüş":
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
        return times
    except Exception as e:
        print(str(e))
        return []
    


def find_bus(hat=None):
    now = datetime.now().strftime("%H:%M")
    times = connect_eshot()
    for i in times:
        if i[:2] == now[:2]:
            if not int(i[3:]) < int(now[3:]):
                print(i, "\t Otobüsünüz {}dk içerisinde kalkıyor!".format(int(i[3:])-int(now[3:])))
                return
        elif int(i[:2]) == int(now[:2])+1:
            print(i,"\t Otobüsünüz {}dk içerisinde kalkıyor!".format((int(i[:2])-int(now[:2]))*60+int(i[3:])-int(now[3:])))
            return
        elif int(i[:2]) == int(now[:2])+2:
            print(i,"\t Otobüsünüz {}dk içerisinde kalkıyor!".format((int(i[:2])-int(now[:2]))*60+int(i[3:])-int(now[3:])))
            return
    for i in times:
        print(i)

def show_all(hat=None):
    times = connect_eshot()
    for i in times:
        print(i)

with sr.Microphone() as src:
    print("Sizi dinliyorum: ")
    audio = r.listen(src)

usr_snd = r.recognize_google(audio, language="tr")
print(usr_snd)
try:
    # sesten hat numarasını algılayıp fonksiyona parametre olarak gönderme ayarlanacak
    if usr_snd.lower() in ["en yakın otobüs", "yaklaşan otobüs", "acil otobüs saati", "en yakın otobüs saatleri", "bana acil otobüs bul"]:
        find_bus()
    elif usr_snd.lower() in ["otobüs saatleri"]:
        show_all()
except Exception as e:
    print(e)
