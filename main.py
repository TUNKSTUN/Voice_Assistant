from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton,  MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog
from kivy.app import App
from kivy.core.window import Window


from helpers import query_helper, toolbar_helper, questions_img_I_I, questions_img_I_II, questions_img_II_I, \
    questions_img_II_II, questions_img_III_I, questions_img_III_II
from firebase import Firebase

import sys
import subprocess
from threading import Timer

import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import requests
import yfinance as yf
import wolframalpha
import translators as ts
import time
import wikipedia
import webbrowser
from datetime import datetime


# # coding section

# crypto API (from binance)
crypto_api_bitcoin = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
crypto_api_ethereum = "https://api.binance.com/api/v3/ticker/price?symbol=ETHBUSD"
crypto_api_dogecoin = "https://api.binance.com/api/v3/ticker/price?symbol=DOGEBUSD"
crypto_api_cardano = "https://api.binance.com/api/v3/ticker/price?symbol=ADABUSD"
crypto_api_XRP = "https://api.binance.com/api/v3/ticker/price?symbol=XRPBUSD"
crypto_api_binancecoin = "https://api.binance.com/api/v3/ticker/price?symbol=BNBBUSD"
crypto_api_litecoin = "https://api.binance.com/api/v3/ticker/price?symbol=LTCBUSD"
crypto_api_solana = "https://api.binance.com/api/v3/ticker/price?symbol=SOLBUSD"

# wolfram alpha API
wolfram_alpha_api = "6QY9X3-HT9G87EVKE"

# jokes API
joke_api = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=religious,racist,sexist,explicit&type=twopart"

# news API
news_api = "59277cccaa8747d0bf618e2a73640776"

# weather API (from weatherstack)
weather_api_key = "cc4941115cdb796fbe49a6853db8d41b"

# map API (from MapQuest)
distance_api = "5kz8LN08BnmDCzGGhJrNfGaNyjc6mO9f"

# # functions


# wolframalpha
def wolfram_alpha_country_capital(text):
    client = wolframalpha.Client(wolfram_alpha_api)
    result = client.query(text)
    answer = next(result.results).text
    answer_split = answer.split()
    capital_result = f"the capital of {answer_split[-1]} is {answer_split[0]}"
    print(capital_result)
    alisa_talk(capital_result)


def wolfram_alpha_calculator(text):
    try:
        text = text.replace("power", "^")
        client = wolframalpha.Client(wolfram_alpha_api)
        result = client.query(text)
        answer = next(result.results).text
        print(answer)
        alisa_talk(f"the result is {answer}")
    except StopIteration as e:
        alisa_talk("invalid expression, please try saying that again")
        text = alisa_listen()
        if text == "":
            alisa_talk("can i help you with anything else?")
            return
        wolfram_alpha_calculator(text)


def wolfram_alpha_president(text):
    client = wolframalpha.Client(wolfram_alpha_api)
    result = client.query(text)
    answer = next(result.results).text
    print(text)
    print(answer)
    alisa_talk(f"the president is, {answer}")


def wolfram_alpha_airport(text):
    try:
        client = wolframalpha.Client(wolfram_alpha_api)
        result = client.query(text)
        answer = next(result.results).text
        print(answer)
        alisa_talk(answer)
    except StopIteration:
        alisa_talk("data not available")


# translator
def translator_japanese(text):
    text = text.replace("translate", "")
    text = text.replace("japanese", "")
    text = text.replace("to", "")
    text = text.replace("in", "")
    final_text = ts.google(text, from_language="en", to_language="ja")
    print(final_text)
    alisa_talk_ja(final_text)


def translator_hindi(text):
    text = text.replace("translate", "")
    text = text.replace("hindi", "")
    text = text.replace("to", "")
    text = text.replace("in", "")
    final_text = ts.google(text, from_language="en", to_language="hi")
    print(final_text)
    alisa_talk_hi(final_text)


def translator_telugu(text):
    text = text.replace("translate", "")
    text = text.replace("telugu", "")
    text = text.replace("to", "")
    text = text.replace("in", "")
    final_text = ts.google(text, from_language="en", to_language="te")
    print(final_text)
    alisa_talk_te(final_text)


# jokes
def jokes_fun():
    response = requests.get(joke_api)
    jokes_data = response.json()
    part_one = jokes_data["setup"]
    print(part_one)
    alisa_talk(part_one)
    time.sleep(1)
    part_two = jokes_data["delivery"]
    print(part_two)

    dialog = MDDialog(
        text=f"• {part_one}\n• {part_two}",
        radius=[50, 20, 50, 20]
    )
    dialog.open()

    alisa_talk(part_two)


# news
def get_news():
    response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=" + news_api)

    news_data = response.json()
    articles = news_data["articles"]

    news_headlines = []
    for article in articles:
        news_headlines.append(article["title"])

    for i in range(3):
        dialog = MDDialog(
            text="".join(news_headlines[i]),
            radius=[50, 20, 50, 20]
        )
        dialog.open()

        print(news_headlines[i])
        alisa_talk(news_headlines[i])


# weather
def get_temperature(location):
    try:
        response = requests.get(url=f"http://api.weatherstack.com/current?access_key={weather_api_key}&query={location}")
        weather_data = response.json()

        temperature = weather_data["current"]["temperature"]
        country = weather_data["location"]["country"]
        print(location)
        print(temperature)
        alisa_talk(f"currently at {location}, {country}, its {temperature} degrees celsius")
    except KeyError:
        alisa_talk("sorry, invalid location, can you try to say that again?")
        weather_input = alisa_listen()
        if "" in weather_input or " " in weather_input or "stop" in weather_input or "no" in weather_input or "ok" in\
        weather_input:
            alisa_talk("sure, can i help you with anything else?")
            return
        get_temperature(weather_input)


def get_weather(location):
    try:
        response = requests.get(url=f"http://api.weatherstack.com/current?access_key={weather_api_key}&query={location}")
        weather_data = response.json()
        print(weather_data)

        temperature = weather_data["current"]["temperature"]
        description = weather_data["current"]["weather_descriptions"]
        print(location)
        print(temperature)
        print(description)
        alisa_talk(f"its {temperature} degrees celsius and {description}")
    except KeyError:
        alisa_talk("sorry, invalid location, can you try saying that again?")
        weather_input = alisa_listen()
        if "" in weather_input or " " in weather_input or "stop" in weather_input or "no" in weather_input or "ok" in\
        weather_input:
            alisa_talk("sure, can i help you with anything else?")
            return
        get_temperature(weather_input)


# distance
def distance_info(from_location, to_location):
    if from_location != "" or to_location != "":
        try:
            response = requests.get(f"https://www.mapquestapi.com/directions/v2/route?key={distance_api}&from={from_location}&to={to_location}&unit=k")
            data = response.json()

            distance_data = data["route"]["distance"]
            print(distance_data)

            dialog = MDDialog(
                text=f"• {from_location} - {to_location} \n • {distance_data} km",
                radius=[50, 20, 50, 20]
            )
            dialog.open()

            alisa_talk(f"the distance between {from_location} and {to_location} is, {distance_data} kilometers")
        except KeyError:
            alisa_talk("sorry, invalid location, what is the starting point")
            from_location = alisa_listen()
            alisa_talk("what is your destination point")
            to_location = alisa_listen()
            if "stop" in from_location or "no" in from_location or "ok" in from_location:  # "by"/"buy"
                alisa_talk("sure, can i help you with anything else?")
                return
            elif "stop" in to_location or "no" in to_location or "ok" in to_location:  # "by"/"buy"
                alisa_talk("sure, can i help you with anything else?")
                return
            distance_info(from_location, to_location)
    else:
        alisa_talk("sorry, invalid location")


# wikipedia
# def wikipedia_search(text):
#     try:
#         wiki_result = wikipedia.summary(text, sentences=1)
#
#         dialog = MDDialog(
#             text=f"• {wiki_result}",
#             radius=[50, 20, 50, 20]
#         )
#         dialog.open()
#
#         print(wiki_result)
#         alisa_talk(wiki_result)
#     except IndexError:
#         alisa_talk("data not available")
#     except wikipedia.exceptions.PageError:
#         alisa_talk("data not available")


def google_search(text):
    try:
        response = requests.get(url=f"https://serpapi.com/search.json?engine=google&q={text}&api_key=00b3892d1210b4ad5a5639353769972585e1fa4e08ca0625cc222942842a9804")

        search_data = response.json()
        data = search_data["answer_box"]["snippet"]

        dialog = MDDialog(
            text=f"• {data}",
            radius=[50, 20, 50, 20]
        )
        dialog.open()

        print(data)
        alisa_talk(data)
    except KeyError:
        try:
            response = requests.get(url=f"https://serpapi.com/search.json?engine=google&q={text}&api_key=00b3892d1210b4ad5"
            f"a5639353769972585e1fa4e08ca0625cc222942842a9804")

            search_data = response.json()
            data = search_data["organic_results"][1]["snippet"]

            dialog = MDDialog(
                text=f"• {data}",
                radius=[50, 20, 50, 20]
            )
            dialog.open()

            print(data)
            alisa_talk(data)
        except KeyError:
            alisa_talk("data not available")


