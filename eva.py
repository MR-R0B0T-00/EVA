# Импорт необходимых библиотек
from random import choice
import sys
import speech_recognition as sr
import pyttsx3
import time
import re
import datetime


eva = pyttsx3.init()
recognizer = sr.Recognizer()
microphone = sr.Microphone()


def set_voice():
    eva.setProperty('rate', 200)
    eva.setProperty('volume', 1)


def speak(what):
    eva.say(what)
    eva.runAndWait()
    eva.stop()


# Обработка команд
def commands(text):
    # Системное время
    if text == 'ева':
        speak('Слушаю, хозяин!')
    elif re.findall('время|времени|часы|часов', text):
        print(f">> Время {datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')}")
        speak(datetime.datetime.strftime(datetime.datetime.now(), '%H %M'))
    # Завершение программы
    elif re.findall('пока|до свидания|отключись|стоп', text):
        answer = choice(['Всего доброго!', 'Пока!', 'До связи!'])
        print(f'>> {answer}')
        speak(answer)
        sys.exit()
    elif re.findall('привет|здарово|хай|здравствуй', text):
        answer = choice(['Приветствую!', 'Привет!', 'Здравствуйте!'])
        print(f'>> {answer}')
        speak(answer)
    else:
        print(text)
        speak(text)


def eva_run():
    while True:
        # Слушаем микрофон
        with microphone as source:
            print('>> Говорите, я слушаю.')
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_vosk(audio, language='ru_RU').lower()
                commands(text)
            except sr.UnknownValueError:
                # Если не разобрали
                speak('Повторите, пожалуйста!')
            time.sleep(0.1)


set_voice()
eva_run()
