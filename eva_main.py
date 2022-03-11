import sys
import speech_recognition as sr  # Перевод речи в текст
import pyttsx3  # Перевод текста в речь
import dialogflow_text
import google  # Модуль для работы Dialogflow от Google
from say_weather import say_weather

# Инициализация голоса
eva = pyttsx3.init()
eva.setProperty('rate', 200)
eva.setProperty('volume', 1)

# Инициализация микрофона
recognizer = sr.Recognizer()
microphone = sr.Microphone()


# Функция текст в голос, в параметр "what" передаем  текст
def speak(what):
    eva.say(what)
    eva.runAndWait()
    eva.stop()


# Функция распознавания голоса в текст
def text_from_microphone():
    # Запись с микрофона
    with microphone as source:
        print('>> Я слушаю.')
        recognizer.adjust_for_ambient_noise(source)
        # Слушаем только 5 сек
        audio = recognizer.listen(source, phrase_time_limit=5)
        # Возвращаем текст, преобразуем с помощью Vosk (работает оффлайн)
        return recognizer.recognize_vosk(audio, language='ru')


# Прослушивание команд
def command_handler(text):
    if text == 'ева':
        speak('Я слушаю')
        text = text_from_microphone()
    # Для dialogflow
        try:
            answer = dialogflow_text.dialog_flow_answer(text)
            if answer[0]:
                print(f'>> {answer[0]}')
                speak(answer[0])
            else:
                print('>> Повторите, пожалуйста.')
                speak('Повторите, пожалуйста')
            if answer[1] == 'smalltalk.greetings.bye':
                sys.exit()
            elif answer[1] == 'smalltalk.agent.say_weather':
                while True:
                    # Команда для обработки погоды
                    city = text_from_microphone().capitalize()
                    if city:
                        speak(say_weather(city))
                        break
                    else:
                        print('>> Повторите, пожалуйста, город.')
                        speak('Повторите, пожалуйста, город')
        except google.api_core.exceptions.InvalidArgument:
            pass
        except google.api_core.exceptions.RetryError:
            print('>> Проблемы с интернет-соединением.')
            speak('Проблемы с интернет-соединением')


# Основная функция работы
def eva_run():
    print('>> Обучаемый голосовой ассистент EVA <<')
    print('*' * 39)
    while True:
        try:
            command_handler(text_from_microphone().lower())
        except sr.UnknownValueError:
            print('>> Повторите, пожалуйста!')
            speak('Повторите, пожалуйста!')
        print('*' * 39)


if __name__ == '__main__':
    eva_run()