# opening websites and apps
def open_youtube():
    alisa_talk("sure, opening youtube")
    webbrowser.open("www.youtube.com")


def open_gmail():
    alisa_talk("sure, opening gmail")
    webbrowser.open("www.gmail.com")


def open_googledrive():
    alisa_talk("sure, opening google drive")
    webbrowser.open("www.drive.google.com")


def open_googlemaps():
    alisa_talk("sure, opening google maps")
    webbrowser.open("www.googlemaps.com")


# opening applications
def open_chrome():
    alisa_talk("sure, opening google chrome")
    os.system("start chrome")


def open_notepad():
    alisa_talk("sure, opening notepad")
    os.system("Notepad")


def open_cmd():
    alisa_talk("sure, opening command prompt")
    os.system("start cmd")


def time_now():
    now = datetime.now()
    hour = now.strftime('%I')
    minutes = now.strftime('%M')
    meridian = now.strftime('%p')
    alisa_talk(f"the time is {hour}:{minutes} {meridian}")


def current_weekday():
    now = datetime.now()
    weekday = now.strftime('%A')
    alisa_talk(f"its, {weekday}")


def alisa_listen():
    listener = sr.Recognizer()

    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        print(listener.energy_threshold)
        print("listening ...")
        audio = listener.listen(source)
        text = ""

        try:
            # using google API to recognize audio
            text = listener.recognize_google(audio)

        except sr.RequestError as re:
            print(re)
        except sr.UnknownValueError as uve:
            print(uve)
        except sr.WaitTimeoutError as wte:
            print(wte)

        text = text.lower()
        return text


def alisa_talk(text):
    # creating a new file
    new_file = "audio.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(new_file)

    playsound.playsound(new_file)
    os.remove(new_file)


def alisa_talk_ja(text):
    # creating a new file
    new_file = "audio.mp3"

    tts = gTTS(text=text, lang="ja")
    tts.save(new_file)

    playsound.playsound(new_file)
    os.remove(new_file)


def alisa_talk_hi(text):
    # creating a new file
    new_file = "audio.mp3"

    tts = gTTS(text=text, lang="hi")
    tts.save(new_file)

    playsound.playsound(new_file)
    os.remove(new_file)


def alisa_talk_te(text):
    # creating a new file
    new_file = "audio.mp3"

    tts = gTTS(text=text, lang="te")
    tts.save(new_file)

    playsound.playsound(new_file)
    os.remove(new_file)


def alisa_reply(text):
    # # Cryptocurrency prices - bitcoin

    if "bitcoin" in text:
        response = requests.get(url=crypto_api_bitcoin)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of bitcoin is, {bitcoin_price} dollars")

    elif "ethereum" in text:
        response = requests.get(url=crypto_api_ethereum)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of ethereum is, {bitcoin_price} dollars")

    elif "cardano" in text:
        response = requests.get(url=crypto_api_cardano)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of cardano is, {bitcoin_price} dollars")

    elif "dogecoin" in text:
        response = requests.get(url=crypto_api_dogecoin)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of dogecoin is, {bitcoin_price} dollars")

    elif "xrp" in text:
        response = requests.get(url=crypto_api_XRP)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of xrp is, {bitcoin_price} dollars")

    elif "binance" in text:
        response = requests.get(url=crypto_api_binancecoin)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of binance is, {bitcoin_price} dollars")

    elif "litecoin" in text:
        response = requests.get(url=crypto_api_litecoin)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of litecoin is, {bitcoin_price} dollars")

    elif "solana" in text:
        response = requests.get(url=crypto_api_solana)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of solana is, {bitcoin_price} dollars")

    # # Stocks - Apple/amazon/tesla

    elif "reliance" in text and "stock" in text:
        reliance = yf.Ticker("RELIANCE.NS")
        price = reliance.info['regularMarketPrice']
        print(price)

        alisa_talk(f"currently you can purchase reliance share for, {price} US dollars")

    elif ("tata" in text or "tcs" in text) and "stock" in text:
        reliance = yf.Ticker("TCS.NS")
        price = reliance.info['regularMarketPrice']
        print(price)

        alisa_talk(f"currently you can purchase tata share for, {price} US dollars")

    elif "wipro" in text and "stock" in text:
        reliance = yf.Ticker("WIPRO.NS")
        price = reliance.info['regularMarketPrice']
        print(price)

        alisa_talk(f"currently you can purchase wipro share for, {price} US dollars")

    elif "apple" in text and "stock" in text:
        apple = yf.Ticker("AAPL")
        apple_stock_price = apple.info['regularMarketPrice']
        print(apple_stock_price)

        alisa_talk(f"currently you can purchase apple share for, {apple_stock_price} US dollars")

    elif "amazon" in text and "stock" in text:
        amazon = yf.Ticker("AMZN")
        amazon_stock_price = amazon.info['regularMarketPrice']
        print(amazon_stock_price)

        alisa_talk(f"currently you can purchase amazon share for, {amazon_stock_price} US dollars")

    elif "tesla" in text and "stock" in text:
        tesla = yf.Ticker("TSLA")
        tesla_stock_price = tesla.info['regularMarketPrice']
        print(tesla_stock_price)

        alisa_talk(f"currently you can purchase tesla share for, {tesla_stock_price} US dollars")

    # wolfram alpha api - capital of a country
    elif "capital" in text and "of" in text:
        wolfram_alpha_country_capital(text)

    # wolfram alpha api - calculations
    elif "+" in text or "-" in text or "x" in text or "/" in text or "%" in text or "log" in text or "logarithm" in \
    text or "root" in text or "power" in text or "percent" in text or "average" in text or "integration" in text:
        wolfram_alpha_calculator(text)

    # wolfram alpha api - president of a certain country
    elif "president" in text and "of" in text:
        wolfram_alpha_president(text)

    # wolframalpha - airports
    elif "airport" in text:
        wolfram_alpha_airport(text)

    # # translator - japanese/hindi/telugu
    elif ("translate" in text and "japanese" in text) or ("in" in text and "japanese" in text):
        alisa_talk("sure")
        translator_japanese(text)

    elif ("translate" in text and "hindi" in text) or ("in" in text and "hindi" in text):
        alisa_talk("sure")
        translator_hindi(text)

    elif ("translate" in text and "telugu" in text) or ("in" in text and "telugu" in text):
        alisa_talk("sure")
        translator_telugu(text)

    # # jokes
    elif "joke" in text:
        if "joke" in text:
            jokes_fun()

        # while True:
        #     if "joke" in text or "yes" in text:
        #         jokes_fun()
        #         alisa_talk("do you want to hear another joke?")
        #         text = alisa_listen()
        #     else:
        #         alisa_talk("sure")
        #         break

    # # news
    elif "news" in text:
        alisa_talk("sure, todays top news are")
        get_news()

    # weather - temperature
    elif "temperature" in text:
        alisa_talk("sure, what is your current location")
        location = alisa_listen()
        get_temperature(location)

    # weather - weather
    elif "weather" in text:
        alisa_talk("sure, what is your current location")
        location = alisa_listen()
        print(location)
        get_weather(location)

    # distance
    elif "distance" in text:
        alisa_talk("sure, what is the starting point")
        from_location = alisa_listen()
        alisa_talk("alright, what is the destination point")
        to_location = alisa_listen()
        alisa_talk("okey, a moment please")

        distance_info(from_location, to_location)

    # # date and time
    elif "time" in text:
        time_now()

    elif "day" in text or "weekday" in text:
        current_weekday()

    # google search
    elif "what" in text or "who" in text or "where" in text or "why" in text or "define" in text or "describe" in text or "how" in text:
        alisa_talk("sure")
        google_search(text)

    # opening websites
    elif "google" in text or "browser" in text or "chrome" in text:
        open_chrome()
        return

    elif "youtube" in text or "you tube" in text:
        open_youtube()
        return

    elif "gmail" in text or "mail" in text:
        open_gmail()

    elif "driver" in text or "drive" in text or "google drive" in text:
        open_googledrive()

    elif "map" in text or "maps" in text:
        open_googlemaps()

    # opening applications
    elif "note" in text or "notepad" in text:
        open_notepad()

    elif "cmd" in text or "command prompt" in text or "terminal" in text:
        open_cmd()

    # updating user name
    elif ("change" in text or "update" in text) and "name" in text:
        alisa_talk("can you tell me your name?")
        updated_name = alisa_listen()
        with open("name.txt", 'w') as name:
            name.write(updated_name)
        print(updated_name)
        alisa_talk(f"sure, user name updated to {updated_name}")

    # # small talk

    elif "your" in text and "name" in text:
        alisa_talk("hi, my name is alisa, how can i help you?")

    elif "thanks" in text or "thank you" in text:
        alisa_talk("you're welcome, can i help you with anything else?")
    elif "exit" in text or "bye" in text:
        alisa_talk("ok have a nice day")
        

    # hi/hello/hai alisa
    # elif "hi" in text or "hai" in text or "hello" in text:
    #     alisa_talk("hello, how can i help you?")

    elif "you" in text and "stupid" in text:
        alisa_talk("well, I think i am pretty smart!")

    elif "favourite" in text or "favorite" in text and "movie" in text:
        alisa_talk("my favourite movie is, a silent voice. I watch it with my friends all the time")

    # unknown value or wait time exceeded
    else:
        alisa_talk("Please Repeat")


