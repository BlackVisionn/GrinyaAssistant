# Голосовой ассистент Гриша
import os
import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
 
# настройки
opts = {
    "alias": ('гриша','григорий','гриня','гриш'),    
    "cmds": {
        "music": ('включи музыку', 'музыку'),
        "ctime": ('текущее время','сейчас времени','который час'),
        "browser": ('браузер','яндекс'),        
    }
}
 
# функции
def speak(what):
    print( what )
    speak_engine.say( what )
    speak_engine.runAndWait()
    speak_engine.stop()
 
def callback(recognizer, audio):
    try:
        voice = recognizer.recognize_google(audio, language = "ru-RU").lower()
        print("[log] Распознано: " + voice)
    
        if voice.startswith(opts["alias"]):
            # обращаются к Грише
            cmd = voice
 
            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()
            
            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])
 
    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")

        print("print")
 
def recognize_cmd(cmd):
    RC = {'cmd': '', 'percent': 0}
    for c,v in opts['cmds'].items():
 
        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    
    return RC
 
def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    
    elif cmd == 'browser':
        # открыть браузер
        os.system("C:\\Users\\black\AppData\\Local\\Yandex\\YandexBrowser\\Application\\browser.exe")
    
    elif cmd == 'music':
        os.system ("C:\\Users\\black\\AppData\\Roaming\\Spotify\\Spotify.exe")
       
    else:
        print('Команда не распознана, повторите!')
 
# запуск
r = sr.Recognizer()
m = sr.Microphone(device_index = 1)
 
with m as source:
    r.adjust_for_ambient_noise(source)
 
speak_engine = pyttsx3.init()
 
speak("Добрый день, Гриша слушает")
 
stop_listening = r.listen_in_background(m, callback)
while True: time.sleep(0.1) # infinity loop