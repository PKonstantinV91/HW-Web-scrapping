import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import re
import pprint
import json


HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def get_headers():
    headers = Headers(browser='firefox', os='win').generate()
    return headers


def find_true_info(text):
    pattern = r"(.*django.*flask.*)|(.*flask.*django.*)"
    result = re.findall(pattern, text, flags=re.I)
    return result


hh_vacancy_html = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(hh_vacancy_html, features='lxml')
vacancy_list_tag = soup.find(id='a11y-main-content')

vacancy_tags = vacancy_list_tag.find_all(class_='vacancy-serp-item__layout')

vacancy_list = []

for vacancy in vacancy_tags:
    vacancy_href = vacancy.find('a', class_='serp-item__title')['href']
    description_html = requests.get(vacancy_href, headers=get_headers()).text
    soup1 = BeautifulSoup(description_html, features="lxml")
    description_body = soup1.find('div', class_="vacancy-section").text
    if len(find_true_info(description_body)) > 0:
        vacancy_name_company = vacancy.find('a', class_='bloko-link').text
        vacancy_city = vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
        vacancy_salary = vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
        if vacancy_salary:
            vs = vacancy_salary.text
        else:
            vs = '-'
        vacancy_list.append({
            'link': vacancy_href,
            'salary': vs,
            'name_company': vacancy_name_company,
            'city': vacancy_city
        })


pprint.pprint(vacancy_list)
with open(r"Vacancy.json", 'w', encoding='utf-8') as f:
        json.dump(vacancy_list, f, ensure_ascii=False,  indent=2)