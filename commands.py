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

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google_access.json'
PROJECT_ID = 'small-talk-hlcf'
SESSION_ID = 'eva'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)


def say_weather(city):
    try:
        observation = mgr.weather_at_place(f'{translator.translate(city)},RU')
    except pyowm.commons.exceptions.NotFoundError:
        print(f'>> Город {city} мне не известен.')
        return f'Город {city} мне не известен.'
    except pyowm.commons.exceptions.InvalidSSLCertificateError:
        print('>> Возможно у Вас неполадки с интернет-соединением. Проверьте и повторите позднее.')
        return 'Возможно у Вас неполадки с интернет соединением. Проверьте и повторите позднее'
    result = f'В городе {city} сейчас: {observation.weather.detailed_status}' \
             f'Температура воздуха: {observation.weather.temperature("celsius")["temp"]:0.0f} по Цельсию' \
             f'Ощущается как: {observation.weather.temperature("celsius")["feels_like"]:0.0f} по Цельсию' \
             f'Скорость ветра: {observation.weather.wind()["speed"]:0.0f} в метрах в секунду.'
    print(f'>> В городе {city} сейчас: {observation.weather.detailed_status}')
    print(f'>> Температура воздуха: {observation.weather.temperature("celsius")["temp"]:0.0f} по Цельсию')
    print(f'>> Ощущается как: {observation.weather.temperature("celsius")["feels_like"]:0.0f} по Цельсию')
    print(f'>> Скорость ветра: {observation.weather.wind()["speed"]:0.0f} в метрах в секунду.')
    return result


def dialog_flow_answer(text):
    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.display_name
