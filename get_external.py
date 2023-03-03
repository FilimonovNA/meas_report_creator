import os
from tkinter import filedialog


# Открытие диалогового окна и выбор юзером папки
def select_path():
    user_path = ''
    while user_path == '':
        user_path = filedialog.askdirectory(title="Select a File")
        # Возвращает строку содержащую путь к выбранной папке
    return user_path


# Принимает название документа и путь сохраняет документ если это возможно, иначе возвращает 1
def save_report(_doc, _path, file_name):
    try:
        _doc.save(f'{_path}/{file_name}.docx')
    except PermissionError:
        return 1


# Удаление документа
def remove_report(_doc, _path, file_name):
    try:
        if hasattr(_doc, "delete"):
            _doc.delete(f'{_path}/{file_name}.docx')
        else:
            return 1
    except PermissionError or AttributeError:
        return 1


# На основании полученного на вход пути возвращает список строк содержащих названия картинок в папке
def get_pictures_list(_path):
    all_files = os.listdir(_path)
    list_of_pictures = []
    for file in all_files:
        if file.endswith('.jpg') or file.endswith('.png'):
            list_of_pictures.append(file)
    return list_of_pictures


# Получаем данные по сервисам и покрытию
def get_services_report(_path):
    # dict result = {floor:{KPI:value, }, }
    result = {}
    filename = _path+'/services_report.txt'
    if os.path.isfile(filename):
        with open(filename) as data_file:   # закрывает автоматически
            all_strings = data_file.read().splitlines()
    else:
        return -1

    # парсинг файла в словарь
    for string in all_strings:
        floor = string[:string.find(':')]
        one_floor_str = string[string.find(':')+1:]
        one_floor_data_list = one_floor_str.split(';')
        one_floor_result = {}
        for i in range(len(one_floor_data_list)-1):
            kpi_elem = one_floor_data_list[i].split('::')
            kpi, value = kpi_elem[0], kpi_elem[1]
            one_floor_result.update({kpi:value})

        result.update({floor:one_floor_result})
    #print(data)
    return result


# Получаем данные по голосу
def get_voice_call_report(_path):
    filename = _path+'/voice_quality_report.txt'
    result = {}
    if os.path.isfile(filename):
        with open(filename) as data_file:   # закрывает автоматически
            all_strings = data_file.read().splitlines()
    else:
        return -1

    # парсинг файла в словарь
    for string in all_strings:
        kpi = string[:string.find(':')]
        one_kpi_str = string[string.find(':')+1:]
        one_kpi_str = one_kpi_str.split(';')

        one_kpi_result = {}
        for i in range(len(one_kpi_str)-1):
            one_tech = one_kpi_str[i].split('::')
            tech, value = one_tech[0], one_tech[1]
            one_kpi_result.update({tech:value})

        result.update({kpi:one_kpi_result})

    return result


# Получаем данные по пересечениям PCI
def get_crossmod(_path):
    filename = _path+'/crossmod.txt'
    if os.path.isfile(filename):
        with open(filename) as data_file:   # закрывает автоматически
            data = data_file.read().splitlines()
        #for line in data:
        #    if line not in [None, "", "\n"]:
        #        print(line)
        if len(data) > 10:
            return filename
        else:
            return data
    else:
        return -1


