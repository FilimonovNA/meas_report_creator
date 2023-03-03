#import Analyze
#from Analyze import Query


'''CONSTANTS'''
UNDEFINED_FLOOR_NUMBER = -999
OUTDOOR_FLOOR_NUMBER = 777
NO_SYMBOL_ID = -1


list = [ 'Sevastopolskiy_prospect_66_fl-1_23Feb09_104430:1',
         'Sevastopolskiy_prospect_66_fl-1_23Feb09_104430:11',
         'Sevastopolskiy_prospect_66_fl-1_23Feb09_104430:2',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104430:3',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104430:4',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104430:5',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104430:6',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:1',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:11',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:2',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:3',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:4',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:5',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_104920:6',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:1',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:11',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:2',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:3',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:4',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:5',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105220:6',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:1',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:11',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:2',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:3',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:4',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:5',
         'Sevastopolskiy_prospect_66_fl-2_23Feb09_105954:6',
         'Sevastopolskiy_prospect_66__fl__23Feb09_105220:11',
         'Sevastopolskiy_prospect_66__fl__23Feb09_105220:2',
         'Sevastopolskiy_prospect_66__fl__23Feb09_105220:3',
         'Sevastopolskiy_prospect_66__fl__23Feb09_105420:4',
         'Sevastopolskiy_prospect_66__fl__23Feb09_106220:5',
         'Sevastopolskiy_prospect_66__fl__23Feb09_101220:6',
         'Sevastopolskiy_prospect_66__fl__23Feb09_121220:1',
         'Sevastopolskiy_prospect_66__fl__23Feb09_186954:11',
         'Sevastopolskiy_prospect_66__fl__23Feb09_187954:2',
         'Sevastopolskiy_prospect_66__fl__23Feb09_114954:3',
         'Sevastopolskiy_prospect_66__fl__23Feb09_101454:4',
         'Sevastopolskiy_prospect_66__fl__23Feb09_435954:5',
         'Sevastopolskiy_prospect_66__fl__23Feb09_105954:6'
         ]

# Rxlevel|RSCP|RSRP|AVG DL/UL 3G| AVG DL/UL 4g| AVG 4G < 2.5 | AVG MOS
''' Словарь соответствия номера трубки и KPI '''
KPI = {
    '1': ['rxle'],
    '2': ['rscp', 'dl', 'ul'],
    '3': ['rsrp', 'dl', 'trhld2.5', 'trhld1.0'],
    '4': ['mos_mo'],
    '5': ['mos_mo'],
    '6': ['ul']
}

''' Дата для одного этажа '''
floor_data = {
    'rxlevel': '',
    'rscp': '',
    'rsrp': '',
    'AVG DL/UL3G': 'dl/ul Mb/s',
    'AVG DL/UL 4G': 'dl/ul Mb/s',
    'DL 4G < 2.5': '%',
    'AVG MOS': ''
}

''' Конечный результат '''


# result = {
#			floor_num : floor_data,
#			floor_num : floor_data
# }


# def print_all_object_attributes(data):
#     for att in dir(data):
    #    Analyze.Log.Write(att)
    #    Analyze.Log.Write(getattr(data, att))


def get_measurements_list():
    measurements_list = list                    #Analyze.Workspace.GetSelectedMeasurements()
    meas_for_query_list = []
    for i in range(len(measurements_list)):
        measurement = measurements_list[i]
        measurement = rename_for_query(measurement)
        meas_for_query_list.append(measurement)
    return sorted(meas_for_query_list)


def rename_for_query(meas):
    name = meas                 #.FullName
    for letter in name:
        if letter == '.':
            name = name.replace(letter, ":")
    # return meas.HintTitle
    return name


def get_dl_ul_data(meas):
    query_name = 'SELECT AVG("app_throughput_downlink"), AVG("app_throughput_uplink") FROM "Nemo"."DAS+" x /* "MEAS(' + meas + ')" */'

    query_file = Query(query_name)
    data_table = []
    for data_str in query_file.Run():
        data_list = []
        for data in data_str:
            Analyze.Log.Write(str(data))
            data_list.append(data)
        data_table.append(data_list)
    return data_table


def get_slave_number(meas):
    '''return number of slave (1, 2, 3, 4, 5, 6, 11)'''
    if meas[-2] == ':':
        phone_number = meas[-1:]
    else:
        phone_number = meas[-2:]
    return int(phone_number)


'''FLOOR SEARCH'''


def try_search_floor_before(string_name, start_fl_num):
    # Before fl
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


#def print_meas_list(meas_list):
#    for elem in meas_list:
#        Analyze.Log.Write(elem)


''' Получаем словарь {номер этажа: слейвы} '''


def get_dict_floor_slaves(meas_list):
    floor_slaves = {}

    for meas in meas_list:
        meas_floor = int(get_floor(meas))
        slave_number = get_slave_number(meas)

        i = -0.1
        is_in_dict = 0
        while (is_in_dict != 1):

            if meas_floor not in floor_slaves.keys():
                '''first input for all'''
                floor_slaves.update({meas_floor: [meas]})
                is_in_dict = 1

            #            elif meas_floor in floor_slaves.keys() and meas_floor != -999:
            #                '''UNDEFINED'''
            #                floor_slaves.get(meas_floor).append(meas)
            #                is_in_dict = 1

            elif meas_floor in floor_slaves.keys():  # if slave already in floor number , floor number will be .1->.2->.3
                '''2+ input for all'''
                current_log_name = get_log_name(meas)
                dict_log_name = get_log_name(floor_slaves.get(meas_floor)[0])

                if current_log_name == dict_log_name:
                    floor_slaves.get(meas_floor).append(meas)
                    is_in_dict = 1

                else:
                    meas_floor = round(meas_floor + i, 1)

    #print("DICT")
    #print(floor_slaves)
    for k, v in floor_slaves.items():
        print(f"{k}:{v}\n")
    return floor_slaves



''' Получаем название измерения без слейва'''
def get_log_name(meas):
    return meas[:-3] if meas[-2].isdigit() else meas[:-2]



def main():
#    for i in range(40):
#        Analyze.Log.Write(' ')

#    Analyze.Log.Write('File generator started work')

    warning = 'WARNING'
    error = 'ERROR'
    path = 'C:/RC_data/data.txt'

    meas_list = get_measurements_list()
    #print_meas_list(meas_list)
    get_dict_floor_slaves(meas_list)
   # print(meas_list)
#    if len(meas_list) == 0:

       # Analyze.Log.Write(error)
        #Analyze.Log.Write('SELECT MEASUREMENTS IN WORKSPACE')
#    else:
#    floor_slave_dict = {}

 #       Analyze.Log.Write('File creator finished')


main()