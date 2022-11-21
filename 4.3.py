import csv
import re
import datetime
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


def scv_parcer(inp_csv, filter_vac, sort_param, is_reverse):
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
                if one_list[i][j][0] != "key_skills":
                    one_list[i][j][1] = re.sub(r'(\n)', ', ', one_list[i][j][1])
                else:
                    one_list[i][j][1] = re.sub(r'(\n)', ',, ', one_list[i][j][1])
                one_list[i][j][1] = re.sub(r"<[^>]+>", "", one_list[i][j][1], flags=re.S)
                one_list[i][j][1] = re.sub(r'(\s)', ' ', one_list[i][j][1])
                one_list[i][j][1] = remove_spaces(one_list[i][j][1])

        return one_list

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
        data[1] = '\n'.join(x)

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
                data_vacancies[i][j][1] = (data_vacancies[i][j][1][:100] + '...') if len(
                    data_vacancies[i][j][1]) > 100 else \
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

    # сортировка
    def sorting(sort_param, is_reverse, table_valeus, old_sort):
        def sort_by_model(model, sort_list, num_list):
            so_di = []
            di = []
            y = []
            for i in range(len(sort_list[num_list])):
                oy = []
                ox = []
                xs = i
                l = model[i]
                x = sort_list[num_list][i]
                oy.append(l)
                oy.append(xs)
                oy.append(0)
                ox.append(x)
                ox.append(xs)
                ox.append(0)
                so_di.append(oy)
                di.append(ox)
            for i in range(len(di)):
                for j in range(len(di)):
                    if di[i][0] == so_di[j][0] and so_di[j][2] == 0:
                        so_di[j][2] += 1
                        y.append(j)
            old_sort_list = []
            for i in range(len(sort_list)):
                ox = []
                for j in range(len(sort_list[i])):
                    ox.append(sort_list[i][j])
                old_sort_list.append(ox)

            for i in range(len(sort_list[0])):
                for j in range(1, len(sort_list)):
                    if sort_list[j][y[i]] != old_sort_list[j][i]:
                        sort_list[j][y[i]] = old_sort_list[j][i]
            return (sort_list)

        def skills_sort(data_sorting, table_valeus, old_sort):
            skills = []
            for i in range(len(old_sort)):
                skills.append(old_sort[i][1])
            sortt=[]
            skills.sort(key=lambda x: len(x))
            for i in range(len(skills)):
                sortt.append(skills[i].split(',, '))
            sortt.sort(key=lambda x: len(x))
            for i in range(len(skills)):
                skills[i] = '\n'.join(sortt[i])
                print(skills[i],len(skills[i]))
                print()
                # skills[i] = (skills[i][:100] + '...') if len(
                #     skills[i]) > 100 else \
                #     skills[i]
                #
            data_sorting=sort_by_model(skills, table_valeus, 3)
            return data_sorting

        def money_sort(data_sorting, table_valeus, old_sort):
            currency_to_rub = {
                "AZN": 35.68,
                "EUR": 59.90,
                "GEL": 21.74,
                "KGS": 0.76,
                "KZT": 0.13,
                "RUR": 1,
                "UAH": 1.64,
                "USD": 60.66,
                "UZS": 0.0055}

        def data_sort(data_sorting, table_valeus, old_sort):
            old_sort_data=[]
            for i in range(len(old_sort)):
                ox=[]
                ox.append(old_sort[i][0])
                old_sort_data.append(ox)
            dates = [datetime.datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S%z") for ts in old_sort_data]
            dates.sort()
            sorteddates = [datetime.datetime.strftime(ts, "%Y-%m-%dT%H:%M:%S%z") for ts in dates]
            time = [datetime.datetime.strptime(ts[0:10], "%Y-%m-%d") for ts in sorteddates]
            time = [datetime.date.strftime(ts, "%d.%m.%Y") for ts in time]
            data_sorting = sort_by_model(time, table_valeus, 9)
            return data_sorting

        def other_sort(data_sorting, table_valeus, sort_param):
            other_dic={"Название":1,'Описание':2,'Опыт работы':4,'Премиум-вакансия':5,'Компания':6,'Название региона':8}
            num=other_dic.get(sort_param)
            sort_data = []
            for i in range(len(table_valeus[num])):
                sort_data.append(table_valeus[num][i])
            sort_data.sort()
            data_sorting=sort_by_model(sort_data, table_valeus, num)
            return data_sorting

        data_sorting = []
        sort_dic = {'Навыки': skills_sort, "Оклад": money_sort, "Дата публикации вакансии": data_sort,
                    "other": other_sort}
        if len(sort_param) == 0:
            data_sorting = table_valeus
        else:
            if sort_param not in dic_naming.values() and sort_param != 'Дата публикации вакансии' and  sort_param != 'Оклад':
                data_sorting = "Параметр сортировки некорректен"
            elif len(is_reverse)!=0 and(is_reverse != "Да" and is_reverse != "Нет"):
                data_sorting = "Порядок сортировки задан некорректно"
            else:
                if sort_param in sort_dic:
                    data_sorting = sort_dic[sort_param](data_sorting, table_valeus, old_sort)
                else:
                    sort_kod = 'other'
                    data_sorting = sort_dic[sort_kod](data_sorting, table_valeus, sort_param)
                if is_reverse == "Да":
                    for i in range(1,len(data_sorting)):
                        data_sorting[i].reverse()
        return data_sorting

    def transpose(matr):
        res = []
        n = len(matr)
        m = len(matr[0])
        for j in range(m):
            tmp = []
            for i in range(n):
                tmp = tmp + [matr[i][j]]
            res = res + [tmp]
        return res

    def table_data(data_vacancies, dic_naming):
        table_string = []
        table_header = []
        # меняем на русский
        for i in range(len(data_vacancies)):
            ou = []
            ox = []
            ou.append(data_vacancies[i][7][1].split(".")[0])
            ou.append(data_vacancies[i][8][1].split(".")[0])
            ou.append(data_vacancies[i][3][1].split(',, '))
            ox.append(data_vacancies[i][12][1])
            ox.append(data_vacancies[i][3][1])
            old_data.append(ou)
            old_sort.append(ox)
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

    reader, list_naming = сsv_reader(inp_csv)
    if len(reader) == 0:
        table_dict = 'Пустой файл'
    elif len(list_naming) == 0:
        table_dict = "Нет данных"
    else:
        reader.insert(0, "№")
        data_vacancies = csv_filer(reader, list_naming)
        table_head, data_vacancies = table_data(data_vacancies, dic_naming)
        if isinstance(data_vacancies, str):
            table_dict = data_vacancies

        else:
            table_valeus = transpose(data_vacancies)
            table_valeus = sorting(sort_param, is_reverse, table_valeus, old_sort)
            if isinstance(table_valeus, str):
                table_dict=table_valeus
            else:
                table_dict = dict.fromkeys(table_head)
                for i in range(len(table_dict)):
                    table_dict[table_head[i]] = table_valeus[i]
    return table_dict


def start_end(vac_nums, table_dic):
    l = len(vac_nums)
    if l == 0:
        start = 0
        end = len(table_dic['№'])
    elif l == 1:
        start = int(vac_nums[0]) - 1
        end = len(table_dic['№'])
    else:
        start = int(vac_nums[0]) - 1
        end = int(vac_nums[1]) - 1
    return start, end


def table_fields(columns_table, table_head):
    fields = []
    if len(columns_table) == 0:
        for key in table_head:
            fields.append(key)
    else:
        fields = columns_table
        fields.insert(0, "№")
    return fields


def print_table(my_table, vac_nums, colums_table, inp_csv, filter_vac, sort_param, is_reverse):
    table_dict = scv_parcer(inp_csv, filter_vac, sort_param, is_reverse)
    if isinstance(table_dict, str):
        print(table_dict)
    else:
        start, end = start_end(vac_nums, table_dict)
        for key, value in table_dict.items():
            my_table.add_column(key, value)
        fields = table_fields(colums_table, table_dict)
        my_table.hrules = 1
        my_table._max_width = {"№": 20, "Название": 20, "Описание": 20, "Навыки": 20, "Опыт работы": 20,
                               "Премиум-вакансия": 20, "Компания": 20, "Оклад": 20, "Название региона": 20,
                               "Дата публикации вакансии": 20}
        my_table.align = 'l'
        print(my_table.get_string(start=start, end=end, fields=fields))


def input_params():
    inp_csv = input("Введите название файла: ")
    filter_vac = input("Введите параметр фильтрации: ")
    sort_param = input("Введите параметр сортировки: ")
    is_reverse = input("Обратный порядок сортировки (Да / Нет): ")
    vac_nums = input("Введите диапазон вывода: ").split()
    columns_table = input("Введите требуемые столбцы: ")

    if len(columns_table) > 0:
        columns_table = columns_table.split(', ')
    my_table = PrettyTable()
    print_table(my_table, vac_nums, columns_table, inp_csv, filter_vac, sort_param, is_reverse)


old_sort = []
old_data = []  # переменная для фильтрации
input_params()