# self.theme_cls.primary_palette = "Green"
# self.theme_cls.primary_hue = "A700"


class Alisa(MDApp):

    def build(self):
        self.screen = Screen()

        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.primary_hue = "A700"         # Thickness of color

        query_btn = MDFillRoundFlatButton(text="Submit",
                                          pos_hint={"center_x": 0.5, "center_y": 0.6},
                                          on_press=self.reply
                                          )

        self.query = Builder.load_string(query_helper)
        toolbar = Builder.load_string(toolbar_helper)

        self.screen.add_widget(self.query)
        self.screen.add_widget(toolbar)
        self.screen.add_widget(query_btn)

        return self.screen

    def reply(self, widget):
        self.query.text = self.query.text.lower()
        original_text = " ".join(self.query.text.split())
        edited_text = "".join(self.query.text.split())
        # self.query.text = " ".join(self.query.text.split())

        print(self.query.text)
        if "sem" in self.query.text and not "semester" in self.query.text:
            alisa_talk("please enter the full name as semester")

        elif "year" in self.query.text and not "semester" in self.query.text:
            alisa_talk("please enter a valid semester")

        elif "semester" in self.query.text and not "year" in self.query.text:
            alisa_talk("please enter a valid year")

        elif ("year" in self.query.text or "semester" in self.query.text) and ("important" in self.query.text or "imp" in
        self.query.text):
            alisa_talk("sorry, important questions are not available, but you can search for previous question papers")

        elif "4year" in edited_text or "fouryear" in edited_text or "4thyear" in edited_text or \
        "fourthyear" in edited_text or "ivyear" in edited_text or "year4" in edited_text or "yearfour" in edited_text \
        or "year4th" in edited_text or "yearfourth" in edited_text or "yeariv" in edited_text:
            alisa_talk("4th year papers are not available")

        # 1 / one / 1st / first / i
        # # conditions

        elif "1year1semester" in edited_text or "1yearsemester1" in edited_text or "year11semester" in edited_text or "year1semester1" in edited_text or\
        "1semester1year" in edited_text or "1semesteryear1" in edited_text or "semester11year" in edited_text or "semester1year1" in edited_text or \
        "oneyearonesemester" in edited_text or "oneyearsemesterone" in edited_text or "yearoneonesemester" in edited_text or "yearonesemesterone" in edited_text or\
        "onesemesteroneyear" in edited_text or "onesemesteryearone" in edited_text or "semesteroneoneyear" in edited_text or "semesteroneyearone" in edited_text or\
        "1styear1stsemester" in edited_text or "1styearsemester1st" in edited_text or "year1st1stsemester" in edited_text or "year1stsemester1st" in edited_text or\
        "1stsemester1styear" in edited_text or "1stsemesteryear1st" in edited_text or "semester1st1styear" in edited_text or "semester1styear1st" in edited_text or\
        "firstyearfirstsemester" in edited_text or "firstyearsemesterfirst" in edited_text or "yearfirstfirstsemester" in edited_text or "yearfirstsemesterfirst" in edited_text or\
        "firstsemesterfirstyear" in edited_text or "firstsemesteryearfirst" in edited_text or "semesterfirstfirstyear" in edited_text or "semesterfirstyearfirst" in edited_text or\
        "iyearisemester" in edited_text or "iyearsemesteri" in edited_text or "yeariisemester" in edited_text or "yearisemesteri" in edited_text or \
        "isemesteriyear" in edited_text or "isemesteryeari" in edited_text or "semesteriiyear" in edited_text or "semesteriyeari" in edited_text:
            print(edited_text)
            self.questions_1_1_img()
            print("1 - 1")

        elif "1year2semester" in edited_text or "1yearsemester2" in edited_text or "year12semester" in edited_text or "year1semester2" in edited_text or\
        "2semester1year" in edited_text or "2semesteryear1" in edited_text or "semester21year" in edited_text or "semester2year1" in edited_text or \
        "oneyeartwosemester" in edited_text or "oneyearsemestertwo" in edited_text or "yearonetwosemester" in edited_text or "yearonesemestertwo" in edited_text or\
        "twosemesteroneyear" in edited_text or "twosemesteryearone" in edited_text or "semestertwooneyear" in edited_text or "semestertwoyearone" in edited_text or\
        "1styear2ndsemester" in edited_text or "1styearsemester2nd" in edited_text or "year1st2ndsemester" in edited_text or "year1stsemester2nd" in edited_text or\
        "2ndsemester1styear" in edited_text or "2ndsemesteryear1st" in edited_text or "semester2nd1styear" in edited_text or "semester2ndyear1st" in edited_text or\
        "firstyearsecondsemester" in edited_text or "firstyearsemestersecond" in edited_text or "yearfirstsecondsemester" in edited_text or "yearfirstsemestersecond" in edited_text or\
        "secondsemesterfirstyear" in edited_text or "secondsemesteryearfirst" in edited_text or "semestersecondfirstyear" in edited_text or "semestersecondyearfirst" in edited_text or\
        "iyeariisemester" in edited_text or "iyearsemesterii" in edited_text or "yeariiisemester" in edited_text or "yearisemesterii" in edited_text or\
        "iisemesteriyear" in edited_text or "iisemesteryeari" in edited_text or "semesteriiiyear" in edited_text or "semesteriiyeari" in edited_text:
            print(edited_text)
            self.questions_1_2_img()
            print("1 - 2")

        elif "2year1semester" in edited_text or "2yearsemester1" in edited_text or "year21semester" in edited_text or "year2semester1" in edited_text or\
        "1semester2year" in edited_text or "1semesteryear2" in edited_text or "semester12year" in edited_text or "semester1year2" in edited_text or \
        "twoyearonesemester" in edited_text or "twoyearsemesterone" in edited_text or "yeartwoonesemester" in edited_text or "yeartwosemesterone" in edited_text or\
        "onesemestertwoyear" in edited_text or "onesemesteryeartwo" in edited_text or "semesteronetwoyear" in edited_text or "semesteroneyeartwo" in edited_text or\
        "2ndyear1stsemester" in edited_text or "2ndyearsemester1st" in edited_text or "year2nd1stsemester" in edited_text or "year2ndsemester1st" in edited_text or\
        "1stsemester2ndyear" in edited_text or "1stsemesteryear2nd" in edited_text or "semester1st2ndyear" in edited_text or "semester1styear2nd" in edited_text or\
        "secondyearfirstsemester" in edited_text or "secondyearsemesterfirst" in edited_text or "yearsecondfirstsemester" in edited_text or "yearsecondsemesterfirst" in edited_text or\
        "firstsemestersecondyear" in edited_text or "firstsemesteryearsecond" in edited_text or "semesterfirstsecondyear" in edited_text or "semesterfirstyearsecond" in edited_text or\
        "iiyearisemester" in edited_text or "iiyearsemesteri" in edited_text or "yeariiisemester" in edited_text or "yeariisemesteri" in edited_text or\
        "isemesteriiyear" in edited_text or "isemesteryearii" in edited_text or "semesteriiiyear" in edited_text or "semesteriyearii" in edited_text:
            print(edited_text)
            self.questions_2_1_img()
            print("2 - 1")

        elif "2year2semester" in edited_text or "2yearsemester2" in edited_text or "year22semester" in edited_text or "year2semester2" in edited_text or\
        "2semester2year" in edited_text or "2semesteryear2" in edited_text or "semester22year" in edited_text or "semester2year2" in edited_text or \
        "twoyeartwosemester" in edited_text or "twoyearsemestertwo" in edited_text or "yeartwotwosemester" in edited_text or "yeartwosemestertwo" in edited_text or\
        "twosemestertwoyear" in edited_text or "twosemesteryeartwo" in edited_text or "semestertwotwoyear" in edited_text or "semestertwoyeartwo" in edited_text or\
        "2ndyear2ndsemester" in edited_text or "2ndyearsemester2nd" in edited_text or "year2nd2ndsemester" in edited_text or "year2ndsemester2nd" in edited_text or\
        "2ndsemester2ndyear" in edited_text or "2ndsemesteryear2nd" in edited_text or "semester2nd2ndyear" in edited_text or "semester2ndyear2nd" in edited_text or\
        "secondyearsecondsemester" in edited_text or "secondyearsemestersecond" in edited_text or "yearsecondsecondsemester" in edited_text or "yearsecondsemestersecond" in edited_text or\
        "secondsemestersecondyear" in edited_text or "secondsemesteryearsecond" in edited_text or "semestersecondsecondyear" in edited_text or "semestersecondyearsecond" in edited_text or\
        "iiyeariisemester" in edited_text or "iiyearsemesterii" in edited_text or "yeariiiisemester" in edited_text or "yeariisemesterii" in edited_text or\
        "iisemesteriiyear" in edited_text or "iisemesteryearii" in edited_text or "semesteriiiiyear" in edited_text or "semesteriiyearii" in edited_text:
            print(edited_text)
            self.questions_2_2_img()
            print("2 - 2")

        elif "3year1semester" in edited_text or "3yearsemester1" in edited_text or "year31semester" in edited_text or "year3semester1" in edited_text or\
        "1semester3year" in edited_text or "1semesteryear3" in edited_text or "semester13year" in edited_text or "semester1year3" in edited_text or \
        "threeyearonesemester" in edited_text or "threeyearsemesterone" in edited_text or  "yearthreeonesemester" in edited_text or "yearthreesemesterone" in edited_text or\
        "onesemesterthreeyear" in edited_text or "onesemesteryearthree" in edited_text or "semesteronethreeyear" in edited_text or "semesteroneyearthree" in edited_text or\
        "3rdyear1stsemester" in edited_text or "3rdyearsemester1st" in edited_text or "year3rd1stsemester" in edited_text or "year3rdsemester1st" in edited_text or\
        "1stsemester3rdyear" in edited_text or "1stsemesteryear3rd" in edited_text or "semester1st3rdyear" in edited_text or "semester1styear3rd" in edited_text or\
        "thirdyearfirstsemester" in edited_text or "thirdyearsemesterfirst" in edited_text or "yearthirdfirstsemester" in edited_text or "yearthirdsemesterfirst" in edited_text or\
        "firstsemesterthirdyear" in edited_text or "firstsemesteryearthird" in edited_text or "semesterfirstthirdyear" in edited_text or "semesterfirstyearthird" in edited_text or\
        "iiiyearisemester" in edited_text or "iiiyearsemesteri" in edited_text or "yeariiiisemester" in edited_text or "yeariiisemesteri" in edited_text or\
        "isemesteriiiyear" in edited_text or "isemesteryeariii" in edited_text or "semesteriiiiyear" in edited_text or "semesteriyeariii" in edited_text:
            print(edited_text)
            self.questions_3_1_img()
            print("3 - 1")

        elif "3year2semester" in edited_text or "3yearsemester2" in edited_text or "year32semester" in edited_text or "year3semester2" in edited_text or\
        "2semester3year" in edited_text or "2semesteryear3" in edited_text or "semester23year" in edited_text or "semester2year3" in edited_text or \
        "threeyeartwosemester" in edited_text or "threeyearsemestertwo" in edited_text or "yearthreetwosemester" in edited_text or "yearthreesemestertwo" in edited_text or\
        "twosemesterthreeyear" in edited_text or "twosemesteryearthree" in edited_text or "semestertwothreeyear" in edited_text or "semestertwoyearthree" in edited_text or\
        "3rdyear2ndsemester" in edited_text or "3rdyearsemester2nd" in edited_text or "year3rd2ndsemester" in edited_text or "year3rdsemester2nd" in edited_text or\
        "2ndsemester3rdyear" in edited_text or "2ndsemesteryear3rd" in edited_text or "semester2nd3rdyear" in edited_text or "semester2ndyear3rd" in edited_text or\
        "thirdyearsecondsemester" in edited_text or "thirdyearsemestersecond" in edited_text or "yearthirdsecondsemester" in edited_text or "yearthirdsemestersecond" in edited_text or\
        "secondsemesterthirdyear" in edited_text or "secondsemesteryearthird" in edited_text or "semestersecondthirdyear" in edited_text or "semestersecondyearthird" in edited_text or\
        "iiiyeariisemester" in edited_text or "iiiyearsemesterii" in edited_text or "yeariiiiisemester" in edited_text or "yeariiisemesterii" in edited_text or\
        "iisemesteriiiyear" in edited_text or "iisemesteryeariii" in edited_text or "semesteriiiiiyear" in edited_text or "semesteriiyeariii" in edited_text:
            print(edited_text)
            self.questions_3_2_img()
            print("3 - 2")

        else:
            print(original_text)
            alisa_reply(original_text)

    # previous questions

    def questions_1_1_img(self):
        # mathematics - I
        storage.child("JNTUH/FIRST/SEM_1/MATHEMATICS_1/R16/MATHEMATICS_1_page-0001.jpg").download\
            ("mathematics_1_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/MATHEMATICS_1/R16/MATHEMATICS_1_page-0002.jpg").download\
            ("mathematics_1_r16_02.jpg")

        storage.child("JNTUH/FIRST/SEM_1/MATHEMATICS_1/R18/MATHEMATICS_1_page-0001.jpg").download\
            ("mathematics_1_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/MATHEMATICS_1/R18/MATHEMATICS_1_page-0002.jpg").download\
            ("mathematics_1_r18_02.jpg")

        # storage.child("JNTUH/FIRST/SEM_1/MATHEMATICS_1/R18/MATHEMATICS_1_2019_page-0001_page-0001.jpg").download \
        #     ("mathematics_1_r18_2019_01.jpg")
        # storage.child("JNTUH/FIRST/SEM_1/MATHEMATICS_1/R18/MATHEMATICS_1_2019_page-0001_page-0002.jpg").download \
        #     ("mathematics_1_r18_2019_02.jpg")

        # chemistry
        storage.child("JNTUH/FIRST/SEM_1/ENGINEERING_CHEMISTRY/R16/ENGINEERING_CHEMISTRY_page-0001.jpg").download\
            ("chemistry_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/ENGINEERING_CHEMISTRY/R16/ENGINEERING_CHEMISTRY_page-0002.jpg").download\
            ("chemistry_r16_02.jpg")

        storage.child("JNTUH/FIRST/SEM_1/CHEMISTRY/R18/CHEMISTRY_page-0001.jpg").download("chemistry_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/CHEMISTRY/R18/CHEMISTRY_page-0002.jpg").download("chemistry_r18_02.jpg")

        # storage.child("JNTUH/FIRST/SEM_1/CHEMISTRY/R18/CHEMISTRY_2019_page-0001.jpg").download("chemistry_r18_2019_01.jpg")
        # storage.child("JNTUH/FIRST/SEM_1/CHEMISTRY/R18/CHEMISTRY_2019_page-0002.jpg").download("chemistry_r18_2019_02.jpg")

        # electrical engineering
        storage.child("JNTUH/FIRST/SEM_1/BASIC_ELECTRICAL_AND_ELECTRONIC_ENGINEERING/R16/BASIC_ELECTRICAL_AND_"
                      "ELECTRONIC_ENGIEERING_page-0001.jpg").download("BEE_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/BASIC_ELECTRICAL_AND_ELECTRONIC_ENGINEERING/R16/BASIC_ELECTRICAL_AND_"
                      "ELECTRONIC_ENGIEERING_page-0002.jpg").download("BEE_r16_02.jpg")

        storage.child("JNTUH/FIRST/SEM_1/BASIC_ELECTRICAL_ENGINEERING/R18/BASIC_ELECTRICAL_ENGINEERING_page-"
                      "0001.jpg").download("BEE_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/BASIC_ELECTRICAL_ENGINEERING/R18/BASIC_ELECTRICAL_ENGINEERING_page-"
                      "0002.jpg").download("BEE_r18_02.jpg")

        # storage.child("JNTUH/FIRST/SEM_1/BASIC_ELECTRICAL_ENGINEERING/R18/BASIC_ELECTRICAL_ENGINEERING_2019_page-"
        #               "0001.jpg").download("BEE_r18_2019_01.jpg")
        # storage.child("JNTUH/FIRST/SEM_1/BASIC_ELECTRICAL_ENGINEERING/R18/BASIC_ELECTRICAL_ENGINEERING_2019_page-"
        #               "0002.jpg").download("BEE_r18_2019_02.jpg")

        # english
        storage.child("JNTUH/FIRST/SEM_1/PROFESSIONAL_COMMUNICATION_IN_ENGLISH/R16/PROFESSIONAL_COMMUNICATION_IN_"
                      "ENGLISH_page-0001.jpg").download("english_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/PROFESSIONAL_COMMUNICATION_IN_ENGLISH/R16/PROFESSIONAL_COMMUNICATION_IN_"
                      "ENGLISH_page-0002.jpg").download("english_r16_02.jpg")
        storage.child("JNTUH/FIRST/SEM_1/PROFESSIONAL_COMMUNICATION_IN_ENGLISH/R16/PROFESSIONAL_COMMUNICATION_IN_"
                      "ENGLISH_page-0003.jpg").download("english_r16_03.jpg")

        storage.child("JNTUH/FIRST/SEM_1/ENGLISH/R18/ENGLISH_page-0001.jpg").download("english_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_1/ENGLISH/R18/ENGLISH_page-0002.jpg").download("english_r18_02.jpg")

        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_I_I)
        self.screen.add_widget(next_screen)

    def questions_1_2_img(self):
        # mathematics - II
        storage.child("JNTUH/FIRST/SEM_2/MATHEMATICS_2/R16/MATHEMATICS_2_page-0001.jpg").download\
            ("mathematics_2_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_2/MATHEMATICS_2/R16/MATHEMATICS_2_page-0002.jpg").download\
            ("mathematics_2_r16_02.jpg")

        storage.child("JNTUH/FIRST/SEM_2/MATHEMATICS_2/R18/MATHEMATICS_2_page-0001.jpg").download\
            ("mathematics_2_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_2/MATHEMATICS_2/R18/MATHEMATICS_2_page-0002.jpg").download\
            ("mathematics_2_r18_02.jpg")

        # physics
        storage.child("JNTUH/FIRST/SEM_2/ENGINEERING_PHYSICS_2/R16/ENGINEERING_PHYSICS_2_page-0001.jpg").download\
            ("physics_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_2/ENGINEERING_PHYSICS_2/R16/ENGINEERING_PHYSICS_2_page-0002.jpg").download\
            ("physics_r16_02.jpg")

        storage.child("JNTUH/FIRST/SEM_2/APPLIED_PHYSICS/R18/APPLIED_PHYSICS_page-0001.jpg").download\
            ("physics_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_2/APPLIED_PHYSICS/R18/APPLIED_PHYSICS_page-0002.jpg").download\
            ("physics_r18_02.jpg")

        # pps
        storage.child("JNTUH/FIRST/SEM_2/COMPUTER_PROGRAMMING_IN_C/R16/COMPUTER_PROGRAMMING_IN_C_page-"
                      "0001.jpg").download("c_r16_01.jpg")
        storage.child("JNTUH/FIRST/SEM_2/COMPUTER_PROGRAMMING_IN_C/R16/COMPUTER_PROGRAMMING_IN_C_page-"
                      "0002.jpg").download("c_r16_02.jpg")

        storage.child("JNTUH/FIRST/SEM_2/PROGRAMMING_FOR_PROBLEM_SOLVING/R18/PROGRAMMING_FOR_PROBLEM_SOLVING_page-"
                      "0001.jpg").download("pps_r18_01.jpg")
        storage.child("JNTUH/FIRST/SEM_2/PROGRAMMING_FOR_PROBLEM_SOLVING/R18/PROGRAMMING_FOR_PROBLEM_SOLVING_page-"
                      "0002.jpg").download("pps_r18_02.jpg")

        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_I_II)
        self.screen.add_widget(next_screen)

    def questions_2_1_img(self):
        # ADE
        storage.child("JNTUH/SECOND/SEM_1/DIGITAL_LOGIC_DESIGN/R16/DIGITAL_LOGIC_DESIGN_page-0001.jpg").download\
            ("ade_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/DIGITAL_LOGIC_DESIGN/R16/DIGITAL_LOGIC_DESIGN_page-0002.jpg").download\
            ("ade_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_1/ANALOG_AND_DIGITAL_ELECTRONICS/R18/ANALOG_AND_DIGITAL_ELECTRONICS_page-"
                      "0001.jpg").download("ade_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/ANALOG_AND_DIGITAL_ELECTRONICS/R18/NONE_0002.jpeg")\
            .download("ade_r18_01.jpg")

        # COA
        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORGANIZATION_AND_ARCHITECTURE/R16/NOT_AVAILABLE_0001.jpeg")\
            .download("coa_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORGANIZATION_AND_ARCHITECTURE/R16/NOT_AVAILABLE_0002.jpeg") \
            .download("coa_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORGANIZATION_AND_ARCHITECTURE/R18/COMPUTER_ORGANIZATION_AND_"
                      "ARCHITECTURE_page-0001.jpg").download("coa_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORGANIZATION_AND_ARCHITECTURE/R18/NONE_0002.jpeg")\
            .download("coa_r18_02.jpg")

        # COSM
        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORIENTED_STATISTICAL_METHOD/R16/NOT_AVAILABLE_0001.jpeg")\
            .download("cosm_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORIENTED_STATISTICAL_METHOD/R16/NOT_AVAILABLE_0002.jpeg")\
            .download("cosm_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORIENTED_STATISTICAL_METHOD/R18/COMPUTER_ORIENTED_STATISTICAL_METHOD"
                      "_page-0001.jpg").download("cosm_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/COMPUTER_ORIENTED_STATISTICAL_METHOD/R18/COMPUTER_ORIENTED_STATISTICAL_METHOD"
                      "_page-0002.jpg").download("cosm_r18_02.jpg")

        # DS
        storage.child("JNTUH/SECOND/SEM_1/DATA_STRUCTURE/R16/NOT_AVAILABLE_0001.jpeg").download("ds_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/DATA_STRUCTURE/R16/NOT_AVAILABLE_0002.jpeg").download("ds_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_1/DATA_STRUCTURE/R18/DATA_STRUCTURE_page-0001.jpg").download("ds_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/DATA_STRUCTURE/R18/NONE_0002.jpeg").download("ds_r18_01.jpg")

        # OOP
        storage.child("JNTUH/SECOND/SEM_1/OBJECT_ORIENTED_PROGRAMMING_USING_JAVA/R16/OBJECT_ORIENTED_PROGRAMMING_USING"
                      "_JAVA_page-0001.jpg").download("oop_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/OBJECT_ORIENTED_PROGRAMMING_USING_JAVA/R16/OBJECT_ORIENTED_PROGRAMMING_USING"
                      "_JAVA_page-0002.jpg").download("oop_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_1/OBJECT_ORIENTED_PROGRAMMING_USING_JAVA/R18/NOT_AVAILABLE_0001.jpeg")\
            .download("oop_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_1/OBJECT_ORIENTED_PROGRAMMING_USING_JAVA/R18/NOT_AVAILABLE_0002.jpeg") \
            .download("oop_r18_02.jpg")

        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_II_I)
        self.screen.add_widget(next_screen)

    def questions_2_2_img(self):
        # BEFA
        storage.child("JNTUH/SECOND/SEM_2/BUSINESS_ECONOMICS_AND_FINANCIAL_ANALYSIS/R16/NOT_AVAILABLE_0001.jpeg")\
            .download("befa_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/BUSINESS_ECONOMICS_AND_FINANCIAL_ANALYSIS/R16/NOT_AVAILABLE_0002.jpeg")\
            .download("befa_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_2/BUSINESS_ECONOMICS_AND_FINANCIAL_ANALYSIS/R18/BUSINESS_ECONOMICS_AND_"
                      "FINANCIAL_ANALYSIS_page-0001.jpg").download("befa_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/BUSINESS_ECONOMICS_AND_FINANCIAL_ANALYSIS/R18/BUSINESS_ECONOMICS_AND_"
                      "FINANCIAL_ANALYSIS_page-0002.jpg").download("befa_r18_02.jpg")

        # DBMS
        storage.child("JNTUH/SECOND/SEM_2/DATABASE_MANAGEMENT_SYSTEM/R16/DATABASE_MANAGEMENT_SYSTEM_page-"
                      "0001.jpg").download("dbms_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/DATABASE_MANAGEMENT_SYSTEM/R18/DATABASE_MANAGEMENT_SYSTEM_page-"
                      "0002.jpg").download("dbms_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_2/DATABASE_MANAGEMENT_SYSTEM/R18/DATABASE_MANAGEMENT_SYSTEM_page-"
                      "0001.jpg").download("dbms_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/DATABASE_MANAGEMENT_SYSTEM/R18/DATABASE_MANAGEMENT_SYSTEM_page-"
                      "0002.jpg").download("dbms_r18_02.jpg")

        # DM
        storage.child("JNTUH/SECOND/SEM_2/DISCRETE_MATHEMATICS/R16/NOT_AVAILABLE_0001.jpeg").download("dm_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/DISCRETE_MATHEMATICS/R16/NOT_AVAILABLE_0002.jpeg").download("dm_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_2/DISCRETE_MATHEMATICS/R18/DISCRETE_MATHEMATICS_page-"
                      "0001.jpg").download("dm_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/DISCRETE_MATHEMATICS/R18/NONE_0002.jpeg").download("dm_r18_02.jpg")


        # Java
        storage.child("JNTUH/SECOND/SEM_2/JAVA_PROGRAMMING/R16/NOT_AVAILABLE_0001.jpeg").download("java_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/JAVA_PROGRAMMING/R16/NOT_AVAILABLE_0002.jpeg").download("java_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_2/JAVA_PROGRAMMING/R18/JAVA_PROGRAMMING_page-0001.jpg").download\
            ("java_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/JAVA_PROGRAMMING/R18/NONE_0002.jpeg").download \
            ("java_r18_02.jpg")

        # OS
        storage.child("JNTUH/SECOND/SEM_2/OPERTAING_SYSTEM/R16/NONE_0002.jpeg").download\
            ("os_r16_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/OPERTAING_SYSTEM/R16/OPERATING_SYSTEMS_page-0001.jpg").download\
            ("os_r16_02.jpg")

        storage.child("JNTUH/SECOND/SEM_2/OPERTAING_SYSTEM/R18/NOT_AVAILABLE_0001.jpeg").download \
            ("os_r18_01.jpg")
        storage.child("JNTUH/SECOND/SEM_2/OPERTAING_SYSTEM/R18/NOT_AVAILABLE_0002.jpeg").download \
            ("os_r18_02.jpg")

        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_II_II)
        self.screen.add_widget(next_screen)

    def questions_3_1_img(self):
        # CN
        storage.child("JNTUH/THIRD/SEM_1/COMPUTER_NETWORKS/R16/NOT_AVAILABLE_0001.jpeg").download("cn_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/COMPUTER_NETWORKS/R16/NOT_AVAILABLE_0002.jpeg").download("cn_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_1/COMPUTER_NETWORKS/R18/COMPUTER_NETWORKS_page-0001.jpg").download \
            ("cn_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/COMPUTER_NETWORKS/R18/NONE_0002.jpeg").download \
            ("cn_r18_02.jpg")

        # DD
        storage.child("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_2/DISTRIBUTED_DATABASE/R16/NOT_AVAILABLE_0001.jpeg").download\
            ("dd_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_2/DISTRIBUTED_DATABASE/R16/NOT_AVAILABLE_0002.jpeg").download\
            ("dd_r16_02.jpg")

        storage("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_2/DISTRIBUTED_DATABASE/R18/DISTRIBUTED_DATABASE_page-0001.jpg").\
            download("dd_r18_01.jpg")
        storage("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_2/DISTRIBUTED_DATABASE/R18/NONE_0002.jpeg"). \
            download("dd_r18_02.jpg")

        # FLAT
        storage("JNTUH/THIRD/SEM_1/FORMAL_LANGUAGE_AND_AUTOMATA_THEORY/R16/NOT_AVAILABLE_0001.jpeg").download\
            ("flat_r16_01.jpg")
        storage("JNTUH/THIRD/SEM_1/FORMAL_LANGUAGE_AND_AUTOMATA_THEORY/R16/NOT_AVAILABLE_0002.jpeg").download \
            ("flat_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_1/FORMAL_LANGUAGE_AND_AUTOMATA_THEORY/R18/FORMAL_LANGUAGE_AND_AUTOMATA_THEORY_"
                      "page-0001.jpg").download("flat_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/FORMAL_LANGUAGE_AND_AUTOMATA_THEORY/R18/FORMAL_LANGUAGE_AND_AUTOMATA_THEORY_"
                      "page-0002.jpg").download("flat_r18_02.jpg")

        # PPL
        storage("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_1/PRINCIPLES_OF_PROGRAMMING_LANGUAGE/R16/NOT_AVAILABLE_0001.jpeg")\
            .download("ppl_r16_01.jpg")
        storage("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_1/PRINCIPLES_OF_PROGRAMMING_LANGUAGE/R16/NOT_AVAILABLE_0002.jpeg") \
            .download("ppl_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_1/PRO_ELECTIVE_1/PRINCIPLES_OF_PROGRAMMING_LANGUAGE/R18/PRINCIPALS_OF_PROGRAMMING_LANGUAGES_page-0001.jpg")\
            .download("ppl_r18_01.jpg")
        storage.child(
            "JNTUH/THIRD/SEM_1/PRO_ELECTIVE_1/PRINCIPLES_OF_PROGRAMMING_LANGUAGE/R18/NONE_0002.jpeg")\
            .download("ppl_r18_02.jpg")

        # SE
        storage.child("JNTUH/THIRD/SEM_1/SOFTWARE_ENGINEERING/R16/NOT_AVAILABLE_0001.jpeg").download("se_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/SOFTWARE_ENGINEERING/R16/NOT_AVAILABLE_0002.jpeg").download("se_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_1/SOFTWARE_ENGINEERING/R18/SOFTWARE_ENGINEERING_page-"
                      "0001.jpg").download("se_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/SOFTWARE_ENGINEERING/R18/NONE_0002.jpeg").download("se_r18_02.jpg")

        # WT
        storage.child("JNTUH/THIRD/SEM_1/WEB_TECHNOLOGIES/R16/NOT_AVAILABLE_0001.jpeg").download("wt_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/WEB_TECHNOLOGIES/R16/NOT_AVAILABLE_0002.jpeg").download("wt_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_1/WEB_TECHNOLOGIES/R18/WEB_TECHNOLOGIES_page-0001.jpg").download\
            ("wt_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_1/WEB_TECHNOLOGIES/R18/NONE_0002.jpeg").download("wt_r18_02.jpg")

        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_III_I)
        self.screen.add_widget(next_screen)

    def questions_3_2_img(self):
        # ML
        storage.child("JNTUH/THIRD/SEM_2/MACHINE_LEARNING/R16/NOT_AVAILABLE_0001.jpeg").download("ml_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_2/MACHINE_LEARNING/R16/NOT_AVAILABLE_0002.jpeg").download("ml_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_2/MACHINE_LEARNING/R18/MACHINE_LEARNING_page-0001.jpg").download\
            ("ml_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_2/MACHINE_LEARNING/R18/NONE_0002.jpeg").download \
            ("ml_r18_02.jpg")

        # CD
        storage.child("JNTUH/THIRD/SEM_2/COMPILER_DESIGN/R16/NOT_AVAILABLE_0001.jpeg").download("cd_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_2/COMPILER_DESIGN/R16/NOT_AVAILABLE_0002.jpeg").download("cd_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_2/COMPILER_DESIGN/R18/COMPILER_DESGIN_page-0001.jpg").download\
            ("cd_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_2/COMPILER_DESIGN/R18/COMPILER_DESGIN_page-0002.jpg").download \
            ("cd_r18_02.jpg")

        # DAA (missing r18 (None))
        storage.child("JNTUH/THIRD/SEM_2/DESIGN_AND_ANALYSIS_OF_ALGORITHM/R16/NOT_AVAILABLE_0001.jpeg")\
            .download("daa_r16_01.jpg")
        storage.child("JNTUH/THIRD/SEM_2/DESIGN_AND_ANALYSIS_OF_ALGORITHM/R16/NOT_AVAILABLE_0002.jpeg")\
            .download("daa_r16_02.jpg")

        storage.child("JNTUH/THIRD/SEM_2/DESIGN_AND_ANALYSIS_OF_ALGORITHM/R18/DESIGN_AND_ANALYSIS_OF_ALGORITHMS_page"
                      "-0001.jpg").download("daa_r18_01.jpg")

        # SL (missing r16 (Not Available))
        storage.child("JNTUH/THIRD/SEM_2/OPEN_ELECTIVE_1/SCRIPTING_LANGUAGES/R18/NOT_AVAILABLE_0001.jpeg")\
            .download("sl_r18_01.jpg")
        storage.child("JNTUH/THIRD/SEM_2/OPEN_ELECTIVE_1/SCRIPTING_LANGUAGES/R18/NOT_AVAILABLE_0002.jpeg") \
            .download("sl_r18_02.jpg")

        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_III_II)
        self.screen.add_widget(next_screen)

    # # execution section

    def execute_assistant(self):
        time = int(datetime.now().strftime('%H'))
        meridian = datetime.now().strftime('%p')

        if os.path.exists("name.txt"):
            with open("name.txt", 'r') as name_file:
                user_name = name_file.read()
                while user_name == " " or user_name == "":
                    alisa_talk("hello, i am your personal assistant alisa, can you tell me your name?")
                    user_name = alisa_listen()
                    print(user_name)
                    with open("name.txt", 'w') as file:
                        file.write(user_name)
        else:
            with open("name.txt", "w+") as name_file:
                user_name = name_file.read()
                while user_name == " " or user_name == "":
                    alisa_talk("hello, i am your personal assistant alisa, can you tell me your name?")
                    user_name = alisa_listen()
                    print(user_name)
                    name_file.write(user_name)
                    
        if 4 < time < 12 and meridian == 'AM':
            alisa_talk(f"good morning {user_name}, how can i help you?")
        elif 12 <= time < 14 and meridian == 'PM':
            alisa_talk(f"good afternoon {user_name}, how can i help you?")
        elif 14 <= time < 24 and meridian == 'PM':
            alisa_talk(f"good evening {user_name}, how can i help you?")

        while True:
            listen_alisa = alisa_listen()
            print(listen_alisa)

            if "4th year" in listen_alisa or "fourth year" in listen_alisa or "4 year" in listen_alisa or \
            "four year" in listen_alisa or "year 4th" in listen_alisa or "year fourth" in listen_alisa or "year 4" \
            in listen_alisa or "year four" in listen_alisa:
                alisa_talk("4th year papers are not available")

            elif ("year" in listen_alisa or "semester" in listen_alisa) and ("important" in listen_alisa or "imp" in listen_alisa):
                alisa_talk("sorry, important questions are not available, but you can search for previous question papers")

            elif "year" in listen_alisa and not "semester" in listen_alisa:
                alisa_talk("please tell a valid semester")

            elif "semester" in listen_alisa and not "year" in listen_alisa:
                alisa_talk("please tell a valid year")

            elif listen_alisa == "" or listen_alisa == " ":
                alisa_talk("bye..., have a nice day")
                break

            # breaking loop
            elif "goodbye" in listen_alisa or "bye" in listen_alisa or "stop" in listen_alisa or "no" in listen_alisa or (
            "ok" in listen_alisa and "thank you" not in listen_alisa and "thanks" not in listen_alisa):
                alisa_talk("it was my pleasure, see you again")
                break

            # # conditions:

            elif ("1st year" in listen_alisa or "first year" in listen_alisa or "year 1" in listen_alisa or "1 year" in
            listen_alisa or "one year" in listen_alisa or "year one" in listen_alisa) and \
            ("1st semester" in listen_alisa or "first semester" in listen_alisa or "1 semester" in listen_alisa or
            "semester 1" in listen_alisa or "1st sem" in listen_alisa or "first sem" in listen_alisa or "1 sem" in
            listen_alisa or "sem 1" in listen_alisa) and not ("2 year" in listen_alisa or "second year" in listen_alisa
            or "2nd year" in listen_alisa or "two year" in listen_alisa or "3 year" in listen_alisa or "third year" in
            listen_alisa or "three year" in listen_alisa or "3rd year" in listen_alisa):
                # self.questions_1_1_img()
                print("1 - 1")
                break

            elif ("1st year" in listen_alisa or "first year" in listen_alisa or "year 1" in listen_alisa or "1 year" in
            listen_alisa or "one year" in listen_alisa or "year one" in listen_alisa) and \
            ("2nd semester" in listen_alisa or "second semester" in listen_alisa or "2 semester" in listen_alisa or
            "semester 2" in listen_alisa or "2nd sem" in listen_alisa or "second sem" in listen_alisa or "2 sem" in
            listen_alisa or "sem 2" in listen_alisa):
                # self.questions_1_2_img()
                print("1 - 2")
                break

            elif ("2nd year" in listen_alisa or "second year" in listen_alisa or "year 2" in listen_alisa or "2 year" in
            listen_alisa or "two year" in listen_alisa or "year two" in listen_alisa) and \
            ("1st semester" in listen_alisa or "first semester" in listen_alisa or "1 semester" in listen_alisa or
            "semester 1" in listen_alisa or "1st sem" in listen_alisa or "first sem" in listen_alisa or "1 sem" in
            listen_alisa or "sem 1" in listen_alisa):
                # self.questions_2_1_img()
                print("2 - 1")
                break

            elif ("2nd year" in listen_alisa or "second year" in listen_alisa or "year 2" in listen_alisa or "2 year" in
            listen_alisa or "two year" in listen_alisa or "year two" in listen_alisa) and \
            ("2nd semester" in listen_alisa or "second semester" in listen_alisa or "2 sesmester" in listen_alisa or
            "semester 2" in listen_alisa or "2nd sem" in listen_alisa or "second sem" in listen_alisa or "2 sem" in
            listen_alisa or "sem 2" in listen_alisa) and not ("3 year" in listen_alisa or "third year" in listen_alisa
            or "three year" in listen_alisa or "3rd year" in listen_alisa):
                # self.questions_2_2_img()
                print("2 - 2")
                break

            elif ("3rd year" in listen_alisa or "third year" in listen_alisa or "year 3" in listen_alisa or "3 year" in
            listen_alisa or "three year" in listen_alisa or "year three" in listen_alisa) and \
            ("1st semester" in listen_alisa or "first semester" in listen_alisa or "1 semester" in listen_alisa or
            "semester 1" in listen_alisa or "1st sem" in listen_alisa or "first sem" in listen_alisa or "1 sem" in
            listen_alisa or "sem 1" in listen_alisa):
                # self.questions_3_1_img()
                print("3 - 1")
                break

            elif ("3rd year" in listen_alisa or "third year" in listen_alisa or "year 3" in listen_alisa or "3 year" in
            listen_alisa or "three year" in listen_alisa or "year three" in listen_alisa) and \
            ("2nd semester" in listen_alisa or "second semester" in listen_alisa or "2 semester" in listen_alisa or
            "semester 2" in listen_alisa or "2nd sem" in listen_alisa or "second sem" in listen_alisa or "2 sem" in
            listen_alisa or "sem 2" in listen_alisa):
                # self.questions_3_2_img()
                print("3 - 2")
                break

            else:
                alisa_reply(listen_alisa)

    def restart(self):
        App.get_running_app().stop()
        Window.close()

        def open_app():
            print("started")
            __file__ = "main.py"
            subprocess.call([sys.executable, os.path.relpath(__file__)] + sys.argv[1:])

        t = Timer(2, open_app)
        t.start()

