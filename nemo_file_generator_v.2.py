import Analyze
from Analyze import Query

'''CONSTANTS'''
UNDEFINED_FLOOR_NUMBER = -999
OUTDOOR_FLOOR_NUMBER = 777
NO_SYMBOL_ID = -1

WARNING = 'WARNING'
ERROR = 'ERROR'
PATH = 'C:/RC_data/data.txt'

''' Словарь соответствия номера трубки и KPI '''
# KPI = {
#	'1':[get_rxle(meas)],
#	'2':[get_rscp(meas), get_dl_3g(meas), get_ul_3g(meas)],
#	'3':[get_rsrp(meas), get_dl_4g(meas), get_trhld2.5(meas)],
#	'4':[get_mos_mo(meas)],
#	'5':[get_mos_mt(meas)],
#	'6':[get_ul_4g(meas)]
#	}

# def print_all_object_attributes(data):
#	for att in dir(data):
#		Analyze.Log.Write(att)
#		Analyze.Log.Write(getattr(data, att))


''' Получаем список выбранных измерений'''


def get_measurements_list():
    measurements_list = Analyze.Workspace.GetSelectedMeasurements()
    meas_for_query_list = []

    for i in range(len(measurements_list)):
        measurement = measurements_list[i]
        measurement = rename_for_query(measurement)
        meas_for_query_list.append(measurement)

    return sorted(meas_for_query_list)


'''Меняем точку на двоеточие для дальнейшего запроса в SQL '''


def rename_for_query(meas):
    name = meas.FullName

    for letter in name:
        if letter == '.':
            name = name.replace(letter, ":")

    return name


'''Получаем номер трубки'''
'''return number of slave (1, 2, 3, 4, 5, 6, 11)'''


def get_slave_number(meas):
    if meas[-2] == ':':
        phone_number = meas[-1:]
    else:
        phone_number = meas[-2:]

    return int(phone_number)


'''УДОЛИ'''
# def get_meas_name(meas):

#	if meas== ':':
#			meas_name_for_workbook = meas[-1:]
#	else:
#		meas_name_for_workbook = meas[-2:]

#	current_floor = get_floor(meas)
#	if current_floor not in [-999, 777]:
#		current_floor = current_floor + 'fl'
#
#	return current_floor + meas_name_for_workbook
'''УДОЛИ'''

'''FLOOR SEARCH'''


def try_search_floor_before(string_name, start_fl_num):
    #    Before fl
    if string_name[start_fl_num - 1].isnumeric() and \
            (string_name[start_fl_num - 2].isnumeric() or
             string_name[start_fl_num - 2] == '-') and \
            string_name[start_fl_num - 3] in ['-', '_']:

        end_fl_num = start_fl_num
        start_fl_num -= 2

        return string_name[start_fl_num:end_fl_num]

    elif string_name[start_fl_num - 1].isnumeric():

        return int(string_name[start_fl_num - 1])
    else:
        return UNDEFINED_FLOOR_NUMBER


def try_search_floor_after(string_name, start_fl_num):
    # After fl
    if (string_name[start_fl_num + 2].isnumeric() or
        string_name[start_fl_num + 2] == '-') \
            and string_name[start_fl_num + 3].isnumeric() \
            and (string_name[start_fl_num + 4] in ['-', '_']):

        start_fl_num += 2
        end_fl_num = start_fl_num + 2

        return string_name[start_fl_num:end_fl_num]

    elif string_name[start_fl_num + 2].isnumeric():

        return int(string_name[start_fl_num + 2])

    # if floor was founded without number
    else:
        return UNDEFINED_FLOOR_NUMBER


# find floor in measure name
def get_floor(string_name):
    '''only 2 symbols for each floor [-9 - 99]'''
    start_fl_num = string_name.rfind('fl')

    # indoor
    if start_fl_num != NO_SYMBOL_ID:
        floor = try_search_floor_before(string_name, start_fl_num)
        if floor == UNDEFINED_FLOOR_NUMBER:
            return try_search_floor_after(string_name, start_fl_num)
        else:
            return floor

    # outdoor
    elif string_name.find('out') != NO_SYMBOL_ID or string_name.find('Out') != NO_SYMBOL_ID or string_name.find(
            'street') != NO_SYMBOL_ID or string_name.find('Street') != NO_SYMBOL_ID:
        return OUTDOOR_FLOOR_NUMBER

    # in other cases
    else:
        return UNDEFINED_FLOOR_NUMBER


''' END OF FLOOR FIND'''

''' Принт всех выбранных измерений '''


def print_meas_list(meas_list):
    for elem in meas_list:
        Analyze.Log.Write(elem)


''' Получаем название измерения без слейва'''


def get_log_name(meas):
    return meas[:-3] if meas[-2].isdigit() else meas[:-2]


''' Получаем словарь {номер этажа: слейвы} '''


def get_dict_floor_slaves(meas_list):
    floor_slaves = {}

    for meas in meas_list:
        meas_floor = get_floor(meas)
        slave_number = get_slave_number(meas)

        i = -0.1
        is_in_dict = 0
        while (is_in_dict != 1):

            if meas_floor not in floor_slaves.keys():
                '''первый вход для всех'''
                floor_slaves.update({meas_floor: [meas]})
                is_in_dict = 1

            elif meas_floor in floor_slaves.keys() and meas_floor != -999:
                '''Второй и более вход  если не UNDEFINED'''
                floor_slaves.get(meas_floor).append(meas)
                is_in_dict = 1

            elif meas_floor <= -999 and meas_floor in floor_slaves.keys():
                '''Второй и более вход если Undefined'''
                '''Требуется сравнения названия измерений, чтобы закинуть в другой лист'''
                current_log_name = get_log_name(meas)
                dict_log_name = get_log_name(floor_slaves.get(meas_floor)[0])

                if current_log_name == dict_log_name:
                    floor_slaves.get(meas_floor).append(meas)
                    is_in_dict = 1

                else:
                    meas_floor += i

    return floor_slaves


