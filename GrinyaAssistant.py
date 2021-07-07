import speech_recognition as sr
import pyttsx3
from fuzzywuzzy import fuzz
from datetime import datetime
import random
import sys
from os import system
import webbrowser
import requests
import re


ndel = ['гриша', 'григорий', 'гриня', 'гриш', 'гришаня']
 
 
commands = ['текущее время', 'сколько сейчас времени', 'который час',
            'открой браузер', 'открой интернет', 'запусти браузер',            
            'пока', 'выключись','до свидания',
            'найди видео', 'включи видео',
            'покажи команды', 'помощь', 'команды', 'что ты умеешь',
            'найди в браузере', 'поиск', 'найди в интернете',
            'выключи компьютер', 'выруби компьютер', ]
 
 
r = sr.Recognizer()
engine = pyttsx3.init()
text = ''
j = 0
num_task = 0
c = False
 
# Озвучка текста ассистентом 
def talk(speech):
    print(speech)
    engine.say(speech)
    engine.runAndWait()
 
# Нечеткое сравнение сказанной команды со списком команд ассистента
def fuzzy_recognizer(rec):
    global j
    ans = ''
    for i in range(len(commands)):
        k = fuzz.ratio(rec, commands[i])
        if (k > 70) & (k > j):
            ans = commands[i]
            j = k
    return str(ans)
 
# Вырезание лишних слов
def clear_task():
    global text
    for i in ndel:
        text = text.replace(i, '').strip()
        text = text.replace('  ', ' ').strip()
 
 # Функция прослушивания микрофона и обработки запроса
def listen():
    global text
    text = ''
    with sr.Microphone(device_index=1) as source:        
        print("Жду команду...")
        r.adjust_for_ambient_noise(source)  # Метод для автоматического понижения уровня шума
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ru-RU").lower()
        except sr.UnknownValueError:
            pass
        print(text)
        system('cls')        
        clear_task()
        return text
 
# Обработка сказанной команды
def cmd_init():
    global text
    text = fuzzy_recognizer(text)
    print(text)
    if text in cmds:
        if (text != 'пока') & (text != 'выключись') & (text != 'до свидания'):
            k = ['Секундочку', 'Сейчас сделаю', 'Уже выполняю']
            talk(random.choice(k))
        cmds[text]()
    elif text == '':                
        talk("Команда не распознана")

    engine.runAndWait()
    engine.stop()
 
# Команда вывода текущего времени
def time():
    now = datetime.now()
    talk("Сейчас " + str(now.hour) + ":" + str(now.minute))
 
# Команда открытия браузера
def open_brows():
    webbrowser.open('https://google.com')
    talk("Браузер открыт!")
 
# Команда выключения компьютера
def shut(): 
    global text
    talk("Подтвердите действие!")
    print("Подтверждаю - подтвердить действие.\n Отмена - отменить действие.")
    text = listen()
    print(text)
    if (fuzz.ratio(text, 'подтвердить') > 60) or (fuzz.ratio(text, "подтверждаю") > 60):
        talk('Действие подтверждено')        
        system('shutdown /s /f /t 3')
        quite()
    elif fuzz.ratio(text, 'отмена') > 60:
        talk("Действие не подтверждено")
    else:
        talk("Действие не подтверждено")
 
# Функция приветствия
def hello():
    time = int(datetime.now().hour)
    if time in (6,7,8,9,10,11,12):
        k = 'Доброе утро! Гриша слушает Вас!'
    elif time in (13,14,15,16,17,18):
        k = 'Добрый день! Гриша слушает Вас!'
    elif time in (19,20,21,22,23):
        k = 'Добрый вечер! Гриша слушает Вас!'
    else:
        k = 'Доброй ночи! Гриша слушает Вас!'
        
    talk(k)
    print("Чтобы узнать мой функционал, скажите: помощь, покажи команды, команды, что ты умеешь.")
    
 
# Команда завершения программы
def quite():
    x = ['Надеюсь мы скоро увидимся!', 'Рад был помочь!', 'Я отключаюсь!', 'До новых встреч!', 'Берегите себя и своих близких!']
    talk(random.choice(x))
    engine.stop()
    system('cls')
    sys.exit(0)

# Команда поиска видео
def search_video():
    global text
    talk("Какое видео хотите найти?")
    text = listen()
    print(text)
    if not text: return
    search_term = "".join(text)
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    # с парсером
    talk("Какое видео включить?")
    text = listen()
    print(text)
    if not text: return

    if (int(text) < 8):
        id_videos = parse(url)
        url_video = "https://www.youtube.com/watch?v=" + id_videos[int(text) - 1]
        webbrowser.get().open(url_video)


# Команда поиска в интернете
def search_browser():
    global text
    talk("Что хотите найти?")    
    text = listen()
    print(text)
    if not text: return
    search_term = "".join(text)
    url = "https://www.google.ru/search?q=" + search_term
    webbrowser.get().open(url)

# Команда, которая выводит список команд
def help():
    talk("Вывожу список команд которые могу выполнить...")
    print ("\nУзнать текущее время: текущее время, сколько сейчас времени, который час.\n"
            "Открыть браузер: открой браузер, открой интернет, запусти браузер.\n"
            "Выключить компьютер: выключи компьютер, выруби компьютер.\n"
            "Найти видео: найди видео, включи видео.\n"
            "Выполнить поиск в поисковой строке браузера: найди в браузере, найди в интернете, поиск.\n"
            "Закрыть ассистента: пока, выключись, до свидания.\n") 
cmds = {
    'текущее время': time, 'сколько сейчас времени': time, 'который час': time,
    'открой браузер': open_brows, 'открой интернет': open_brows, 'запусти браузер': open_brows,    
    'пока': quite, 'выключись': quite, 'до свидания': quite,
    'выключи компьютер': shut, 'выруби компьютер': shut,
    'найди видео': search_video, 'включи видео': search_video,
    'найди в браузере': search_browser, 'поиск': search_browser, 'найди в интернете': search_browser,
    'покажи команды':help, 'помощь':help, 'команды':help, 'что ты умеешь':help,
} 

system('cls')


def get_html(input_url):
    response = requests.get(input_url)
    return response


def get_content(html):
    temp = ''.join(html.text)

    result_rx = re.findall(r'\"addedVideoId\":\"[^\"]*\"', temp)

    idvideos = []
    for result_rx_line in result_rx:
        idvideos.append(result_rx_line.split('\"')[3])

    return idvideos


def parse(input_url):
    html = get_html(input_url)
    if html.status_code == 200:
        id_videos = get_content(html)
        return id_videos
        print('ok')
    else:
        print('ERROR')


def main():
    global text, j, c           
    try:
        if c == False:
            c = True       
            hello()

        listen()       

        if text != '':
            cmd_init()
            j = 0

    except UnboundLocalError:
        pass
    except NameError:
        pass
    except TypeError:
        pass


while True:
    main()