from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDIconButton, MDFillRoundFlatButton,  MDRectangleFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.dialog import MDDialog


from helpers import query_helper, toolbar_helper, questions_img_I_I

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
crypto_api = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# wolfram alpha API
wolfram_alpha_api = "6QY9X3-HT9G87EVKE"

# jokes API
joke_api = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=religious,racist,sexist,explicit&type=twopart"

# news API
news_api = "59277cccaa8747d0bf618e2a73640776"

# weather API (from weatherbit)
weather_api_key = "3968ed4cab48441c9121711c9171d1fa"

# map API (from MapQuest)
distance_api = "5kz8LN08BnmDCzGGhJrNfGaNyjc6mO9f"


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
        alisa_talk("I did not get that, please try saying that again")
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
def get_temperature(weather_input):
    try:
        response = requests.get("https://api.weatherbit.io/v2.0/current?&city=" + weather_input + "&key=" + weather_api_key)
        weather_data = response.json()

        temperature = weather_data["data"][0]["temp"]
        print(weather_input)
        print(temperature)
        alisa_talk(f"the temperature in {weather_input} is currently {temperature} degrees")
    except KeyError:
        alisa_talk("sorry, invalid location, can you try to say that again?")
        weather_input = alisa_listen()
        if "stop" in weather_input or "no" in weather_input or "ok" in weather_input:  # "by"/"buy"
            alisa_talk("sure, can i help you with anything else?")
            return
        get_temperature(weather_input)


def get_weather(weather_input):
    try:
        response = requests.get("https://api.weatherbit.io/v2.0/current?&city=" + weather_input + "&key=" + weather_api_key)
        weather_data = response.json()

        temperature = weather_data["data"][0]["temp"]
        description = weather_data["data"][0]["weather"]["description"]
        print(weather_input)
        print(temperature)
        print(description)
        alisa_talk(f"its {temperature} degrees and {description}")
    except KeyError:
        alisa_talk("sorry, invalid location, can you try saying that again?")
        weather_input = alisa_listen()
        if "stop" in weather_input or "no" in weather_input or "ok" in weather_input:  # "by"/"buy"
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
def wikipedia_search(text):
    try:
        wiki_result = wikipedia.summary(text, sentences=1)

        dialog = MDDialog(
            text=f"• {wiki_result}",
            radius=[50, 20, 50, 20]
        )
        dialog.open()

        print(wiki_result)
        alisa_talk(wiki_result)
    except IndexError:
        alisa_talk("data not available")
    except wikipedia.exceptions.PageError:
        alisa_talk("data not available")


# opening websites
def open_youtube():
    alisa_talk("sure, opening youtube")
    webbrowser.open("www.youtube.com")
    return


def open_gmail():
    alisa_talk("sure, opening gmail")
    webbrowser.open("www.gmail.com")
    return


def open_googledrive():
    alisa_talk("sure, opening google drive")
    webbrowser.open("www.drive.google.com")
    return


def open_googlemaps():
    alisa_talk("sure, opening google maps")
    webbrowser.open("www.googlemaps.com")
    return


# opening applications
def open_chrome():
    alisa_talk("sure, opening chrome")
    os.system("start chrome")
    return


# def open_notepad():
#     alisa_talk("sure, opening notepad")
#     os.system("Notepad")
#     return
#
#
# def open_cmd():
#     alisa_talk("sure, opening command prompt")
#     os.system("start cmd")
#     return


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


