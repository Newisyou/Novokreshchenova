import csv
import re
import datetime
import sympy
from prettytable import PrettyTable

dic_naming = {"name": "Название",
              "description": "Описание",
              "key_skills": "Навыки",
              "experience_id": "Опыт работы",
              "premium": "Премиум-вакансия",
              "employer_name": "Компания",
              "salary_from": "Нижняя граница вилки оклада",
              "salary_to": "Верхняя граница вилки оклада",
              "salary_gross": "Оклад указан до вычета налогов",
              "salary_currency": "Идентификатор валюты оклада",
              "area_name": "Название региона",
              "published_at": "Дата и время публикации вакансии"}


def yes_or_no(a):
    a = a.upper()
    if a == "TRUE":
        a = "Да"
    elif a == "FALSE":
        a = "Нет"
    return a


def remove_spaces(str_change):
    while "  " in str_change:
        str_change = str_change.replace("  ", " ")
        str_change = str_change.strip()
    return str_change


# пробелы для деняк
def money(mon):
    mon = mon.split(".")[0]
    if len(mon) // 3 == "0":
        n = (len(mon) // 3) - 1
    else:
        n = len(mon) // 3

    oy = []
    while n != 0:
        y = mon[len(mon) - 3:len(mon)]
        mon = mon[0:len(mon) - len(y)]
        n -= 1
        oy.append(y)
    oy.append(mon)
    mon = ""
    oy = list(reversed(oy))
    for i in range(len(oy)):
        mon += oy[i] + " "
    mon.strip()
    return mon


def cur_rus(data):
    dic_currency = {"AZN": "Манаты",
                    "BYR": "Белорусские рубли",
                    "EUR": "Евро",
                    "GEL": "Грузинский лари",
                    "KGS": "Киргизский сом",
                    "KZT": "Тенге",
                    "RUR": "Рубли",
                    "UAH": "Гривны",
                    "USD": "Доллары",
                    "UZS": "Узбекский сум"}
    data[1] = dic_currency.get(data[1])
    return data


def exp_rus(data):
    dic_exp = {"noExperience": "Нет опыта",
               "between1And3": "От 1 года до 3 лет",
               "between3And6": "От 3 до 6 лет",
               "moreThan6": "Более 6 лет"}
    data[1] = dic_exp.get(data[1])
    return data


def date_form(data):
    # меняем время Datetime
    time = datetime.datetime.strptime(data[1][0:10], "%Y-%m-%d")
    time = time.date().strftime("%d.%m.%Y")
    data[1] = time
    data[0] = "Дата публикации вакансии"
    return data


def skills_form(data):
    x = data[1].split(',, ')
    data[1]='\n'.join(x)

    return data


def formatter(data_vacancies):
    formatter_dic = {"Идентификатор валюты оклада": cur_rus,
                     "Опыт работы": exp_rus,
                     "Дата и время публикации вакансии": date_form,
                     "Навыки": skills_form}

    # меняем на русский
    for i in range(len(data_vacancies)):
        for j in range(len(data_vacancies[i])):
            if data_vacancies[i][j][0] in formatter_dic:
                data_vacancies[i][j] = formatter_dic[data_vacancies[i][j][0]](data_vacancies[i][j])
            data_vacancies[i][j][1] = (data_vacancies[i][j][1][:100] + '...') if len(data_vacancies[i][j][1]) > 100 else \
                data_vacancies[i][j][1]
            if data_vacancies[i][j][0] == 'Премиум-вакансия' or data_vacancies[i][j][
                0] == "Оклад указан до вычета налогов":
                data_vacancies[i][j][1] = yes_or_no(data_vacancies[i][j][1])

        # Все про оклад
        data_vacancies[i][7][1] = money(data_vacancies[i][7][1]).strip()
        data_vacancies[i][8][1] = money(data_vacancies[i][8][1]).strip()
        salary = data_vacancies[i][7][1] + " - " + data_vacancies[i][8][1] + " (" + data_vacancies[i][10][1] + ") "
        taxes = "(С вычетом налогов)" if data_vacancies[i][9][1] == "Нет" else '(Без вычета налогов)'
        salary += taxes
        data_vacancies[i][7][0] = "Оклад"
        data_vacancies[i][7][1] = salary

    for i in range(len(data_vacancies)):
        del data_vacancies[i][8:11]
    return data_vacancies


def сsv_reader(ﬁle_name):
    csv_content = []
    res = []
    header_line = []
    with open(ﬁle_name, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            csv_content.append(row)
    if len(csv_content) == 0:
        pass
    else:
        header_line = csv_content.pop(0)

        # отбираем нужные строки
        for l in csv_content:
            k = 1
            for i in range(len(l)):
                if len(l[i]) == 0:
                    k = 0
            if len(l) == len(header_line) and k == 1:
                res.append(l)
    return header_line, res


def csv_filer(header_line, res):
    one_list = []

    # Преобразуем раздельные списки в один и убираем лишние пробелы
    for i in range(len(res)):
        res[i].insert(0, str(i + 1))
        ou = []  # промежуточная переменная, для корректного вывода
        for j in range(len(res[i])):
            oxy = []  # промежуточная переменная, для корректного вывода
            x = header_line[j].strip()
            y = res[i][j].strip()
            oxy.append(x)
            oxy.append(y)
            ou.append(oxy)
        one_list.append(ou)

    # Избавляемся от переноса и html
    for i in range(len(one_list)):
        for j in range(len(one_list[i])):
            if one_list[i][j][0]!="key_skills":
                one_list[i][j][1] = re.sub(r'(\n)', ', ', one_list[i][j][1])
            else:
                one_list[i][j][1] = re.sub(r'(\n)', ',, ', one_list[i][j][1])
            one_list[i][j][1] = re.sub(r"<[^>]+>", "", one_list[i][j][1], flags=re.S)
            one_list[i][j][1] = re.sub(r'(\s)', ' ', one_list[i][j][1])
            one_list[i][j][1] = remove_spaces(one_list[i][j][1])

    return one_list


def table_data(data_vacancies, dic_naming):
    table_string = []
    table_header = []
    # меняем на русский
    for i in range(len(data_vacancies)):
        ou = []
        ou.append(data_vacancies[i][7][1].split(".")[0])
        ou.append(data_vacancies[i][8][1].split(".")[0])
        ou.append(data_vacancies[i][3][1].split(',, '))
        old_data.append(ou)
        for j in range(1, len(data_vacancies[i])):
            data_vacancies[i][j][0] = dic_naming.get(data_vacancies[i][j][0])

    data_vacancies = formatter(data_vacancies)
    data_vacancies = filter_param(filter_vac, data_vacancies, old_data)
    if isinstance(data_vacancies, str):
        table_string = data_vacancies
    else:
        for i in range(len(data_vacancies)):
            ou = []
            for j in range(len(data_vacancies[i])):
                if len(table_header) < len(data_vacancies[0]):
                    table_header.append(data_vacancies[0][j][0])
                ou.append(data_vacancies[i][j][1])
            table_string.append(ou)

    return table_header, table_string


# Проверяем на разные условия, когда фильтрация не пройдет, если пройдет, то выполняет одну из функций
def filter_param(filter_vac, data_vacancies, old_data):
    def salary_met(filter_vac, data_filter, old_data, data_vacancies):
        for i in range(len(old_data)):
            if int(old_data[i][0]) <= int(filter_vac) <= int(old_data[i][1]):
                data_filter.append(data_vacancies[i][1:])
        for i in range(len(data_filter)):
            data_filter[i].insert(0, ["№", i + 1])
        return data_filter

    def key_skills_met(filter_vac, data_filter, old_data, data_vacancies):
        filter_vac = filter_vac.split(', ')
        for i in range(len(old_data)):
            c = list(set(filter_vac) & set(old_data[i][2]))
            if len(c) == len(filter_vac):
                data_filter.append(data_vacancies[i][1:])

        for i in range(len(data_filter)):
            data_filter[i].insert(0, ["№", i + 1])
        return data_filter

    def others_met(filter_vac, data_filter, old_data, data_vacancies):
        for i in range(len(data_vacancies)):
            for j in range(len(data_vacancies[i])):
                if filter_vac == data_vacancies[i][j][1]:
                    data_filter.append(data_vacancies[i][1:])
        for i in range(len(data_filter)):
            data_filter[i].insert(0, ["№", i + 1])
        return data_filter

    def currency(filter_vac, data_filter, old_data, data_vacancies):
        for i in range(len(data_vacancies)):
            for j in range(len(data_vacancies[i])):
                if filter_vac in data_vacancies[i][j][1]:
                    data_filter.append(data_vacancies[i][1:])
        for i in range(len(data_filter)):
            data_filter[i].insert(0, ["№", i + 1])
        return data_filter

    def premium(filter_vac, data_filter, old_data, data_vacancies):
        for i in range(len(data_vacancies)):
            if filter_vac == data_vacancies[i][5][1]:
                data_filter.append(data_vacancies[i][1:])
        for i in range(len(data_filter)):
            data_filter[i].insert(0, ["№", i + 1])
        return data_filter

    special_solutions = ['Оклад', 'Навыки', 'Премиум-вакансия']
    data_filter = []
    x = 1
    func = {'Оклад': salary_met, 'Навыки': key_skills_met, 'others': others_met,
            'Идентификатор валюты оклада': currency, 'Премиум-вакансия': premium}
    if len(filter_vac) == 0:
        data_filter = data_vacancies
    else:
        if ":" not in filter_vac:
            x = 0
            data_filter = "Формат ввода некорректен"
        while x == 1:
            param_name = filter_vac[0:filter_vac.find(':')]
            if param_name in special_solutions:
                filter_vac = filter_vac[filter_vac.find(':') + 2:]
                data_filter = func[param_name](filter_vac, data_filter, old_data, data_vacancies)
                if len(data_filter) == 0:
                    data_filter = 'Ничего не найдено'
                x = 0
            elif param_name != dic_naming.get(
                    param_name) and param_name not in dic_naming.values() and param_name != 'Дата публикации вакансии':
                x = 0
                data_filter = "Параметр поиска некорректен"
            else:
                # разобьем на 3 случая
                if param_name not in dic_naming.values():

                    param_name = dic_naming.get(param_name)
                filter_vac = filter_vac[filter_vac.find(':') + 2:]
                if param_name != 'Идентификатор валюты оклада' and param_name not in special_solutions:
                    param_name = 'others'
                data_filter = func[param_name](filter_vac, data_filter, old_data, data_vacancies)

                if len(data_filter) == 0:
                    data_filter = 'Ничего не найдено'
                x = 0
    return data_filter


def start_end(vac_nums, data_vacancies):
    l = len(vac_nums)
    if l == 0:
        start = 0
        end = len(data_vacancies)
    elif l == 1:
        start = int(vac_nums[0]) - 1
        end = len(data_vacancies)
    else:
        start = int(vac_nums[0])-1
        end = int(vac_nums[1]) - 1
    return start, end


def table_fields(columns_table, table_head):
    if len(columns_table) == 0:
        fields = table_head
    else:
        fields = columns_table
        fields.insert(0, "№")
    return fields


def print_table(my_table, vac_nums, columns_table):
    reader, list_naming = сsv_reader(inp_csv)
    if len(reader) == 0:
        print('Пустой файл')
    elif len(list_naming) == 0:
        print("Нет данных")
    else:
        reader.insert(0, "№")
        data_vacancies = csv_filer(reader, list_naming)
        table_head, data_vacancies = table_data(data_vacancies, dic_naming)
        if isinstance(data_vacancies, str):
            print(data_vacancies)
        else:
            my_table.field_names = table_head
            start, end = start_end(vac_nums, data_vacancies)
            fields = table_fields(columns_table, table_head)
            for i in range(len(data_vacancies)):
                my_table.add_row(data_vacancies[i])
            my_table.hrules = 1
            my_table._max_width = {"№": 20, "Название": 20, "Описание": 20, "Навыки": 20, "Опыт работы": 20,
                                   "Премиум-вакансия": 20, "Компания": 20, "Оклад": 20, "Название региона": 20,
                                   "Дата публикации вакансии": 20}
            my_table.align = 'l'
            print(my_table.get_string(start=start, end=end, fields=fields))


old_data = []  # переменная для фильтрации
inp_csv = input()  # файл csv
filter_vac = input()  # параметр фильтрации
vac_nums = input().split()  # порядковые номера вакансий
columns_table = input()  # Названия столбцов, которые нужно выводить в таблице
if len(columns_table) > 0:
    columns_table = columns_table.split(', ')
my_table = PrettyTable()
print_table(my_table, vac_nums, columns_table)
