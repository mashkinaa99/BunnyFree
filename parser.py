import requests
from bs4 import BeautifulSoup
from recording_database import RecordingDataBase


class SearchNames:
    original_url = 'https://crueltyfree.peta.org/'
    url = ''
    test = ''

    def start(self):
        test_on_animals = ['working-for-regulatory-change', 'do-test', 'dont-test']
        for test in test_on_animals:
            self.url = self.original_url
            self.test = test
            self.parse_num_of_pages()

    def parse_num_of_pages(self):
        self.url += 'companies-' + self.test + '/'

        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        pages = soup.select('.pagination > li')
        last_page = 2
        if len(pages) != 0:
            last_page = int(pages[len(pages) - 2].text)

        return self.search_on_pages(last_page)

    def search_on_pages(self, last_page):
        for page_number in range(1, last_page):
            self.search_on_page(page_number)

    def search_on_page(self, num_page: int):
        url = f'{self.url}page/{num_page}/'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        html_code_name = soup.find_all('ul', class_='search-results')

        test = ''
        if self.test == 'dont-test':
            test = 'No'
        elif self.test == 'do-test':
            test = 'Yes'
        elif self.test == 'working-for-regulatory-change':
            test = 'Working'

        for tags in html_code_name:
            return self.normal_name(tags, test)

    @staticmethod
    def normal_name(tags, test: str):
        tags_title = []
        tags_text = tags.text.strip().split('\n')
        for tag in tags_text:
            if len(tag) < 2:
                del tag
            else:
                tags_title.append(tag)
        return RecordingDataBase(tags_title, test).recording_base()

