# Импорт необходимых библиотек
from random import choice
import sys
import speech_recognition as sr
import pyttsx3
import time
import re
import requests
import datetime


# Инициализация приложения
eva = pyttsx3.init()
voices = eva.getProperty('voices')
# Выбор голоса системы, если ругается
# Укажите 0 или 1
eva.setProperty('voice', voices[0].id)


# Функция для воспроизведения речи
def speak(what):
    eva.say(what)
    eva.runAndWait()
    eva.stop()


# Обработка команд
def commands(text):
    # Погода, можно настроить свой город
    # В конце ссылки просто поменять на нужный
    if re.findall('погода|погоде|на улице|погодка', text):
        print('О погоде')
        weather = requests.get('https://yandex.ru/pogoda/astrahan')
        bs = BeautifulSoup(weather.text, 'html.parser')
        speak(bs.find('div', 'header-title header-title_in-fact').h1.text)
        speak('Температура' + bs.find('div', 'temp fact__temp fact__temp_size_s').find('span', 'temp__value').text + 'градусов')
        speak('Ощущается как' + bs.find('div', 'term term_orient_h fact__feels-like').find('span', 'temp__value').text)
        speak(bs.find('div', 'link__condition day-anchor i-bem').text)
        speak('Скорость ветра' + bs.find('span', 'wind-speed').text + 'метров в секунду')
    # Системное время
    elif re.findall('время|времени|часы|часов', text):
        print(f"Время {datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')}")
        speak(datetime.datetime.strftime(datetime.datetime.now(), '%H %M'))
    # Завершение программы
    elif re.findall('пока|до свидания|отключись|стоп', text):
        answer = choice(['Всего доброго!', 'Пока!', 'До связи!'])
        print(answer)
        speak(answer)
        sys.exit()
    # Подключаемся к DialogFlow от Google
    else:
        # Вводим свой токен

        request = apiai.ApiAI(CONFIG_SET['token']).text_request()
        request.lang = 'ru'
        request.session_id = 'EVA'
        request.query = text
        response = json.loads(request.getresponse().read().decode('utf-8'))
        print(response)
#        resp = response['result']['fulfillment']['speech']

        if resp:
            print(resp)
            speak(resp)
        else:
            # Если ничего не вернулось
            print('Не понятно')
            speak('Я не совсем поняла!')


r = sr.Recognizer()
m = sr.Microphone()


def irina_run():
    while True:
        # Слушаем микрофон
        with m as source:
            print('Говорите, я слушаю.')
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            try:
                text = r.recognize_vosk(audio, language='ru_RU').lower()
                commands(text)
            except sr.UnknownValueError:
                # Если не разобрали
                print('Я вас не понимаю, повторите!')
                speak('Я вас не понимаю, повторите!')
            time.sleep(0.1)


irina_run()
