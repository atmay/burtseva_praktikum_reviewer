# В целом хорошо, но есть, что исправить!

import datetime as dt


class Record:
    # Можно лучше:
    # В последних версиях Питона появилась опция аннотации типов данных.
    # Теперь можно указать ожидаемые на вход и выход типы. Подробнее тут: 
    # https://docs.python.org/3/library/typing.html 
    # Попробуй добавить type hints в свои методы классов!
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        # Можно лучше: 
        # для лучшей читаемости кода можно сначала прописать готовые данные, 
        # которые не надо вычислять, а потом - расчеты. Так проще ничего не упустить.
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        # Надо поправить:
        # по pep8 с большой буквы начинаются имена классов. Переменные пишутся строчными.
        for Record in self.records:
            # Надо поправить:
            # Дату стоит вычислить однократно перед циклом - она не меняется,
            # поэтому нет смысла ее вычислять для каждой записи.
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Надо поправить:
    # Комментарии - полезная вещь, но для описания работы классов, методов и функций есть 
    # более удобный вариант - докстринги (docstring). Добавь их здесь и в остальных классах
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        x = self.limit - self.get_today_stats()
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        # Надо поправить:
        # можно убрать вложенность (else). Если исполнение кода дошло до этого места,
        # значит, лимита по калориям уже не осталось (булочки спасены!)
        else:
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.
    
    # Надо исправить:
    # Курсы валют доступны в пространстве класса, их не нужно передавать
    # К ним можно получить доступ через self - так код чище!
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Можно лучше:
        # Неплохо! Но а что, если валют будет 10? 20? 100?
        # Информацию о валютах можно оформить в виде словаря-справочника,
        # где ключ - currency_type, а значение - постфикс валюты (руб/Euro/)
        # тогда можно будет получить тип валюты за 1 строку
        
        # Надо исправить:
        # В первой проверке ты проверяешь currency, а далее -
        # currency_type. Стоит быть последовательным - код будет логичнее
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Надо исправить
            # Количество "=" имеет значение :)
            # Не путай оператор присваивания и сравнения
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        # Надо исправить
        # Избыточная проверка. Можно либо заменить на else, либо 
        # убрать вложенность - если выполнение дошло до этого места, это
        # единственный вариант.
        elif cash_remained < 0:
            # Можно лучше:
            # В современном Питоне есть очень удобные f-strings! 
            # Попробуй заменить format на них.
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)
    # Надо исправить:
    # Метод get_week_stats уже наследуется от родительского класса Calculator,
    # объявлять или переопределять его тут не нужно.
    def get_week_stats(self):
        super().get_week_stats()
