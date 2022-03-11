import pyowm
from pyowm.config import DEFAULT_CONFIG
from access.cfg import API_KEY
from translate import Translator

DEFAULT_CONFIG['language'] = 'ru'  # Ставим русский язык для погоды
owm = pyowm.OWM(API_KEY)  # API_KEY - ключ для работы с сайтом https://openweathermap.org/
mgr = owm.weather_manager()

translator = Translator('en')  # Гугл переводчик для перевода города с с ru на en


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
