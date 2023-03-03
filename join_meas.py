from tkinter import filedialog
from os import listdir
import os
from get_joined_meas_names import main as get_joined_meas_names
import time


# Производительность 3500 строк в сек


def main():
    start_time = time.time()
    user_directory = open_file_dialog()
    if user_directory == '':

        return "Выберите директорию"
    files_list = get_file_names_list(user_directory)

    if files_list is not None:
        joins_dict = get_joined_meas_names(files_list)
        print(joins_dict)

        for k, v in joins_dict.items():

            if k[-3:] == 'nmf':
                if len(v) == 1:
                    pass
                elif k.find('fl') != -1:
                    join_nmf_indoor(user_directory, v)
                else:
                    join_nmf_outdoor(user_directory, v)
            elif k[-3:] == 'gpx':
                if len(v) == 1:
                    pass
                else:
                    join_gpx(user_directory, v)
            elif k[-3:] == 'mrk':
                if len(v) == 1:
                    pass
                else:
                    join_mrk(user_directory, v)

            #  elif k[-3:] == 'csv':
            #     if len(v) == 1:
            #         pass
            #     else:
            #         join_csv(user_directory, v)
    else:

        return "Нечего объединять"
    end_time = time.time()
    print(f'Мы потратили {round(end_time-start_time, 2)} для join\'a')

    return "Объединение выполнено"


def get_file_names_list(directory):
    files_list = listdir(directory)
    output_list = []
    for file in files_list:
        if (file.endswith('.nmf') or file.endswith('.gpx') or file.endswith('.mrk')) and \
                file.startswith('joined') is False:
            output_list.append(file)
    output_list.sort()
    return output_list


def open_file_dialog():

    # user_path = filedialog.askdirectory(title="Select a File")
    user_path = filedialog.askopenfilename()
    user_path = os.path.dirname(user_path)

    return user_path


def join_nmf_outdoor(directory, nmf_list):
    start_time = time.time()
    first_meas = nmf_list[0]

    with open(f'{directory}/{first_meas}', 'r') as f:

        lines = f.readlines()

    with open(f'{directory}/joined_{first_meas}', 'w') as f:
        if first_meas[-6:] == '17.nmf':
            f.writelines(lines[:-3])
        else:
            f.writelines(lines[:-5])
    end_time = time.time()

    print(f'rewrite {len(lines)} lines in {round(end_time-start_time, 2)}s')

    output_file = open(f'{directory}/joined_{first_meas}', 'a')
    input_lines = []
    for i in range(1, len(nmf_list)):
        start_time = time.time()
        input_file = open(f'{directory}/{nmf_list[i]}', 'r')
        if first_meas[-6:] == '17.nmf':
            input_lines = input_file.readlines()[23:]
        else:
            input_lines = input_file.readlines()[32:]
        if i % 10000 == 0:
            time.sleep(0.5)
        output_file.writelines(input_lines)
        input_file.close()

    end_time = time.time()
    print(f'append in {round(end_time-start_time)}s {len(input_lines)} input lines')
    output_file.close()


def join_nmf_indoor(directory, nmf_list):
    mark_counter: int = -1   # Подсчет идет с нуля

    nmf_list.sort()
    first_meas = nmf_list[0]

    # Узнаем сколько маркеров было в первом файле
    first_meas_file = open(f'{directory}/{first_meas}', 'r')
    joined_meas_file = open(f'{directory}/joined_{first_meas}', 'a')

    while True:
        text_line = first_meas_file.readline()

        if text_line.find("#STOP") == -1 and text_line.find("#HASH") == -1:
            joined_meas_file.write(text_line)

        mark_flag = text_line.find("MARK,")
        if mark_flag != -1:
            mark_counter += 1

        if not text_line:
            break
    first_meas_file.close()

    for i in range(1, len(nmf_list)):
        print("i = ", i)
        meas_name = nmf_list[i]
        file = open(f'{directory}/{meas_name}', 'r')
        start_flag = 0
        # STOP_FLAG = 0
        while True:
            mark_flag = 0
            new_line = file.readline()

            if new_line.find("#START") != -1:
                start_flag = 1
                new_line = file.readline()

            if new_line.find("#STOP") != -1 and i != len(nmf_list)-1:
                file.close()
                break

            if new_line.find("MARK,") != -1:
                mark_flag = 1
                mark_counter += 1

            if start_flag == 1:      # and STOP_FLAG == 0:
                if mark_flag == 0:
                    joined_meas_file.write(new_line)
                elif mark_flag == 1:
                    new_line = new_line[:-4] + str(mark_counter) + new_line[-3:]
                    joined_meas_file.write(new_line)
            if not new_line:
                file.close()
                break
    joined_meas_file.close()