# firebase implementation down here!


config = {
  "apiKey": "AIzaSyDMVjDyDXyvSKbeGmrQv8HM7sboTTObB1E",
  "authDomain": "voice-assistant-13b8c.firebaseapp.com",
  "databaseURL": "https://voice-assistant-13b8c-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "voice-assistant-13b8c",
  "storageBucket": "voice-assistant-13b8c.appspot.com",
  "messagingSenderId": "337572643085",
  "appId": "1:337572643085:web:8f423ce1f735fc91fa3044",
  "measurementId": "G-9C9LL4ZREY"
}

firebase = Firebase(config)
storage = firebase.storage()

# # previous questions
# year-I sem-I


class I_I_subjects_img(Screen):
    pass


class I_I_mathematics_prev_img(Screen):
    pass


class I_I_chemistry_prev_img(Screen):
    pass


class I_I_electrical_engineering_prev_img(Screen):
    pass


class I_I_english_prev_img(Screen):
    pass


sm_I_I = ScreenManager()

sm_I_I.add_widget(I_I_subjects_img(name="I_I_subjects_img"))
sm_I_I.add_widget(I_I_mathematics_prev_img(name="mathematics_img"))
sm_I_I.add_widget(I_I_chemistry_prev_img(name="chemistry_img"))
sm_I_I.add_widget(I_I_electrical_engineering_prev_img(name="electrical_engineering_img"))
sm_I_I.add_widget(I_I_english_prev_img(name="english_img"))


