# Импорт необходимых библиотек
import sys
import speech_recognition as sr
import pyttsx3
import re
import commands

eva = pyttsx3.init()
eva.setProperty('rate', 200)
eva.setProperty('volume', 1)

recognizer = sr.Recognizer()
microphone = sr.Microphone()


def speak(what):
    eva.say(what)
    eva.runAndWait()
    eva.stop()


def listing_microphone():
    with microphone as source:
        print('>> Говорите, я слушаю.')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        return audio


def command_handler(text):
    if re.findall('пока', text):
        speak(commands.say_bye())
        sys.exit()
    elif re.findall('привет|здравствуй', text):
        speak(commands.say_hello())
    elif re.findall('погод', text):
        while True:
            print('>> В каком городе Вы сейчас находитесь?')
            speak('В каком городе Вы сейчас находитесь?')
            city = recognizer.recognize_vosk(listing_microphone(), language='ru_RU').capitalize()
            if city:
                speak(commands.say_weather(city))
                break
            else:
                print('>> Извините, я Вас не слышу повторите пожалуйста')
                speak('Извините, я Вас не слышу повторите пожалуйста')
    elif text.startswith('узнать про'):
        speak(commands.what_it(text[11:]))


def eva_run():
    while True:
        try:
            text = recognizer.recognize_vosk(listing_microphone(), language='ru_RU').lower()
            command_handler(text)
        except sr.UnknownValueError:
            speak('Повторите, пожалуйста!')


print('>> Вас приветствует обучаемый голосовой ассистент ЕВА.')
speak('Вас приветствует обучаемый голосовой ассистент ЕВА.')

eva_run()
