import requests
from bs4 import BeautifulSoup
from recording_database import RecordingDataBase


class SearchNames:

    def __init__(self, test: str, num_page: int or str):
        self.test = test
        self.num_page = num_page

    def correct_test(self):
        if self.test == 'dont':
            test = 'No'
            return self.search_on_site(test, self.num_page)
        elif self.test == 'do':
            test = 'Yes'
            return self.search_on_site(test, self.num_page)

    def search_on_site(self, test: str, num_page: int or str):
        url = f'https://crueltyfree.peta.org/companies-{self.test}-test/page/{num_page}/'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        html_code_name = soup.find_all('ul', class_='search-results')
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


