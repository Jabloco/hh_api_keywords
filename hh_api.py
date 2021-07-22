# Библиотека для работы с HTTP-запросами. Будем использовать ее для обращения к API HH

import requests
 
# Пакет для удобной работы с данными в формате json
import json
 
# Модуль для работы со значением времени
import time
 
# Модуль для работы с операционной системой. Будем использовать для работы с файлами
# import os
 
  
def getPage(page = 0):
    """
    Создаем функцию для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
     
    # Справочник для параметров GET-запроса
    params = {
        'text': 'NAME:python junior', # Текст фильтра. В имени должно быть слово "Аналитик"
        'page': page, # Индекс страницы поиска на HH
        'per_page': 2 # Кол-во вакансий на 1 странице
    }
     
    req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data


def vacancy_detail(url_list):

    """
    Функция для создания списка вакансий с детализацией
    Аргументы:
        url_list - список ссылок на вакансии
    """

    vacancy_detail_list = []
    for url in url_list:
        req = requests.get(url)
        data = json.loads(req.content.decode())
        req.close()
        vacancy_detail_list.append(data)
    return vacancy_detail_list

def remote_symbol(s):
    """
    Функция удаления тэгов и знаков препинания.
    Аргументы:
        s - строка
    """
    symbol_lst = ['<p>', '</p>', '<li>', '</li>', '<ul>', '</ul>', '<em>', '</em>', '<strong>', '</strong>', '(', ')', ',', '.', ';', ':']

    for symbol in symbol_lst:
        s = s.replace(symbol, '')
    return s

    
# получаем список ссылок на вакансии
url_list = []
for page in range(1):

    # ****** Запись сроки ответа в файл для разбора структуры json
    # js = getPage(page)
    # with open('hh_vac', 'w', encoding='utf8') as w:
    #     w.write(js)
    # *****
    
    js = json.loads(getPage(page)) # Преобразуем текст ответа запроса в словарь Python
    
    for i in range(len(js['items'])):
        url_list.append(js['items'][i]['url'])

    
    if (js['pages'] - page) <= 1: # Проверка на последнюю страницу если вакансий меньше чем в диапазоне цикла
        break
     
    
    time.sleep(0.25) # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать

print(url_list)

print(vacancy_detail(url_list)[0].keys())
print(vacancy_detail(url_list)[0]['description'])
print(vacancy_detail(url_list)[0]['key_skills'])



