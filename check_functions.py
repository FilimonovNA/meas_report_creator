from get_external import *
from get_external import get_pictures_list
from get_report_body import *
from docx import Document

path = r'C:\RG_data'
#get_crossmod(path)

#get_services_report(path)

#get_voice_call_report(path)

pictures_list = get_pictures_list(path)
# print(pictures_list)
#for picture in pictures_list:
#    print(picture + ' : ' + get_script_number_of_picture(picture))
#     print(f'{picture}: {get_picture_number_of_floor(picture)}')
# doc = Document()
#
# meas_data_dict_input = {'Отчет подготовил: ': 'я',
#                         'Измерения провел: ': 'z',
#                         'Дата измерений: ': 'odnfjdf',
#                         'Адрес: ': None,
#                         'Объект:': 'd3wjde',
#                         'report name': '312edh'}
# add_first_page_in_doc(doc, meas_data_dict_input)
#
# save_report(doc, path, 'test')
#print(get_floor_list(pictures_list))
#print(get_list_of_floor_pictures(3, pictures_list))
doc = Document()
add_services_report_table(path, doc)