''' Заполнение floor_data '''


def get_one_floor_data(meas_list):
    rxle = ''
    rscp = ''
    rsrp = ''
    dl_3g = ''
    ul_3g = ''
    dl_4g = ''
    ul_4g = ''
    trh25 = ''
    mos = 0
    mos_mo = 0
    mos_mt = 0
    for meas in meas_list:
        slave_number = get_slave_number(meas)
        if slave_number == 1:
            rxle = get_rxle(meas)  # ok добавить каналы в запрос

        elif slave_number == 2:
            rscp = get_rscp(meas)  # ok проверить каналы
            dl_3g = get_dl(meas)  # ok методика средней скорости?)
            ul_3h = get_ul(meas)  # ok методика средней скорости?)

        elif slave_number == 3:
            rsrp = get_rsrp(meas)  # ok проверить каналы
            dl_4g = get_dl(meas)  # ok методика средней скорости?)
            trh25 = get_trh25(meas)

        elif slave_number == 4:
            mos_mo = get_mos_mo(meas)  # ok

        elif slave_number == 5:
            mos_mt = get_mos_mo(meas)  # ok

        elif slave_numbet == 6:
            ul_4g = get_ul(meas)  # ok методика средней скорости?)

    mos = (mos_mt + mos_mo) / 2
    ''' Дата для одного этажа '''
    floor_data = {
        'rxlevel': rxle,
        'rscp': rscp,
        'rsrp': rsrp,
        'AVG DL/UL3G': dl_3g + '/' + ul_3g,
        'AVG DL/UL 4G': dl_4g + '/' + ul_4g,
        'DL 4G < 2.5': trh25,
        'AVG MOS': mos
    }

    return floor_data


''' Получение средних значение DL'''


def get_dl(meas):
    query_name = 'SELECT AVG("app_throughput_downlink") FROM "Nemo"."DAS+" x /* "MEAS(' + meas + ')" */'
    query_file = Query(query_name)
    for data_str in query_file.Run():
        return str(round(data_str[0], 2))


''' Получение средних значение UL'''


def get_ul(meas):
    query_name = 'SELECT AVG("app_throughput_uplink") FROM "Nemo"."DAS+" x /* "MEAS(' + meas + ')" */'
    query_file = Query(query_name)
    for data_str in query_file.Run():
        return str(round(data_str[0], 2))


''' Получение средних значение Rx Level'''


def get_rxle(meas):
    query_name = 'SELECT AVG("rx_level_sub") FROM "Nemo.GSM"."RXL+" x WHERE "server"=1  /* "MEAS(' + meas + ')" */'
    query_file = Query(query_name)
    for data_str in query_file.Run():
        return str(round(data_str[0] < 2))


''' Получение средних значение RSCP'''


def get_rscp(meas):
    query_name = 'SELECT  AVG("rscp") FROM "Nemo.UMTS.ECNO"."Cell+" x WHERE "cell_type" = 0 AND "order" = 1 AND "channel_number" IN (2938, 10638, 10662, 10687) /* "MEAS(' + meas + ')" */'
    query_file = Query(query_name)
    for data_str in query_file.Run():
        return str(round(data_str[0] < 2))


''' Получение средних значение RSRP'''


def get_rsrp(meas):
    query_name = 'SELECT  AVG("lte_received_power") FROM "Nemo.LTE.CELLMEAS"."Cell+" x WHERE "lte_cell_type"=0 AND "channel_number" IN (6338, 6350, 1602, 1458, 2850, 3048, 37900, 225) /* "MEAS(' + meas + ')" */'
    query_file = Query(query_name)
    for data_str in query_file.Run():
        return str(round(data_str[0] < 2))


''' Получение процента меньше порога '''


def get_trh25(meas):
    query_name_full = 'SELECT COUNT("app_throughput_downlink") FROM "Nemo"."DAS+" /* "MEAS(' + meas + ')" */'
    query_name_trh = 'SELECT COUNT("app_throughput_downlink" ) FROM "Nemo"."DAS+" x WHERE "app_throughput_downlink" < 2500000  /* "MEAS(' + meas + ')" */'

    query_full = Query(query_name_full)
    query_trh = Query(query_name_trh)

    for data_str in query_full.Run():
        full = data_str[0]
    for data_str in query_trh.Run():
        trh = data_str[0]
    if full not in [None, 0]:
        result = trh * 100.0 / full * 1.0
        result = str(round(result, 2))
    elif full == result and full not in [None, 0]:
        result = 0.00
    else:
        result = None
    return result


''' Заполнение данных для конечного результата'''


def get_result(fs_dict):
    ''' Конечный результат '''
    #	result = {floor_num : floor_data}
    result = {}
    for floor in fs_dict.keys():
        result.update({floor: get_one_floor_data(fs_dict.get(floor))})

    return result


# def print_result

''' Главная часть программы '''


def main():
    for i in range(40):
        Analyze.Log.Write(' ')

    Analyze.Log.Write('File generator started work')

    meas_list = get_measurements_list()
    # print_meas_list(meas_list)

    if len(meas_list) == 0:
        Analyze.Log.Write(error)
        Analyze.Log.Write('SELECT MEASUREMENTS IN WORKSPACE')
    else:
        floor_slave_dict = get_dict_floor_slaves(meas_list)
        result = get_result(floor_slave_dict)

        Analyze.Log.Write('File creator finished')


main()