# year - I sem - II


class I_II_subjects_img(Screen):
    pass


class I_II_mathematics_II_prev_img(Screen):
    pass


class I_II_applied_physics_prev_img(Screen):
    pass


class I_II_PPS_prev_img(Screen):
    pass


sm_I_II = ScreenManager()

sm_I_II.add_widget(I_II_subjects_img(name="I_II_subjects_img"))
sm_I_II.add_widget(I_II_mathematics_II_prev_img(name="mathematics_II_img"))
sm_I_II.add_widget(I_II_applied_physics_prev_img(name="applied_physics_img"))
sm_I_II.add_widget(I_II_PPS_prev_img(name="pps_img"))

# year - II sem - I


class II_I_subjects_img(Screen):
    pass


class II_I_ADE_prev_img(Screen):
    pass


class II_I_COA_prev_img(Screen):
    pass


class II_I_COSM_prev_img(Screen):
    pass


class II_I_data_structures_prev_img(Screen):
    pass


class II_I_OOP_prev_img(Screen):
    pass


sm_II_I = ScreenManager()

sm_II_I.add_widget(II_I_subjects_img(name="II_I_subjects_img"))
sm_II_I.add_widget(II_I_ADE_prev_img(name="ade_img"))
sm_II_I.add_widget(II_I_COA_prev_img(name="coa_img"))
sm_II_I.add_widget(II_I_COSM_prev_img(name="cosm_img"))
sm_II_I.add_widget(II_I_data_structures_prev_img(name="data_structures_img"))
sm_II_I.add_widget(II_I_OOP_prev_img(name="oop_img"))

