from datetime import date

'''GLOBAL CONSTANTS'''
PRODUCT_NAME = 'Report Creator'                         # Название программы
FOUNDER = 'Filimonov'                                   # Разработчик
VERSION = '0.0'                                         # Версия программы 
YEARS = '2022-2023'                                     # Годы поддержки
MAIL = 'nikita.filimonov@megafon.ru'                    # Почта для связи
LAST_UPDATE_TIME = date.today().strftime("%d-%m-%Y")    # Дата последней сборки


'''GUI CONSTANTS'''
MAIN_WINDOW_WIDTH = 700                              # Ширина окна приложения
MAIN_WINDOW_HEIGHT = 400                             # Высота окна приложения
LABEL_WIDTH = 250                                    # Ширина поля для ввода информации
LABEL_HEIGHT = 30                                    # Высота поля для ввода информации
VERTICAL_BLOCK_DISTANCE = 70                         # Расстояние между блоками по высоте


'''REPORT CONSTANTS'''
UNDEFINED_FLOOR_NUMBER = 999                         # Если этаж не обнаружен
OUTDOOR_FLOOR_NUMBER = 777                           # Для outdoor
OUTDOOR_TITLE = 'Outdoor'                            # Единое название outdoor
UNDEFINED_FLOOR_TITLE = 'Undefined'                  # Единой название для измерений без этажа
NO_SYMBOL_ID = -1                                    # Если нет символа, возвращается -1
NEMO_POSTFIX_LENGTH = 16                             # Длина постфикса в названии файла измерений default 16
SCANNER_SCRIPTS_NUMBERS = ['10', '11', '12']         # Номера скриптов сканнера

PICTURES_CAPTIONS = {'01': 'Качественные показатели покрытия 2G',
                        '02': 'Качественные показатели покрытия 3G',
                        '03': 'Качественные показатели покрытия 4G',
                        '04': 'Скорость ППД DL/UL 3G',
                        '05': 'Скорость ППД DL 4G',
                        '06': 'Скорость ППД UL 4G',
                        '07': 'MOS MO',
                        '08': 'MOS MT',
                        '09': 'Функциональные показатели CSFB',
                        '10': 'Функциональные показатели 2G best scanner',
                        '11': 'Функциональные показатели 3G best scanner',
                        '12': 'Функциональные показатели LTE best scanner'
                        }                           # Соответствие названия номера картинки и названия скрипта

PROCENTS_VCR_KPIS = [ '6. Call setup success rate',
                      '7. Call completion rate',
                      '8. Call dropped rate',
                      'Успешность установления вызова',
                      'Успешность завершения вызова',
                      'Процент обрывов'
                      ]                                  # Список KPI для voice call report которым нужен % в конце

VCR_TRANSLATE = { '1. Call attempt': 'Количество попыток установления вызова',
                  '2. Call attempt failure': 'Количество неуспешных попыток',
                  '3. Call connected': 'Количество начавшихся звонков',
                  '4. Call dropped': 'Количество обрывов вызова',
                  '5. Call disconnected': 'Количество окончившихся вызовов',
                  '6. Call setup success rate' : 'Успешность установления вызова',
                  '7. Call completion rate': 'Успешность завершения вызова',
                  '8. Call dropped rate': 'Процент обрывов'
                  }                                   # Перевод KPI для voice call report

SR_COLUMNS = [ '',
               'RxLevel',
               'RSCP',
               'RSRP',
               'AVG DL/UL 3G',
               'AVG DL/UL 4G',
               'DL 4G < 2.5',
               'AVG MOS'
               ]                                    # названия колонок для services report

GREEN = "00b33c"                                    # цвета для заливки ячеек
LIGHT_GREEN = "00e600"
ORANGE = "ff6600"
RED = "ff0000"

external = [ None,
             'None',
             '',
             '1. Отчет подготовил: ',
             '3. Дата измерений: ',
             '4. Адрес: ',
             'report name',
             '2. Измерения провел: ',
             '5. Объект: '
             ]                                      # внешние поля, заполняемые юзером