def alisa_reply(text):

    # # small talk

    if "your" in text and "name" in text:
        alisa_talk("hi, my name is alisa, how can i help you?")

    elif "thanks" in text or "thank you" in text:
        alisa_talk("you're welcome, can i help you with anything else?")

    # elif "yes" in text:
    #     alisa_talk("okay, how can i help you?")

    # hi/hello/hai alisa
    elif "hi" in text or "hai" in text or "hello" in text:
        alisa_talk("hello, how can i help you?")

    elif "you" in text and "stupid" in text:
        alisa_talk("well, I think i am pretty smart!")

    elif "favourite" in text or "favorite" in text and "movie" in text:
        alisa_talk("my favourite movie is, a silent voice. I watch it with my friends all the time")

    # # Cryptocurrency prices - bitcoin

    elif "bitcoin" in text:
        response = requests.get(url=crypto_api)
        crypto_data = response.json()
        bitcoin_price = float(crypto_data["price"])
        print(bitcoin_price)

        alisa_talk(f"the current price of bitcoin is, {bitcoin_price} rupees")

    # # Stocks - Apple/amazon/tesla

    elif "apple" in text:
        apple = yf.Ticker("AAPL")
        apple_stock_price = apple.info['regularMarketPrice']
        print(apple_stock_price)

        alisa_talk(f"currently you can purchase apple share for, {apple_stock_price} US dollars")

    elif "amazon" in text:
        amazon = yf.Ticker("AMZN")
        amazon_stock_price = amazon.info['regularMarketPrice']
        print(amazon_stock_price)

        alisa_talk(f"currently you can purchase amazon share for, {amazon_stock_price} US dollars")

    elif "tesla" in text:
        tesla = yf.Ticker("TSLA")
        tesla_stock_price = tesla.info['regularMarketPrice']
        print(tesla_stock_price)

        alisa_talk(f"currently you can purchase tesla share for, {tesla_stock_price} US dollars")

    # wolfram alpha api - capital of a country
    elif "capital" in text and "of" in text:
        wolfram_alpha_country_capital(text)

    # wolfram alpha api - calculations
    elif "+" in text or "-" in text or "x" in text or "/" in text or "log" in text or "root" in text or "power" in text or "percent" in text or "average" in text:
        wolfram_alpha_calculator(text)

    # wolfram alpha api - president of a certain country
    elif "president" in text and "of" in text:
        wolfram_alpha_president(text)

    # wolframalpha - airports
    elif "airport" in text:
        wolfram_alpha_airport(text)

    # # translator - japanese
    elif "translate" in text and "japanese" in text:
        alisa_talk("sure")
        translator_japanese(text)

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
        weather_input = alisa_listen()
        get_temperature(weather_input)

    # weather - weather
    elif "weather" in text:
        alisa_talk("sure, what is your current location")
        weather_input = alisa_listen()
        print(weather_input)
        get_weather(weather_input)

    # distance
    elif "distance" in text:
        alisa_talk("sure, what is the starting point")
        from_location = alisa_listen()
        alisa_talk("alright, what is the destination point")
        to_location = alisa_listen()
        alisa_talk("okey, a moment please")

        distance_info(from_location, to_location)

    # wikipedia search
    elif "driver" in text or "drive" in text or "google drive" in text:
        open_googledrive()

    elif "what" in text or "who" in text or "where" in text or "why" in text or "define" in text or "describe" in text or "how" in text:
        wikipedia_search(text)

    # opening websites
    elif "google" in text or "browser" in text or "chrome" in text:
        open_chrome()

    elif "youtube" in text or "you tube" in text:
        open_youtube()

    elif "gmail" in text or "mail" in text:
        open_gmail()

    elif "map" in text or "maps" in text:
        open_googlemaps()

    # opening applications
    # elif "note" in text or "notepad" in text:
    #     open_notepad()
    #
    # elif "cmd" in text or "command prompt" in text or "terminal" in text:
    #     open_cmd()

    # date and time
    elif "time" in text:
        time_now()

    elif "day" in text or "weekday" in text:
        current_weekday()

    # updating user name
    elif ("change" in text or "update" in text) and "name" in text:
        alisa_talk("can you tell me your name?")
        updated_name = alisa_listen()
        with open("name.txt", 'w') as name:
            name.write(updated_name)
        print(updated_name)
        alisa_talk(f"sure, user name updated to {updated_name}")

    # imp questions search
    elif ("1st year" in text or "first year" in text or "year 1" in text) and (
                    "1st semester" in text or "first semester" in text or "semester 1" in text):
        alisa_talk("sure")

    # breaking loop
    elif "goodbye" in text or "bye" in text or "stop" in text or "no" in text or "ok" in text:  # "by"/"buy"
        alisa_talk("it was my pleasure, see you again")

    # unknown value or wait time exceeded
    else:
        alisa_talk("Please Repeat")


# self.theme_cls.primary_palette = "Green"
# self.theme_cls.primary_hue = "A700"


class assistant(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Screen()

    def build(self):

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
        print(self.query.text)
        if ("1st year" in self.query.text or "first year" in self.query.text or "year 1" in self.query.text) and (
                    "1st semester" in self.query.text or "first semester" in self.query.text or "semester 1" in self.query.text):
            alisa_talk("sure")
            self.questions_1_1_img()
        else:
            alisa_reply(self.query.text)

    def questions_1_1_img(self):
        self.screen.clear_widgets()
        next_screen = Builder.load_string(questions_img_I_I)
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
            alisa_reply(listen_alisa)

            if ("1st year" in listen_alisa or "first year" in listen_alisa or "year 1" in listen_alisa) and (
                    "1st semester" in listen_alisa or "first semester" in listen_alisa or "semester 1" in listen_alisa):
                self.questions_1_1_img()
                break

            elif "goodbye" in listen_alisa or "bye" in listen_alisa or "stop" in listen_alisa or "no" in listen_alisa or (
                    "ok" in listen_alisa and "thank you" not in listen_alisa and "thanks" not in listen_alisa):
                break

# firebase implementation down here!


# I - I subjects


class I_I_subjects_img(Screen):
    pass


class I_I_mathematics_questions_img(Screen):
    pass


class I_I_chemistry_questions_img(Screen):
    pass


class I_I_electrical_engineering_questions_img(Screen):
    pass


class I_I_english_questions_img(Screen):
    pass


# I - II subjects (pending!...)

# II - I subjects (pending!...)

# II - II subjects (pending!...)

# III - I subjects (pending!...)

# III - II subjects (pending!...)


sm = ScreenManager()
# year - I sem- I
sm.add_widget(I_I_subjects_img(name="subjects_I_I_img"))
sm.add_widget(I_I_mathematics_questions_img(name="mathematics_img"))
sm.add_widget(I_I_chemistry_questions_img(name="chemistry_img"))
sm.add_widget(I_I_electrical_engineering_questions_img(name="electrical_engineering_img"))
sm.add_widget(I_I_english_questions_img(name="english_img"))

# year - I sem - II (pending!...)

# year - II sem - I (pending!...)

# year - II sem - II (pending!...)

# year - III sem - I (pending!...)

# year - III sem - II (pending!...)

assistant().run()