# year - II sem - II


class II_II_subjects_img(Screen):
    pass


class II_II_BEFA_prev_img(Screen):
    pass


class II_II_DBMS_prev_img(Screen):
    pass


class II_II_discrete_mathematics_prev_img(Screen):
    pass


class II_II_java_programming_prev_img(Screen):
    pass


class II_II_operating_system_prev_img(Screen):
    pass


sm_II_II = ScreenManager()

sm_II_II.add_widget(II_II_subjects_img(name="II_II_subjects_img"))
sm_II_II.add_widget(II_II_BEFA_prev_img(name="befa_img"))
sm_II_II.add_widget(II_II_DBMS_prev_img(name="dbms_img"))
sm_II_II.add_widget(II_II_discrete_mathematics_prev_img(name="discrete_mathematics_img"))
sm_II_II.add_widget(II_II_java_programming_prev_img(name="java_img"))
sm_II_II.add_widget(II_II_operating_system_prev_img(name="operating_system_img"))

# year - III sem - I


class III_I_subjects_img(Screen):
    pass


class III_I_computer_networks_prev_img(Screen):
    pass


class III_I_distributed_databases_prev_img(Screen):
    pass


class III_I_FLAT_prev_img(Screen):
    pass


class III_I_PPL_prev_img(Screen):
    pass


