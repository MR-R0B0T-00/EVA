import pyowm
from pyowm.config import DEFAULT_CONFIG
from cfg import API_KEY
from translate import Translator
from google.cloud import dialogflow
import os

DEFAULT_CONFIG['language'] = 'ru'
owm = pyowm.OWM(API_KEY)
mgr = owm.weather_manager()
translator = Translator('en')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'small-talk-hlcf-c4d492b1181c.json'
session_client = dialogflow.SessionsClient()
session = session_client.session_path('small-talk-hlcf', 'eva')


def say_weather(city):
    try:
        observation = mgr.weather_at_place(f'{translator.translate(city)},RU')
    except pyowm.commons.exceptions.NotFoundError:
        print(f'>> Города {city} нет в моей базе, извините.')
        return f'Города {city} нет в моей базе, извините.'
    except pyowm.commons.exceptions.InvalidSSLCertificateError:
        print('>> Возможно у Вас неполадки с интернет-соединением. Проверьте и повторите позднее.')
        return 'Возможно у Вас неполадки с интернет соединением. Проверьте и повторите позднее'
    w = observation.weather
    result = f'В городе {city} сейчас: {w.detailed_status}' \
             f'Температура воздуха: {round(w.temperature("celsius")["temp"])} по Цельсию' \
             f'Ощущается как: {round(w.temperature("celsius")["feels_like"])} по Цельсию' \
             f'Скорость ветра: {round(w.wind()["speed"])} метра в секунду.'
    print(f'>> В городе {city} сейчас: {w.detailed_status}')
    print(f'>> Температура воздуха: {round(w.temperature("celsius")["temp"])} по Цельсию')
    print(f'>> Ощущается как: {round(w.temperature("celsius")["feels_like"])} по Цельсию')
    print(f'>> Скорость ветра: {round(w.wind()["speed"])} метра в секунду.')
    return result


def dialog_flow_answer(text):
    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.display_name
