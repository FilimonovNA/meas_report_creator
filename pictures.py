import Analyze
import time

'''CONSTANTS'''
UNDEFINED_FLOOR_NUMBER = 999
OUTDOOR_FLOOR_NUMBER = 777 
NO_SYMBOL_ID = -1


workbook_list_1 = ['2g']				# Long call + scanner
workbook_list_2 = ['3g', 'dl_ul_3g']	# DL/UL
workbook_list_3 = ['4g', 'dl_4g'] 		# Endless DL
workbook_list_4 = ['mos_mo'] 			# MO
workbook_list_5 = ['mos_mt']			# MT
workbook_list_6 = ['ul_4g', 'csfb']		# CSFB + UL

workbook_list_11 = ['2g_best', '3g_best', '4g_best'] 	# Scanner

workbook_dict = {
				'1' : workbook_list_1,'2' : workbook_list_2, 
				'3' : workbook_list_3, '4' : workbook_list_4, 
				'5' : workbook_list_5, '6' : workbook_list_6,
				'11' : workbook_list_11
				}

# real workbook names like: 		rg_indoor_2g / rg_outdoor_2g
picture_dict = {							# in / out

				'2g' : '01', 				# ok / ok
				'3g' : '02',				# ok / ok
				'4g' : '03',				# ok / ok
				'dl_ul_3g' : '04',			# ok / ok
				'dl_4g' : '05',				# ok / ok
				'ul_4g' : '06',				# ok / ok
				'mos_mo' : '07',			# ok / ok
				'mos_mt' : '08',			# ok / ok
				'csfb' : '09',				# ok / ok
				'2g_best' : '10',			# ok / ok
				'3g_best' :	'11',			# ok / ok
				'4g_best' : '12',			# ok / ok

				}



#def print_all_object_attributes(data):
#	for att in dir(data):
#		Analyze.Log.Write(att)
#		Analyze.Log.Write(getattr(data, att))



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



def get_slave_number(meas):
    '''return number of slave (1, 2, 3, 4, 5, 6, 11)'''
    if meas.FullName[-2] == '.':
        return meas.FullName[-1:]
    else:
        return meas.FullName[-2:]		# if 11/17



def get_workbook_name(floor, workbook_str):
	''' return workbook name in Workbooks/User/rc folder '''	
	if floor >= OUTDOOR_FLOOR_NUMBER and floor <= OUTDOOR_FLOOR_NUMBER + 1:
		name_workbook = 'rc_outdoor_' + workbook_str
	else:
		name_workbook = 'rc_indoor_' + workbook_str
	return name_workbook



''' Main function '''
def main():
	
	Analyze.Log.Write('Pictures creator started work')
	measurements = Analyze.Workspace.GetSelectedMeasurements()  # get selected meas list
	
	all_meas_dict = {}
	current_meas_number = 1		# log
	all_meas_number = len(measurements) # log
	
	for meas in measurements:  # number of slave (1, 2, 3, 5, 7, 11)
		
		log_string = str(current_meas_number) + '/' + str(all_meas_number)	# log
		Analyze.Log.Write(log_string)										# log
		
		slave_number = get_slave_number(meas)
		current_floor = get_floor(meas.FullName)
		
		''' if not outdoor or undefined add fl in the end '''
		if current_floor not in [UNDEFINED_FLOOR_NUMBER,  OUTDOOR_FLOOR_NUMBER]:	
			floor_postfix = 'fl'
		else:
			floor_postfix = ''
		
		Analyze.Log.Write(slave_number)
		''' START OF BLOCK'''
		''' Write to the dict, avoid overwriting pictures '''
		is_in_dict = 0
		i = 0.1
		while is_in_dict != 1:
			if slave_number not in all_meas_dict.keys():
				all_meas_dict[slave_number] = [current_floor]
				is_in_dict = 1
			elif  slave_number in all_meas_dict.keys() and current_floor not in all_meas_dict.get(slave_number):
				all_meas_dict.get(slave_number).append(current_floor)
				is_in_dict = 1
			else:
				current_floor = round(current_floor + i,1)

		#current_floor = str(current_floor) + floor_postfix		# end name of floor
		
		''' END OF FLOOR FIND'''
        
        #if current_floor in floor_list:
        #    ''' if overwriting is come, floor + .1'''
        #    current_floor += '.' + i
        #    i += 1
		''' END OF BLOCK '''
        
        

		''' PICTURE CREATE BLOCK '''
		if slave_number in workbook_dict:
			''' Open workbooks in workbook_list for current slave '''
			for workbook_str in workbook_dict.get(slave_number):
				name_workbook = get_workbook_name(current_floor, workbook_str) 	
				newWorkbook = Analyze.Workspace.OpenWorkbook(name_workbook, meas)  # open 1 workbook and later save it in picture
				workbookpage = newWorkbook.CurrentPage
				
				''' Cause of NEMO ANALYZE!!! '''
				crutch_1 = Analyze.Workspace.OpenWorkbook('crutch', meas)  # crutch for NEMO
				counter = 0
				for elem in workbookpage.Views:
					counter += 1
					if type(elem) is Analyze.MapDataView:		#zoom map to best fit
						elem.BestFitZoom()
					
				name = 'C:\\RC_data\\{0}_{1}_{2}.png'.format(current_floor, picture_dict[workbook_str], workbook_str)
				time.sleep(1)		
				crutch_1.Close()
                # time.sleep(1)
                # for i in range(1, 100000):
                #	j = i*i
                #	j +=1
				newWorkbook.ExportPage(0, name)
				time.sleep(1)
				newWorkbook.ExportPage(0, name)
				newWorkbook.Close()

		else:
			continue
			
	Analyze.Log.Write('Pictures creator finished work')

#main()