class III_I_SE_prev_img(Screen):
    pass


class III_I_WT_prev_img(Screen):
    pass


sm_III_I = ScreenManager()

sm_III_I.add_widget(III_I_subjects_img(name="III_I_subjects_img"))
sm_III_I.add_widget(III_I_computer_networks_prev_img(name="cn_img"))
sm_III_I.add_widget(III_I_distributed_databases_prev_img(name="dd_img"))
sm_III_I.add_widget(III_I_FLAT_prev_img(name="flat_img"))
sm_III_I.add_widget(III_I_PPL_prev_img(name="ppl_img"))
sm_III_I.add_widget(III_I_SE_prev_img(name="se_img"))
sm_III_I.add_widget(III_I_WT_prev_img(name="wt_img"))

# year - III sem - II


class III_II_subjects_img(Screen):
    pass


class III_II_machine_learning_prev_img(Screen):
    pass


class III_II_compiler_design_prev_img(Screen):
    pass


class III_II_DAA_prev_img(Screen):
    pass


class III_II_scripting_languages_prev_img(Screen):
    pass


sm_III_II = ScreenManager()

sm_III_II.add_widget(III_II_subjects_img(name="III_II_subjects_img"))
sm_III_II.add_widget(III_II_machine_learning_prev_img(name="ml_img"))
sm_III_II.add_widget(III_II_compiler_design_prev_img(name="cd_img"))
sm_III_II.add_widget(III_II_DAA_prev_img(name="daa_img"))
sm_III_II.add_widget(III_II_scripting_languages_prev_img(name="sl_img"))

