import telebot
import config
import requests
import json
from googletrans import Translator
        
SEARCHERS = {
    "Yandex":"https://ya.ru/search/?text=",
    "Google":"https://www.google.com/search?q=",
    "Youtube":"https://www.youtube.com/results?search_query=",
    "DuckDuckGo":"https://duckduckgo.com/?t=h_&q="
}
NOW_SEARCHER = SEARCHERS["Google"]

bot = telebot.TeleBot(config.TOKEN)
translator = Translator()

def logging(person, message):
    with open("logger.log", "a", encoding="utf-8") as file:
        file.write(f"{person}: {message} \n")

@bot.message_handler(commands=['start'])
def welcome(message):
    logging(message.chat.id, message.text)
    
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name}")
    
@bot.message_handler(commands=['weather'])
def get_weather(message):
    logging(message.chat.id, message.text)
    
    if " " in message.text:
        command, city = message.text.split(maxsplit=1)
    else:
        bot.send_message(message.chat.id, f"Введите город")
        return
        
    result = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={config.API_WEATHER}&units=metric")
    if result.status_code == 200:
        data = json.loads(result.text)
        weather = ""

        for i in range(len(data['weather'])):
            translate = translator.translate(data['weather'][i]['description'], src='en', dest='ru').text
            weather = weather + translate + ", "

        weather = weather[:-2]
        temperature = data['main']['temp']
        temperature_fell_like = data['main']['feels_like']
        wind_speed = data['wind']['speed']

        answer = f"Погода: {weather} \n Температура: {temperature} \n Ощущается как: {temperature_fell_like} \n Скорость ветра: {wind_speed}"
        
    else:
        answer = "город указан не верно"
 
    bot.reply_to(message, answer)

@bot.message_handler(commands=['currency'])
def get_currency(message):
    logging(message.chat.id, message.text)
    
    if " " in message.text:
        command, currency = message.text.split(maxsplit=1)
    else:
        bot.send_message(message.chat.id, f"введите валюту")
        return
    
    with open('exchange rate.json', 'r') as file:
        data = json.load(file)
    
    answer = ""
     
    if currency in data['Valute'].keys():
        answer = f"Номинал: {data['Valute'][currency]['Nominal']}, Курс: {data['Valute'][currency]['Value']} рублей"
    else:
        answer = f"неизвестная валюта"
        
    bot.reply_to(message, answer)
    
@bot.message_handler(commands=['swap_searcher'])
def swap_searcher(message):
    logging(message.chat.id, message.text)
    if " " in message.text:
        command, searcher = message.text.split(maxsplit=1)
    else:
        bot.send_message(message.chat.id, f"Введите поисковую систему")
        return
    global NOW_SEARCHER
    if searcher in SEARCHERS.keys():
        NOW_SEARCHER = SEARCHERS[searcher]
        bot.send_message(message.chat.id, f"сменено на {searcher}") 
    else:
       bot.send_message(message.chat.id, f"неизвестное имя") 
       
@bot.message_handler(commands=['translate'])
def translate(message):
    logging(message.chat.id, message.text)
    if " " in message.text:
        command, searcher = message.text.split(maxsplit=1)
    else:
        bot.send_message(message.chat.id, f"Введите слово или фразу")
        return
    
    translate = translator.translate(searcher, dest='ru').text
    bot.reply_to(message, translate)

@bot.message_handler(content_types=['text'])
def question(message):
    logging(message.chat.id, message.text)
    bot.send_message(message.chat.id, f"{NOW_SEARCHER}{message.text.replace(' ', '+')}")

bot.polling(none_stop=True)
