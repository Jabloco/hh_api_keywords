
import requests
import json
import time
from string import ascii_letters


def getPage(page = 0):
    """
    Создаем функцию для получения страницы со списком вакансий.
    Аргументы:
        page - Индекс страницы, начинается с 0. Значение по умолчанию 0, т.е. первая страница
    """
    # Словарь для параметров GET-запроса
    params = {
        'text': 'NAME:python junior', # Текст фильтра. В имени должно быть слово "Аналитик"
        'page': page, # Индекс страницы поиска на HH
        'per_page': 100 # Кол-во вакансий на 1 странице
    }
     
    req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data

def remote_symbol(input_str):
    """
    Функция удаления тэгов и знаков препинания.
    Аргументы:
        s - строка
    """
    symbol_lst = ['<p>', '</p>', '<li>', '</li>', '<ul>', '</ul>', '<em>', '</em>', '<strong>', '</strong>', '<br />','(', ')', ',', '.', ';', ':']
    
    for symbol in symbol_lst:
        input_str = input_str.lower().replace(symbol, ' ')
    return input_str

def vacancys_details(url_list):

    """
    Функция возвращает список всех слов в description и значений в key_skills
    Аргументы:
        url_list - список ссылок на вакансии
    """
    descriptions_list = []
    for url in url_list:
        req = requests.get(url)
        # write_to_file(req.content.decode(), 'vacancy_detail.json')
        data = json.loads(req.content.decode())
        req.close()
        descriptions_list.extend(remote_symbol(data['description']).split())
        # Пример поля key_skills
        # 'key_skills': [{'name': 'Python'}, {'name': 'Linux'}, {'name': 'SQL'}, {'name': 'Git'}, {'name': 'Django Framework'}]
        for skill in data['key_skills']:
            descriptions_list.append(skill['name'])

    return descriptions_list

def write_to_file(input_str, file_name = 'vacancy.json'):
    """
    Функция записи в файл.
    Аргументы:
        input_str - строка которую пишем в файл
        file_name - имя файла

    """
    with open(file_name, 'w', encoding='utf8') as w:
        w.write(input_str)

def select_latin_words(input_lst):
    latin_words_dict = {}
    for elem in input_lst:
        for symb in elem:
            if symb in ascii_letters:
                flag = True
            else:
                flag = False
                break
        if flag:
            if elem not in latin_words_dict.keys():
                latin_words_dict[elem] = 1
            else:
                latin_words_dict[elem] += 1
    return latin_words_dict

# получаем список ссылок на вакансии
for page in range(20):
    js_str = getPage(page) #получаем ответ в виде json - файла
    # write_to_file(js_str) # Запись строки ответа в файл для разбора структуры json
    js = json.loads(js_str) # Преобразуем текст ответа запроса в словарь Python
    
    url_list = [js['items'][i]['url'] for i in range(len(js['items']))] # добавляем url в список ссылок
    
    if (js['pages'] - page) <= 1: # Проверка на последнюю страницу если вакансий меньше чем в диапазоне цикла
        break

    time.sleep(0.25) # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать

latin_words = select_latin_words(vacancys_details(url_list))
print(*sorted(latin_words.items(), key=lambda x:x[1], reverse=True), sep='\n')


