from black_database import BlackDataBase


class DataForBot:

    def __init__(self, name: str):
        self.name = name

    def correct_name(self):
        if '\'' in self.name:
            return 'Символа \" \' \" нет ни в одном названии бренда.'
        elif len(self.name) <= 2:
            return 'Длинна строки слишком маленькая, боту нужно больше символов.'
        else:
            return self.search()

    def search(self):
        b = BlackDataBase('black_database.db', 'blacktable')
        list_of_companies = b.search_by_name(self.name)

        if len(list_of_companies) == 1:
            for name, test in list_of_companies:
                name_str = ''.join(name)
                test_str = ''.join(test)
                return self.answer_for_one(name_str, test_str)

        elif len(list_of_companies) > 1:
            return self.sorted_tests(list_of_companies)

        else:
            return self.answer_for_none()

    @staticmethod
    def answer_for_one(name: str, test_company: str):
        smail_good = '\U0001F436'
        smail_bad = '\U0001F489'
        test_good = '<b>НЕ ТЕСТИРУЕТ</b>'
        test_bad = '!!! ТЕСТИРУЕТ !!!'

        if test_company == 'No':
            return f'Компания {name}\n{smail_good} {test_good} {smail_good}\nсвою продукцию на животных!'

        else:
            return f'Компания {name}\n{smail_bad} {test_bad} {smail_bad}\nсвою продукцию на животных!'

    def sorted_tests(self, list_of_companies: list):
        yes_test = []
        no_test = []

        for name, test in list_of_companies:

            if test == 'No':
                no_test.append(name)

            else:
                yes_test.append(name)

        return self.answer_for_several(yes_test, no_test)

    def answer_for_several(self, yes_test: list, no_test: list):
        start_phrase = 'По вашему запросу найдено несколько компаний:'
        smail_good = '\U0001F436'
        smail_bad = '\U0001F489'

        yes = f'\n\n{smail_bad}'.join(yes_test)
        no = f'\n\n{smail_good}'.join(no_test)

        test_good = '<b>НЕ ТЕСТИРУЮТ</b>'
        test_bad = '<b>!!! ТЕСТИРУЮТ !!!</b>'

        if len(yes_test) < 2 and len(no_test) > 2:
            return f'{start_phrase}\n\nВсе бренды, подходящие под запрос,' \
                   f'\n{smail_good} {test_good} {smail_good}\n' \
                   f'свою продукцию на животных!\n\n' \
                   f'{smail_good}{no}'

        elif len(no_test) < 2 and len(yes_test) > 2:
            return f'{start_phrase}\nВсе бренды, подходящие под запрос,' \
                   f'\n{smail_bad} {test_bad} {smail_bad}\n' \
                   f'свою продукцию на животных!\n\n' \
                   f'{smail_bad}{yes}'
        else:
            return f'{start_phrase}\n\n' \
                   f'Бренды, которые {smail_good} {test_good} {smail_good}:\n\n' \
                   f'{smail_good}{no}\n\n\n' \
                   f'Бренды, которые {smail_bad} {test_bad} {smail_bad}:\n\n' \
                   f'{smail_bad}{yes}\n\n'

    @staticmethod
    def answer_for_none():
        return 'Бот не нашел такую компанию в \"Черном\" или \"Белом\" списке.\n' \
               'Это может быть из-за того, что компанию пока нельзя отнести ни к одному из списков или из-за некоректного ввода.'


