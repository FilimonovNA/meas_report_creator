from os import system, listdir, path, unlink, startfile
from tkinter import Tk, Label, Button, filedialog, Entry, Text
from const import *
from get_report import generate_file
from join_meas import main as join_meas


window = Tk()
window.title(f"{PRODUCT_NAME} v.{VERSION}{' ' * 10}{' ' * 10}Moscow")
window.geometry(f'{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}')
window.minsize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
window.maxsize(MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
window['background'] = '#eeeeee'

# image_bg = PhotoImage(file="C:\\Python_Projects\\nuclear\\")
# canvas_bg = Canvas(window, width=MAIN_WINDOW_WIDTH, height=MAIN_WINDOW_HEIGHT)
# canvas_bg.pack(fill="both", expand=True)
# canvas_bg.create_image(-50, -50, image=image_bg, anchor="nw")
# meas_data_dict = {'<Reporter name>': '<Reporter name>', '<Measurer name>': '<Measurer name>',
#                 '<Date>': '<Date>', '<Address>': '<Address>', '<Building>': '<Building>'}


def set_defaults():
    btn_configure.config(text="Создать\nОтчет")
    text_send_email.place(x=171, y=321, width=1, height=1)
    btn_join_meas.config(text='Объединить измерения')
    btn_clear_rg_data.config(text='Очистить папку RG_data')
    return 1


def select_pictures_path():
    set_defaults()
    user_path = filedialog.askdirectory(title="Select a File")
    if len(user_path) < 1:
        label_path_with_pictures.config(text='Ваш путь будет здесь')
    else:
        label_path_with_pictures.config(text=user_path)
    pic_path = user_path
    return pic_path


def select_report_path():
    set_defaults()
    user_path = filedialog.askdirectory(title="Select a File")
    if len(user_path) < 1:
        label_report_path.config(text='Ваш путь будет здесь')
    else:
        label_report_path.config(text=user_path)
    rep_path = user_path
    return rep_path


def generate():
    set_defaults()
    if label_path_with_pictures['text'].find('/') == NO_SYMBOL_ID or \
            label_report_path['text'].find('/') == NO_SYMBOL_ID:
        btn_configure.config(text="Выберите\n обе директории")
    else:
        user_meas_data = get_meas_data_dict()
        btn_configure.config(
            text=generate_file(label_path_with_pictures['text'], label_report_path['text'], user_meas_data))
        report_path = label_report_path["text"]
        if btn_configure['text'] == "Отчет\nсоздан":
            report_path = path.realpath(report_path)
            startfile(report_path)


def get_meas_data_dict():
    set_defaults()
    meas_data_dict = {
                       '1. Отчет подготовил': None,
                       '2. Измерения провел: ': None,
                       '3. Дата измерений: ': None,
                       '4. Адрес: ': None,
                       '5. Объект: ': None,
                       'report name': 'report'
                       }

    meas_data_dict_input = {
                            '1. Отчет подготовил: ': entry_name_reporter.get(),
                            '2. Измерения провел: ': entry_name_measurer.get(),
                            '3. Дата измерений: ': entry_date.get(),
                            '4. Адрес: ': entry_address.get(),
                            '5. Объект: ': entry_building.get(),
                            'report name': entry_file_name.get()
                            }
    for value in meas_data_dict_input:
        if len(meas_data_dict_input[value]) > 0:
            meas_data_dict[value] = meas_data_dict_input[value]
        else:
            meas_data_dict[value] = ''

    return meas_data_dict


# Сохранение e-mail в буфер
def add_to_clip_board(text):
    #set_defaults()
    command = 'echo ' + text.strip() + '| clip'
    system(command)


def send_email():
    set_defaults()
    print("Button has been picked")
    text_send_email.place(x=170, y=320, width=250, height=70)
    # os.start_file("outlook")
    # os.system("start \"\" mailto:nikita.filimonov@megafon.ru?subject=Обратная%20связь%20Report%20Generator")
    # os.system("start \"\" mailto:nikita.filimonov@megafon.ru?subject=Обратная%20связь%20Report%20Generator")

    text_send_email.insert("1.0", "Отправьте сообщение на почту\nnikita.filimonov@megafon.ru\n"
                                 "с темой: Report generator\np.s. Почта уже скопирована\n")
    add_to_clip_board('nikita.filimonov@megafon.ru')


def clear_rg_data():
    set_defaults()
    # user_path = filedialog.askdirectory(title="Выберите папку для очистки")
    folder = 'C:/RG_data/'
    for filename in listdir(folder):
        file_path = path.join(folder, filename)
        try:
            if path.isfile(file_path) or path.islink(file_path):
                unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    btn_clear_rg_data.config(text='Папка очищена')


def join():
    set_defaults()
    btn_join_meas.config(text='Объединяю...')
    # join_pg.config(mode="indeterminate")
    answer = join_meas()
    btn_join_meas.config(text=answer)


def config():
    set_defaults()
    print(window.title)


# anchor "n", "ne", "e", "se", "s", "sw", "w", "nw", or "center"
label_select_pictures_path = Label(window, text="Путь с файлами из Nemo", anchor="w")
label_select_pictures_path.place(x=10, y=10, width=150, height=20)  #

btn_select_pictures_path = Button(window, text="Выбрать", command=select_pictures_path)
btn_select_pictures_path.place(x=165, y=10, width=80, height=20)

label_path_with_pictures = Label(window, text="Выбранный путь", anchor="e")
label_path_with_pictures.place(x=250, y=10, width=120, height=20)

label_select_report_path = Label(window, text="Путь для отчета", anchor="w")
label_select_report_path.place(x=10, y=40, width=150, height=20)

btn_select_report_path = Button(window, text="Выбрать", command=select_report_path)
btn_select_report_path.place(x=165, y=40, width=80, height=20)

label_report_path = Label(window, text="Выбранный путь", anchor="e")
label_report_path.place(x=250, y=40, width=120, height=20)

btn_configure = Button(window, text="Создать\nОтчет", command=generate, font=('Times', 15), fg='#f5f5f5',
                       background="#66b0ab")
btn_configure.place(x=520, y=270, width=170, height=60)

# names_list = ['Филимонов', 'Елисеев', 'Мартынов', 'Жбанов', 'Кочетков', 'Шиянов', 'Мещеряков']

label_name_measurer = Label(window, text="Измерения провел:", anchor="w")
label_name_measurer.place(x=10, y=110, width=120)
entry_name_measurer = Entry(window)
entry_name_measurer.place(x=140, y=110, width=250)  # x = 300 - EOF

label_name_reporter = Label(window, text="Отчет выполнил:", anchor="w")
label_name_reporter.place(x=10, y=140, width=100)
entry_name_reporter = Entry(window)
entry_name_reporter.place(x=140, y=140, width=250)  # x = 300 - EOF

label_date = Label(window, text="Дата:", anchor="w")
label_date.place(x=10, y=170, width=100)
entry_date = Entry(window)
entry_date.place(x=140, y=170, width=250)  # x = 300 - EOF

label_address = Label(window, text="Адрес:", anchor="w")
label_address.place(x=10, y=200, width=100)
entry_address = Entry(window)
entry_address.place(x=140, y=200, width=250)  # x = 300 - EOF

label_building = Label(window, text="Объект(БЦ,ТЦ):", anchor="w")
label_building.place(x=10, y=230, width=100)
entry_building = Entry(window)
entry_building.place(x=140, y=230, width=250)  # x = 300 - EOF

label_file_name = Label(window, text="Название файла:", anchor="w")
label_file_name.place(x=10, y=260, width=100)
entry_file_name = Entry(window)
entry_file_name.place(x=140, y=260, width=250)  # x = 300 - EOF

label_file_name_end = Label(window, text=".docx", anchor="w")
label_file_name_end.place(x=375, y=260, width=40)

text_send_email = Text(window)
text_send_email.place(x=171, y=321, width=1, height=1)

btn_send_email = Button(window, text="Сообщить о проблеме", command=send_email)
btn_send_email.place(x=10, y=360, width=150, height=30)

btn_clear_rg_data = Button(window, text="Очистить папку RG_data", command=clear_rg_data)
btn_clear_rg_data.place(x=470, y=10, width=150)

btn_join_meas = Button(window, text="Объединить измерения", command=join)
btn_join_meas.place(x=470, y=50, width=150)

# join_pg = ttk.Progressbar(orient="horizontal", length=150, value=0)
# join_pg.place(x=470, y=70, width=150)

btn_quit = Button(window, text="Выход", command=window.destroy)
btn_quit.place(x=620, y=360, width=70, height=30)

# pb = ttk.Progressbar(window, mode="determinate")
# pb.pack()
# pb.place(x=470, y=90, width=150)

# threading.Thread(target=progress).start()

window.mainloop()
