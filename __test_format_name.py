name_list = ['vtb-krasnovorot-fl-2209Sep_122341', 'vtb-krasnovorot_fl-2209Sep_122341',
             'vtb-krasnovorot-fl_2209Sep_122341', 'vtb-out_snovorot-10fl-2209Sep_122341',
             'vtb-krasnovorot_7fl-2209Sep_122341', 'vtb-krasnovorot-10fl_2209Sep_122341',
             'vtb-krasnovorot_fl-10_2209Sep_122341', 'vtb-krasnovorot_out-2209Sep_122341',
             'vtb-krasnovorot-street_2209Sep_122341', 'vtb-krasnovorot-fl-7-2209Sep_122341',
             'vtb-krasnovorot_fl10-2209Sep_122341', 'vtb-krasnovorot-fl-10_2209Sep_122341',
             'vtb-krasnovorot-1_0fl-2209Sep_122341', 'vtb-krasnovorot_10_-1fl-2209Sep_122341',
             'vtb-krasnovorot-10fl_2209Sep_122341']


# result_list = ['error', 'error', 'error', '1', '1', '1', ' 1', '1', '1', '-7', '10', 'error', '0', '-1', '10']

'''FLOOR SEARCH'''

workbook_list_1 = ['2g']				# Long call + scanner
workbook_list_2 = ['3g', 'dl_ul_3g']	# DL/UL
workbook_list_3 = ['4g', 'dl_4g'] 		# Endless DL
workbook_list_4 = ['mos_mo'] 			# MO
workbook_list_5 = ['mos_mt']			# MT
workbook_list_6 = ['ul_4g', 'csfb']		# CSFB + UL

workbook_list_11 = [
					'2g_best',	'3g_best',
					'4g_best', 'lte_800_best',
					'lte_1800_best', 'lte_2600_best'
					] 					# Scanner

workbook_dict = {
				'1' : workbook_list_1,'2' : workbook_list_2,
				'3' : workbook_list_3, '4' : workbook_list_4,
				'5' : workbook_list_5, '6' : workbook_list_6,
				'11' : workbook_list_11
				}

# real workbook names line: 		rg_indoor_2g / rg_outdoor_2g

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
				'2g_best' : '10',			# NO / NO
				'3g_best' :	'11',			# NO / NO
				'4g_best' : '12',			# NO / NO
				'lte_2600_best' : '13',		# NO / NO
				'lte_1800_best' : '14',		# NO / NO
				'lte_800_best' : '15'		# NO / NO
				}



def try_search_floor_before(string_name, start_fl_num):
    # Before fl
    if string_name[start_fl_num - 1].isnumeric() and \
            (string_name[start_fl_num - 2].isnumeric() or
             string_name[start_fl_num - 2] == '-') and \
            string_name[start_fl_num - 3] in ['-', '_']:

        end_fl_num = start_fl_num
        start_fl_num -= 2

        return int(string_name[start_fl_num:end_fl_num])

    elif int(string_name[start_fl_num - 1].isnumeric()):

        return int(string_name[start_fl_num - 1])
    else:
        return -999


def try_search_floor_after(string_name, start_fl_num):
    # After fl
    if (string_name[start_fl_num + 2].isnumeric() or
        string_name[start_fl_num + 2] == '-') \
            and string_name[start_fl_num + 3].isnumeric() \
            and (string_name[start_fl_num + 4] in ['-', '_']):

        start_fl_num += 2
        end_fl_num = start_fl_num + 2

        return int(string_name[start_fl_num:end_fl_num])

    elif string_name[start_fl_num + 2].isnumeric():

        return int(string_name[start_fl_num + 2])

    # if floor was founded without number
    else:
        return -999


# find floor in measure name
def get_floor(string_name):
    '''only 2 symbols for each floor [-9 - 99]'''
    start_fl_num = string_name.rfind('fl')
    # indoor

    if start_fl_num != -1:
        floor = try_search_floor_before(string_name, start_fl_num)
        if floor == -999:
            return try_search_floor_after(string_name, start_fl_num)
        else:
            return floor

# outdoor
    elif not (not (string_name.find('out') != -1) and not (string_name.find('Out') != -1) and not (
                string_name.find('street') != -1) and not (string_name.find('Street') != -1)):
        return 'Outdoor'

# in other cases
    else:
        return 'Undefined'

''' END OF FLOOR FIND'''


def get_slave_number(meas):
    '''return number of slave (1, 2, 3, 4, 5, 6, 11)'''
    if meas[-2] == '.': #.FullName[-2] == '.':
        return meas[-1:] #.FullName[-1:]
    else:
        return meas[-2:]    #.FullName[-2:]  # if 11/17


def get_workbook_name(floor, workbook_str):
    ''' return workbook name in Workbooks/User/rc folder '''
    if floor == 'Outdoor':
        name_workbook = 'rc_outdoor_' + workbook_str
    else:
        name_workbook = 'rc_indoor_' + workbook_str
    return name_workbook


''' Main function '''


def main():
    measurements = ['Shate_M-plus__fl1_23Feb06_102608.1', 'Shate_M-plus__fl1_23Feb06_102688.1',
                    'Shate_M-plus__fl1_23Feb06_102608.1', 'Shate_M-plus__fl1_23Feb06_102688.2',
                    'Shate_M-plus__fl1_23Feb06_102608.1', 'Shate_M-plus__fl1_23Feb06_102688.3']  # get selected meas list
    all_meas_dict = {}

    for meas in measurements:  # number of slave (1, 2, 3, 5, 7, 11)
        slave_number = get_slave_number(meas)
        current_floor = get_floor(meas) #.FullName)
        #Analyze.Log.Write(slave_number)

        ''' START OF BLOCK'''
        ''' Write to the dict, avoid overwriting pictures '''
        flag = 0 # flag for current floor
        i = 0.1
        j = 1
        while flag != 1:
            end_floor_int = int(current_floor)
            end_floor_str = str(current_floor)
            if slave_number not in all_meas_dict.keys():
                all_meas_dict[slave_number] = [current_floor]
                flag = 1
               # print(f'slave_floors:{all_meas_dict.get(slave_number)}')
            elif slave_number in all_meas_dict.keys() and current_floor not in all_meas_dict.get(slave_number):
                all_meas_dict.get(slave_number).append(current_floor)
                flag = 1
            else:
                if type(current_floor) in ['int', 'float']:
                    current_floor = round(current_floor + i, 1) #+ '.' + i
                else:
                    current_floor = current_floor + str(j)
                    j += 1
          #  print(current_floor)

    print(all_meas_dict)


main()

