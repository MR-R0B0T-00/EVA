import sys
import speech_recognition as sr
import pyttsx3
import commands
import google

eva = pyttsx3.init()
eva.setProperty('rate', 200)
eva.setProperty('volume', 1)

recognizer = sr.Recognizer()
microphone = sr.Microphone()


def speak(what):
    eva.say(what)
    eva.runAndWait()
    eva.stop()


def text_from_microphone():
    with microphone as source:
        print('>> Я слушаю.')
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        return recognizer.recognize_vosk(audio, language='ru_RU')


def command_handler(text):
    try:
        answer = commands.dialog_flow_answer(text)
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
                city = text_from_microphone().capitalize()
                if city:
                    speak(commands.say_weather(city))
                    break
                else:
                    print('>> Повторите, пожалуйста, город.')
                    speak('Повторите, пожалуйста, город')
    except google.api_core.exceptions.InvalidArgument:
        pass
    except google.api_core.exceptions.RetryError:
        print('>> Проблемы с интернет-соединением.')
        speak('Проблемы с интернет-соединением')


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
