from bs4 import BeautifulSoup as bs
import requests
import json
from bs4 import Tag

URL = "https://mgkct.minskedu.gov.by/%D0%BE-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%B4%D0%B6%D0%B5/%D0%BF%D0%B5%D0%B4%D0%B0%D0%B3%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BB%D0%BB%D0%B5%D0%BA%D1%82%D0%B8%D0%B2"

response = requests.get(URL)

if response.status_code != 200:
    print(f"Ошибка при запросе к сайту: {response.status_code}")
    exit()

soup = bs(response.text, "html.parser")

teachers = soup.find_all('h3')
posts = soup.find_all('li', class_ = 'tss')

data_json = []
for i in range(0, len(teachers)):
    d = {
        "id":i+1,
        "Преподаватель": teachers[i].text,
        "Должность": posts[i].text
    }
    data_json.append(d)

with open('data.json','w',encoding='UTF-8') as file:
    json.dump(data_json, file, ensure_ascii = False, indent=4)

with open('data.json','r',encoding='UTF-8') as file:
    data = json.load(file)

def print_teachers(data_json):
    for idx, teacher in enumerate(data_json, 1):
        print(f'{idx}. Преподаватель: {teacher["Преподаватель"]}; Должность: {teacher["Должность"]};')

# Пример вызова функции
print_teachers(data_json)

def generate_html(data_file="data.json", template_file="template.html", output_file="index.html"):
    # Загрузка данных из JSON
    with open(data_file, "r", encoding="utf-8") as f:
        teachers_data = json.load(f)

    # Загрузка HTML-шаблона
    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    # Парсинг шаблона
    soup = bs(template, "html.parser")

    # Нахождение элемента для вставки таблицы
    container = soup.find("div", class_="place-here")
    if not container:
        raise ValueError("В шаблоне отсутствует элемент с классом 'place-here' для вставки таблицы.")

    # Создание таблицы
    table = Tag(name="table", attrs={"class": "teachers-table"})

    # Создание заголовков таблицы
    thead = Tag(name="thead")
    tr_head = Tag(name="tr")
    headers = ["№", "Преподаватель", "Должность"]
    for header in headers:
        th = Tag(name="th")
        th.string = header
        tr_head.append(th)
    thead.append(tr_head)
    table.append(thead)

    # Создание строк таблицы
    tbody = Tag(name="tbody")
    for teacher in teachers_data:
        tr = Tag(name="tr")

        # Столбец №
        td_id = Tag(name="td")
        td_id.string = str(teacher["id"])
        tr.append(td_id)

        # Столбец Преподаватель
        td_teacher = Tag(name="td")
        td_teacher.string = teacher["Преподаватель"]
        tr.append(td_teacher)

        # Столбец Должность
        td_post = Tag(name="td")
        td_post.string = teacher["Должность"]
        tr.append(td_post)

        tbody.append(tr)

    table.append(tbody)

    # Вставка таблицы в шаблон
    container.append(table)

    # Сохранение результата в файл
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(soup.prettify())

# Пример вызова функции
generate_html()