if __name__ == "__main__":
    Alisa().run()

# removing files
# 1 - 1
try:
    os.remove("mathematics_1_r16_01.jpg")
    os.remove("mathematics_1_r16_02.jpg")
    os.remove("mathematics_1_r18_01.jpg")
    os.remove("mathematics_1_r18_02.jpg")

    os.remove("chemistry_r16_01.jpg")
    os.remove("chemistry_r16_02.jpg")
    os.remove("chemistry_r18_01.jpg")
    os.remove("chemistry_r18_02.jpg")

    os.remove("BEE_r16_01.jpg")
    os.remove("BEE_r16_02.jpg")
    os.remove("BEE_r18_01.jpg")
    os.remove("BEE_r18_02.jpg")

    os.remove("english_r16_01.jpg")
    os.remove("english_r16_02.jpg")
    os.remove("english_r16_03.jpg")
    os.remove("english_r18_01.jpg")
    os.remove("english_r18_02.jpg")
except FileNotFoundError:
    print("Clearing Data...")

# 1 - 2
try:
    os.remove("mathematics_2_r16_01.jpg")
    os.remove("mathematics_2_r16_02.jpg")
    os.remove("mathematics_2_r18_01.jpg")
    os.remove("mathematics_2_r18_02.jpg")

    os.remove("physics_r16_01.jpg")
    os.remove("physics_r16_02.jpg")
    os.remove("physics_r18_01.jpg")
    os.remove("physics_r18_02.jpg")

    os.remove("c_r16_01.jpg")
    os.remove("c_r16_02.jpg")
    os.remove("pps_r18_01.jpg")
    os.remove("pps_r18_02.jpg")
except FileNotFoundError:
    print("Clearing Data...")

# 2 - 1
try:
    os.remove("ade_r16_01.jpg")
    os.remove("ade_r16_02.jpg")
    os.remove("ade_r18_01.jpg")
    os.remove("ade_r18_02.jpg")

    os.remove("coa_r16_01.jpg")
    os.remove("coa_r16_02.jpg")
    os.remove("coa_r18_01.jpg")
    os.remove("coa_r18_02.jpg")

    os.remove("cosm_r16_01.jpg")
    os.remove("cosm_r16_02.jpg")
    os.remove("cosm_r18_01.jpg")
    os.remove("cosm_r18_02.jpg")

    os.remove("ds_r16_01.jpg")
    os.remove("ds_r16_02.jpg")
    os.remove("ds_r18_01.jpg")
    os.remove("ds_r18_02.jpg")

    os.remove("oop_r16_01.jpg")
    os.remove("oop_r16_02.jpg")
    os.remove("oop_r18_01.jpg")
    os.remove("oop_r18_02.jpg")
except FileNotFoundError:
    print("Clearing Data...")

# 2 - 2
try:
    os.remove("befa_r16_01.jpg")
    os.remove("befa_r16_02.jpg")
    os.remove("befa_r18_01.jpg")
    os.remove("befa_r18_02.jpg")

    os.remove("dbms_r16_01.jpg")
    os.remove("dbms_r16_02.jpg")
    os.remove("dbms_r18_01.jpg")
    os.remove("dbms_r18_02.jpg")

    os.remove("dm_r16_01.jpg")
    os.remove("dm_r16_02.jpg")
    os.remove("dm_r18_01.jpg")
    os.remove("dm_r18_02.jpg")

    os.remove("java_r16_01.jpg")
    os.remove("java_r16_02.jpg")
    os.remove("java_r18_01.jpg")
    os.remove("java_r18_02.jpg")

    os.remove("os_r16_01.jpg")
    os.remove("os_r16_02.jpg")
    os.remove("os_r18_01.jpg")
    os.remove("os_r18_02.jpg")
except FileNotFoundError:
    print("Clearing Data...")

# 3 - 1
try:
    os.remove("cn_r16_01.jpg")
    os.remove("cn_r16_02.jpg")
    os.remove("cn_r18_01.jpg")
    os.remove("cn_r18_02.jpg")

    os.remove("flat_r16_01.jpg")
    os.remove("flat_r16_02.jpg")
    os.remove("flat_r18_01.jpg")
    os.remove("flat_r18_02.jpg")

    os.remove("se_r16_01.jpg")
    os.remove("se_r16_02.jpg")
    os.remove("se_r18_01.jpg")
    os.remove("se_r18_02.jpg")

    os.remove("wt_r16_01.jpg")
    os.remove("wt_r16_02.jpg")
    os.remove("wt_r18_01.jpg")
    os.remove("wt_r18_02.jpg")
except FileNotFoundError:
    print("Clearing Data...")

# 3 - 2
try:
    os.remove("ml_r16_01.jpg")
    os.remove("ml_r16_02.jpg")
    os.remove("ml_r18_01.jpg")
    os.remove("ml_r18_02.jpg")

    os.remove("cd_r16_01.jpg")
    os.remove("cd_r16_02.jpg")
    os.remove("cd_r18_01.jpg")
    os.remove("cd_r18_02.jpg")

    os.remove("daa_r16_01.jpg")
    os.remove("daa_r16_02.jpg")
    os.remove("daa_r18_01.jpg")

    os.remove("sl_r18_01.jpg")
    os.remove("sl_r18_02.jpg")
except FileNotFoundError:
    print("Clearing Data...")

