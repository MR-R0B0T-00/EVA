# Модуль для работы с погодой
import pyowm
from pyowm.config import DEFAULT_CONFIG
from access.cfg import API_KEY
from translate import Translator
from google.cloud import dialogflow
import os

DEFAULT_CONFIG['language'] = 'ru'  # Ставим русский язык для погоды
owm = pyowm.OWM(API_KEY)  # API_KEY - ключ для работы с сайтом https://openweathermap.org/
mgr = owm.weather_manager()

translator = Translator('en')  # Гугл переводчик для перевода города с с ru на en

# Если нужно привязать Dialogflow, то потребуется залогиниться через сервис аккаунт
# Скачиваете свой файл json с сайта googlecloud, указываем путь до файла
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'access/google_access.json'
# ID проекта, к которому будем обращаться
PROJECT_ID = 'small-talk-hlcf'
# ID сессии, можно указать любой, формат str
SESSION_ID = 'eva'
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)


# Команда для обработки текущей погоды, принимает город
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


# Принимает запрос для dialogflow
# Возвращает текст ответа и событие
def dialog_flow_answer(text):
    text_input = dialogflow.TextInput(text=text, language_code='ru-RU')
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.display_name
