import datetime
from random import choice
import pyowm
from pyowm.config import DEFAULT_CONFIG
from cfg import API_KEY, LANGUAGE
import wikipediaapi
from translate import Translator

DEFAULT_CONFIG['language'] = LANGUAGE
owm = pyowm.OWM(API_KEY)
mgr = owm.weather_manager()
wikipedia = wikipediaapi.Wikipedia(LANGUAGE)
translator = Translator('en')


def say_weather(city):
    try:
        observation = mgr.weather_at_place(f'{translator.translate(city)},RU')
    except pyowm.commons.exceptions.NotFoundError:
        print(f'>> Города {city} нет в моей базе, извините.')
        return f'Города {city} нет в моей базе, извините.'
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


def say_time():
    print(f">> Сейчас {datetime.datetime.strftime(datetime.datetime.now(), '%H:%M')}")
    return f"Сейчас {datetime.datetime.strftime(datetime.datetime.now(), '%H %M')}"


def say_bye():
    bye = choice(['Всего доброго!', 'Пока!', 'До связи!'])
    print(f">> {bye}")
    return bye


def say_hello():
    hello = choice(['Приветствую!', 'Привет!', 'Здравствуйте!'])
    print(f">> {hello}")
    return hello


def what_it(wiki):
    answer = wikipedia.page(wiki)
    print(f'>> {answer.summary}')
    return answer.summary
