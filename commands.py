import datetime
from random import choice


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


def listing_commands():
    print('>> Пока я умею, здороваться, прощаться и подсказывать время, в будущем команд будет больше.')
    return 'Пока я умею, здороваться, прощаться и подсказывать время, в будущем команд будет больше.'
