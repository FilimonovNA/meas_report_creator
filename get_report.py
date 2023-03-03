from get_report_body import *
from get_external import *
from docx import Document


def generate_file(path_with_pictures, report_path, user_meas_data):
    report_doc = Document()
    file_name = get_file_name(user_meas_data['report name'])

    if save_report(report_doc, report_path, file_name) != 1:
    # path = 'C:/Users/PC/Desktop/Work/'  # legacy for save time
    # path_with_pictures = path + '/Pictures'
    # path_with_pictures = select_path()
       # report_doc = Document()
        set_margin(report_doc)
      #  file_name = get_file_name(user_meas_data['<Report name>'])
        all_pictures = get_pictures_list(path_with_pictures)

        if len(all_pictures) == 0:
            return "Картинки\nне найдены"

        all_floors = get_floor_list(all_pictures)

        if len(all_floors) == 0:
            return "Некорректный формат\nназвания картинок"
        # report_path = select_path()
        # report_path = path

        add_footer_in_doc(report_doc, user_meas_data)
        add_header_in_doc(report_doc)
        add_first_page_in_doc(report_doc, user_meas_data)

        add_voice_call_report_table(report_path, report_doc)
        add_services_report_table(report_path, report_doc)
        add_crossmod(report_path, report_doc)

        absolut_picture_number_in_file = 1

        for current_floor in all_floors:
            current_floor_pictures_list = get_list_of_floor_pictures(current_floor, all_pictures)
            absolut_picture_number_in_file = add_floor_in_report(path_with_pictures, report_doc, current_floor,
                                                                 current_floor_pictures_list,
                                                                 absolut_picture_number_in_file)
        save_report(report_doc, report_path, file_name)
        return "Отчет\nсоздан"
    else:
        remove_report(report_doc, report_path, file_name)
        return "Закройте\nфайл"


# Получаем название выходного файла
def get_file_name(name):
    if len(name) > 0:
        return name
    else:
        return name+"report"
