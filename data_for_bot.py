from black_database import BlackDataBase


class DataForBot:
    smiley_good = '\U0001F436'
    smiley_bad = '\U0001F489'
    smiley_working = '\U0001F64F'
    test_good = '<b>НЕ ТЕСТИРУЮТ</b>'
    test_bad = '!!!<b>ТЕСТИРУЮТ</b>!!!'
    test_working = '!<b>ПЕРЕСТАЮТ ТЕСТИРОВАТЬ</b>!'

    bad_string_s_t_s = str(smiley_bad + ' ' + test_bad + ' ' + smiley_bad)
    good_string_s_t_s = str(smiley_good + ' ' + test_good + ' ' + smiley_good)
    working_string_s_t_s = str(smiley_working + ' ' + test_working + ' ' + smiley_working)

    def __init__(self, name: str):
        self.name = name

    def correct_name(self):
        correct_name = [m for m in self.name if m != '\'']
        self.name = ''.join(correct_name)
        if len(self.name) <= 2:
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

    def answer_for_one(self, name: str, test_company: str):

        if test_company == 'No':
            return f'Компания {name}\n{self.good_string_s_t_s}\nсвою продукцию на животных!'

        elif test_company == 'Yes':
            return f'Компания {name}\n{self.bad_string_s_t_s}\nсвою продукцию на животных!'

        else:
            return f'Компания {name}\n{self.working_string_s_t_s}\nсвою продукцию на животных!'

    def sorted_tests(self, list_of_companies: list):
        yes_test = []
        no_test = []
        working_test = []

        for name, test in list_of_companies:

            if test == 'No':
                no_test.append(name)

            elif test == 'Yes':
                yes_test.append(name)

            else:
                working_test.append(name)

        return self.correct_answer_for_several(yes_test, no_test, working_test)

    def correct_answer_for_several(self, yes_test: list, no_test: list, working_test: list):
        yes = f'\n\n{self.smiley_bad}'.join(yes_test)
        no = f'\n\n{self.smiley_good}'.join(no_test)
        working = f'\n\n{self.smiley_working}'.join(working_test)

        if yes == '':
            yes = None
        elif no == '':
            no = None
        elif working == '':
            working = None

        return self.answer_for_several(yes, no, working)

    def answer_for_several(self, yes: str, no: str, working: str):
        start_phrase = 'По вашему запросу найдено несколько компаний:'

        if no is not None \
                and yes is None \
                and working is None:
            return f'{start_phrase}\n\nВсе бренды, подходящие под запрос,' \
                   f'\n{self.good_string_s_t_s}\n' \
                   f'свою продукцию на животных!\n\n' \
                   f'{self.smiley_good}{no}'

        elif yes is not None \
                and no is None \
                and working is None:
            return f'{start_phrase}\nВсе бренды, подходящие под запрос,' \
                   f'\n{self.bad_string_s_t_s}\n' \
                   f'свою продукцию на животных!\n\n' \
                   f'{self.smiley_bad}{yes}'

        elif working is not None \
                and no is None \
                and yes is None:
            return f'{start_phrase}\nВсе бренды, подходящие под запрос,' \
                   f'\n{self.working_string_s_t_s}\n' \
                   f'свою продукцию на животных!\n\n' \
                   f'{self.smiley_working}{working}'

        elif yes is not None \
                and no is not None \
                and working is None:
            return f'{start_phrase}\n\n' \
                   f'Бренды, которые {self.good_string_s_t_s}:\n\n' \
                   f'{self.smiley_good}{no}\n\n\n' \
                   f'Бренды, которые {self.bad_string_s_t_s}:\n\n' \
                   f'{self.smiley_bad}{yes}\n\n'

        elif yes is not None \
                and working is not None \
                and no is None:
            return f'{start_phrase}\n\n' \
                   f'Бренды, которые {self.working_string_s_t_s}:\n\n' \
                   f'{self.smiley_working}{working}\n\n\n' \
                   f'Бренды, которые {self.bad_string_s_t_s}:\n\n' \
                   f'{self.smiley_bad}{yes}\n\n'

        elif no is not None \
                and working is not None \
                and yes is None:
            return f'{start_phrase}\n\n' \
                   f'Бренды, которые {self.working_string_s_t_s}:\n\n' \
                   f'{self.smiley_working}{working}\n\n\n' \
                   f'Бренды, которые {self.good_string_s_t_s}:\n\n' \
                   f'{self.smiley_good}{no}\n\n'

        else:
            return f'{start_phrase}\n\n' \
                   f'Бренды, которые {self.working_string_s_t_s}:\n\n' \
                   f'{self.smiley_working}{working}\n\n\n' \
                   f'Бренды, которые {self.good_string_s_t_s}:\n\n' \
                   f'{self.smiley_good}{no}\n\n' \
                   f'Бренды, которые {self.bad_string_s_t_s}:\n\n' \
                   f'{self.smiley_bad}{yes}\n\n'

    @staticmethod
    def answer_for_none():
        return 'Бот не нашел такую компанию в \"Черном\" или \"Белом\" списке.\n' \
               'Это может быть из-за того, что компанию пока нельзя отнести ни к одному из списков или из-за некоректного ввода.'


if __name__ == '__main__':
    a = DataForBot('estee')
    print(a.correct_name())