def join_gpx(directory, gpx_list):

    start_time = time.time()
    first_meas = gpx_list[0]
    print(first_meas)

    with open(f'{directory}/{first_meas}', 'r') as f:
        lines = f.readlines()

    with open(f'{directory}/joined_{first_meas}', 'w') as f:
        f.writelines(lines[:-4])

    end_time = time.time()
    print(f'{len(lines)} in {round(end_time-start_time)}')

    output_file = open(f'{directory}/joined_{first_meas}', 'a')
    input_lines = []
    for i in range(1, len(gpx_list)):
        start_time = time.time()
        input_file = open(f'{directory}/{gpx_list[i]}', 'r')
        input_lines = input_file.readlines()[5:]
        output_file.writelines(input_lines)
        input_file.close()

    end_time = time.time()
    print(f'in {round(end_time-start_time)} sec input {len(input_lines)}')
    output_file.close()


'''
#def join_csv(directory, csv_list):
    # first_meas = csv_list[0]
    #
    # with open(f'{directory}/{first_meas}', 'r') as f:
    #     lines = f.readlines()
    #
    # with open(f'{directory}/joined_{first_meas}', 'w') as f:
    #     f.writelines(lines)
    # first_data = get_data_csv(lines)
    # for meas in range(1, len(csv_list)):
    #
    # print(first_data)
#    pass
'''


def join_mrk(directory, mrk_list):
    first_meas = mrk_list[0]
    # print(first_meas)
    with open(f'{directory}/{first_meas}', 'r') as f:
        lines = f.readlines()
    index_marker = 0
    counter_marker = 0
    index_index = 0
    for line in lines:
        if line.find('[marker') != -1 and line.find('[markercount]') == -1:
            index_marker = int(line[line.find('[marker')+len('[marker'):-2])
            counter_marker += 1
        if line.find('index=') != -1 and int(line[line.find('index=')+len('index='):-1]) > index_index:
            index_index = int(line[line.find('index=')+len('index='):-1])

    print(index_marker)
    print(index_index)

    with open(f'{directory}/joined_{first_meas}', 'w') as f:
        f.writelines(lines)

    output_file = open(f'{directory}/joined_{first_meas}', 'a')
    for i in range(1, len(mrk_list)):
        input_file = open(f'{directory}/{mrk_list[i]}', 'r')
        input_lines = input_file.readlines()[6:]
        for line in input_lines:
            if line.find('[marker') != -1:
                index_marker += 1
                new_line = f'[marker{index_marker}]\n'
                counter_marker += 1
            elif line.find('index=') != -1:
                index_index += 1
                new_line = f'index={index_index}\n'
            else:
                new_line = line
            output_file.writelines(new_line)
    output_file.close()

    output_file = open(f'{directory}/joined_{first_meas}', 'r')
    lines = output_file.readlines()
    output_file.close()
    output_file = open(f'{directory}/joined_{first_meas}', 'w')
    for line in lines:
        if line.find('markers=') != -1:
            new_line = f'markers={counter_marker}\n'
        else:
            new_line = line
        output_file.writelines(new_line)
    output_file.close()


'''
# def get_data_csv(lines):
    # data = {}
    # for line in lines:
    #     semicolon_number = line.find(';')
    #     if semicolon_number != -1:
    #         data[line[:semicolon_number]] = line[semicolon_number + 1:-1]
    #     else:
    #         data[line[:semicolon_number]] = None
    # return data
#   pass
'''
