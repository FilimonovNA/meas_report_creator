import sys
import Analyze
sys.path.append('C:\\Nemo Tools\\Nemo Analyze\\Macros\\V2.0') 	# Путь до директории со скриптом

import file_generator
from file_generator import main as get_services_report		# Импорт модуля генерации файла services_report.txt

import pictures
from pictures import main as get_pictures				  	# Импорт модуля генерации картинок

import crossmod
from crossmod import main as get_crossmod_file				# пересечение по mod 6/30 crossmod.txt

import voice_call_report	
from voice_call_report import main as get_voice_call_report	# для сводной таблицы services_report.txt


reload(file_generator)			# Обновление модулей каждый раз потому что НЕМО)
reload(pictures)				# --||--
reload(crossmod)				# --||--
reload(voice_call_report)		# --||--


def main():
	Analyze.Log.Write('STARTED')
	
	get_services_report()		# Генерируем файл с уровнями/скоростями/MOS
	get_voice_call_report()		# Генерируем файл VoiceCallReport
	get_crossmod_file()			# Генерирует файл с пересечением PCI
	get_pictures()				# Генерируем картинки для отчета
	
	Analyze.Log.Write('FINISHED')
	Analyze.Windows.MessageBox('Work inside nemo finished \n let\'s start create report', 'SUCCESS', "ok")
	
main()


#	Необходимые тестовые данные
# 		indoor + outdoor
#		indoor 2 прохода 1 этажа
#		outdoor 2 лога с одного измерения
#		indoor с файлами без номера этажа
#		indoor с 2+ файлами без номера этажа
