# Импорт необходимых библиотек
import sys
import speech_recognition as sr
import pyttsx3
import time
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


def command_handler(text):
    if re.findall('время|времени|часы|часов', text):
        speak(commands.say_time())
    elif re.findall('пока|до свидания|отключись|стоп', text):
        speak(commands.say_bye())
        sys.exit()
    elif re.findall('привет|здарово|хай|здравствуй', text):
        speak(commands.say_hello())
    elif text == 'что ты умеешь':
        speak(commands.listing_commands())


def eva_run():
    while True:
        # Слушаем микрофон
        with microphone as source:
            print('>> Говорите, я слушаю.')
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_vosk(audio, language='ru_RU').lower()
                command_handler(text)
            except sr.UnknownValueError:
                # Если не разобрали
                speak('Повторите, пожалуйста!')
            time.sleep(0.1)


print('>> Вас приветствует обучаемый голосовой ассистент ЕВА.')
speak('Вас приветствует обучаемый голосовой ассистент ЕВА.')
print('>> Спросите "что ты умеешь?" и получите листинг моих команд.')
speak('Спросите "что ты умеешь?" и получите листинг моих команд.')
eva_run()
