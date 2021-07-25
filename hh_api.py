
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
        'text': 'python junior', # Текст фильтра
        'page': page, # Индекс страницы поиска на HH
        'per_page': 100, # Кол-во вакансий на 1 странице
        'area': 113 # регион поиска. 113 - Россия
    }
     
    req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
    data = req.content.decode() # Декодируем его ответ, чтобы Кириллица отображалась корректно
    req.close()
    return data

def remote_symbol(input_str):
    """
    Функция удаления тэгов и знаков препинания.
    Аргументы:
        input_str - строка
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
    print('Вакансий найдено: ', len(url_list))
    descriptions_list = []
    for url in url_list:
        req = requests.get(url)
        # write_to_file(req.content.decode(), 'vacancy_detail.json')
        data = json.loads(req.content.decode())
        req.close()
        descriptions_list.extend(remote_symbol(data['description']).lower().split())
        # Пример поля key_skills
        # 'key_skills': [{'name': 'Python'}, {'name': 'Linux'}, {'name': 'SQL'}, {'name': 'Git'}, {'name': 'Django Framework'}]
        for skill in data['key_skills']:
            descriptions_list.append(skill['name'].lower())
        time.sleep(0.1)
    return descriptions_list

def write_to_file(input_str, file_name = 'vacancy.json', mode = 'w'):
    """
    Функция записи в файл.
    Аргументы:
        input_str - строка которую пишем в файл
        file_name - имя файла
        mode - режим открытия файла
    """
    with open(file_name, mode, encoding='utf8') as file:
        file.write(input_str)

def select_latin_words(input_lst):
    """
    Функция возвращает словарь и счетчик слов полностью из латинских символов
    Аргументы:
        input_lst - список слов
    """
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
result = {} # так как парсим много страниц то все результаты пишем в словарь result
for page in range(20):
    js_str = getPage(page) #получаем ответ в виде json - файла
    # write_to_file(js_str) # Запись строки ответа в файл для разбора структуры json
    js = json.loads(js_str) # Преобразуем текст ответа запроса в словарь Python
    # добавляем url в список ссылок
    url_list = [js['items'][i]['url'] for i in range(len(js['items']))] 
    # формируем словарь латинских слов
    latin_words = select_latin_words(vacancys_details(url_list))
    # поэлементно проверяем словарь и пишем элементы в результирующий словарь
    for word in latin_words:
        if word not in result.keys():
            result[word] = latin_words[word]
        else:
            result[word] += latin_words[word]
    # Проверка на последнюю страницу если вакансий меньше чем в диапазоне цикла
    if (js['pages'] - page) <= 1:
        break
     # Необязательная задержка, но чтобы не нагружать сервисы hh, оставим. 5 сек мы может подождать
    time.sleep(0.25)

result = sorted(result.items(), key=lambda x:x[1], reverse=True)
write_to_file('','result.txt', 'w') # создаем\очищаем файл
for elem in result:
    write_to_file(f'{elem[0]}: {elem[1]}\n','result.txt', 'a')




