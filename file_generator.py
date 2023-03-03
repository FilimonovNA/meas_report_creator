import Analyze
from Analyze import Query


'''CONSTANTS'''
UNDEFINED_FLOOR_NUMBER = 999
OUTDOOR_FLOOR_NUMBER = 777
NO_SYMBOL_ID = -1

WARINING = 'WARNING'
ERROR = 'ERROR'

			
'''DICT slave_number: KPIs '''
#KPI = {
#	'1':[get_rxle(meas)],
#	'2':[get_rscp(meas), get_dl_3g(meas), get_ul_3g(meas)],
#	'3':[get_rsrp(meas), get_dl_4g(meas), get_trhld2.5(meas)],
#	'4':[get_mos_mo(meas)],
#	'5':[get_mos_mt(meas)],
#	'6':[get_ul_4g(meas)]
#	}


#def print_all_object_attributes(data):
#	for att in dir(data):
#		Analyze.Log.Write(att)
#		Analyze.Log.Write(getattr(data, att))


''' list of user selected meas'''
def get_measurements_list():
	measurements_list = Analyze.Workspace.GetSelectedMeasurements() 
	meas_for_query_list = []
	
	for i in range(len(measurements_list)):
		measurement = measurements_list[i]
		measurement = rename_for_query(measurement)
		meas_for_query_list.append(measurement)
	
	return sorted(meas_for_query_list)


'''replace . -> : for SQL '''
def rename_for_query(meas):
	name = meas.FullName			
	
	for letter in name:  			
	    if letter == '.':
	        name = name.replace(letter, ":")
	
	return name


'''slave number'''
'''return number of slave (1, 2, 3, 4, 5, 6, 11)'''
def get_slave_number(meas):
	if meas[-2] == ':':
		phone_number = meas[-1:]
	else:
		phone_number = meas[-2:]
	
	return int(phone_number)
	

'''exta (delete)'''
#def get_meas_name(meas):

#	if meas== ':':
#			meas_name_for_workbook = meas[-1:]
#	else:
#		meas_name_for_workbook = meas[-2:]		
		
#	current_floor = get_floor(meas)
#	if current_floor not in [-999, 777]:
#		current_floor = current_floor + 'fl'
#		
#	return current_floor + meas_name_for_workbook
'''extra (delete)'''



'''FLOOR SEARCH'''
def try_search_floor_before(string_name, start_fl_num):
    
    #    Before fl
    if string_name[start_fl_num - 1].isnumeric() and \
            (string_name[start_fl_num - 2].isnumeric() or
             string_name[start_fl_num - 2] == '-') and \
            string_name[start_fl_num - 3] in ['-', '_']:

        end_fl_num = start_fl_num
        start_fl_num -= 2

        return int(string_name[start_fl_num:end_fl_num])

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

        return int(string_name[start_fl_num:end_fl_num])

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
            return int(floor)

    # outdoor
    elif string_name.find('out') != NO_SYMBOL_ID or string_name.find('Out') != NO_SYMBOL_ID or string_name.find(
            'street') != NO_SYMBOL_ID or string_name.find('Street') != NO_SYMBOL_ID:
        return OUTDOOR_FLOOR_NUMBER

	# in other cases
    else:
        return UNDEFINED_FLOOR_NUMBER
''' END OF FLOOR FIND'''


''' Print all meas in log window (debug)'''
def print_meas_list(meas_list):
	for elem in meas_list:
		Analyze.Log.Write(elem)


''' get log name without number'''
def get_log_name(meas):
    return meas[:-3] if meas[-2].isdigit() else meas[:-2]


''' get dict floor_number = slaves '''
def get_dict_floor_slaves(meas_list):
    floor_slaves = {}

    for meas in meas_list:
        meas_floor = get_floor(meas)
        slave_number = get_slave_number(meas)

        i = 0.1
        is_in_dict = 0
        while (is_in_dict != 1):
        
            if meas_floor not in floor_slaves.keys():
                '''first input for all'''
                floor_slaves.update({meas_floor:[meas]})
                is_in_dict = 1
                
#            elif meas_floor in floor_slaves.keys() and meas_floor != -999:
#                '''UNDEFINED'''
#                floor_slaves.get(meas_floor).append(meas)
#                is_in_dict = 1

            elif meas_floor in floor_slaves.keys():		# if slave already in floor number , floor number will be .1->.2->.3
                '''2+ input for all'''
                current_log_name = get_log_name(meas)
                dict_log_name = get_log_name(floor_slaves.get(meas_floor)[0])
              
                if current_log_name == dict_log_name:
                    floor_slaves.get(meas_floor).append(meas)
                    is_in_dict = 1
                    
                else:
                    meas_floor = round(meas_floor+i,1)
                    
    return floor_slaves



'''floor_data dict ''' 
def get_one_floor_data(meas_list):
	
	rxle = 'None'
	rscp = 'None' 
	rsrp = 'None'
	dl_3g = 'None'
	ul_3g = 'None'
	dl_4g = 'None'
	ul_4g = 'None' 
	trh25 = 'None'
	mos = 0
	mos_mo = 0
	mos_mt = 0	
	for meas in meas_list:
		slave_number = get_slave_number(meas)
		if slave_number == 1:
			rxle = get_rxle(meas) 			# ok add channels in SQL query
			
		elif slave_number == 2:
			rscp = get_rscp(meas) 			# ok add channels in SQL query
			dl_3g = get_dl(meas)	 		# ok
			ul_3g = get_ul(meas) 			# ok
		
		elif slave_number == 3:
			rsrp = get_rsrp(meas)			# ok add channels in SQL query 
			dl_4g = get_dl(meas) 			# ok
			trh25 = get_trh25(meas)
		
		elif slave_number == 4:
			mos_mo = get_mos_dl(meas) 		# ok
		
		elif slave_number == 5:
			mos_mt = get_mos_dl(meas)		# ok
		
		elif slave_number == 6:
			ul_4g = get_ul(meas)			# ok
	
	if mos_mo == 'None' or mos_mt == 'None':
		mos = 'None'
	else:
		mos = round((mos_mt + mos_mo)/2,2)

	''' structure for 1 floor '''		
	floor_data = {
				'RxLevel': str(rxle),
				'RSCP': str(rscp),
				'RSRP':str(rsrp),
				'AVG DL/UL 3G': str(dl_3g) + '/' + str(ul_3g),
				'AVG DL/UL 4G':str(dl_4g) + '/' + str(ul_4g),
				'DL 4G < 2.5': str(trh25),
				'AVG MOS': str(mos)
				}

	return floor_data


''' AVG DL'''
def get_dl(meas):

	query_name = 'SELECT SUM(TO_FLOAT(T_DIFFERENCE(x.sql_time,dreq.sql_time))/1000) AS "Download time",SUM("transferred_bytes_dl") FROM "Nemo"."DCOMP+" x INNER JOIN "Nemo.Connection"."DataTransfer" conn ON conn.the_ending = x.oid INNER JOIN "Nemo"."DREQ+" dreq ON conn.the_beginning = dreq.oid LEFT OUTER JOIN "Nemo.DREQ"."FTP+" ftp ON ftp.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."HTTP+" http ON http.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."SMTP+" smtp ON smtp.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."POP3+" pop3 ON pop3.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."MMS+" mms ON mms.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."WAP+" wap ON wap.the_connection = x.the_connection WHERE transferred_bytes_dl IS NOT NULL /* "MEAS('+ meas +')" */'
	
	#'SELECT AVG("app_throughput_downlink") FROM "Nemo"."DAS+" x /* "MEAS('+ meas +')" */'
	query_file = Query(query_name)
	
	for data_str in query_file.Run():
		if data_str[0] not in [None, 0] and data_str[1] not in [None, 0]:	
			return round(data_str[1]*8/data_str[0]/1000.0/1000.0, 2)
		else:
			return 'None'


''' AVG UL'''
def get_ul(meas):
	query_name = 'SELECT SUM(TO_FLOAT(T_DIFFERENCE(x.sql_time,dreq.sql_time))/1000) AS "Upload time",SUM("transferred_bytes_ul") FROM "Nemo"."DCOMP+" x INNER JOIN "Nemo.Connection"."DataTransfer" conn ON conn.the_ending = x.oid INNER JOIN "Nemo"."DREQ+" dreq ON conn.the_beginning = dreq.oid LEFT OUTER JOIN "Nemo.DREQ"."FTP+" ftp ON ftp.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."HTTP+" http ON http.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."SMTP+" smtp ON smtp.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."POP3+" pop3 ON pop3.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."MMS+" mms ON mms.the_connection = x.the_connection LEFT OUTER JOIN "Nemo.DREQ"."WAP+" wap ON wap.the_connection = x.the_connection WHERE transferred_bytes_ul IS NOT NULL /* "MEAS('+ meas +')" */'
	
	#'SELECT AVG("app_throughput_uplink") FROM "Nemo"."DAS+" x /* "MEAS('+ meas +')" */'
	query_file = Query(query_name)
	for data_str in query_file.Run():	
		if data_str[0] not in [None, 0] and data_str[1] not in [None, 0]:	
			return round(data_str[1]*8/data_str[0]/1000.0/1000.0, 2)
		else:
			return 'None'

''' AVG Rx Level'''
def get_rxle(meas):
	query_name = 'SELECT AVG("rx_level_sub") FROM "Nemo.GSM"."RXL+" x WHERE "server"=1  /* "MEAS('+ meas +')" */'
	query_file = Query(query_name)
	for data_str in query_file.Run():	
		if data_str[0] not in [None, 0]:
			return round(data_str[0],2)
		else:
			return 'None'
		
''' AVG RSCP'''
def get_rscp(meas):
	query_name = 'SELECT  AVG("rscp") FROM "Nemo.UMTS.ECNO"."Cell+" x WHERE "cell_type" = 0 AND "order" = 1 AND "channel_number" IN (2938, 10638, 10662, 10687) /* "MEAS(' + meas + ')" */'
	query_file = Query(query_name)
	for data_str in query_file.Run():	
		if data_str[0] not in [None, 0]:
			return round(data_str[0],2)
		else:
			return 'None'
		
''' AVG RSRP'''
def get_rsrp(meas):
	query_name = 'SELECT  AVG("lte_received_power") FROM "Nemo.LTE.CELLMEAS"."Cell+" x WHERE "lte_cell_type"=0 AND "channel_number" IN (6338, 6350, 1602, 1458, 2850, 3048, 37900, 225) /* "MEAS(' + meas + ')" */'
	query_file = Query(query_name)
	for data_str in query_file.Run():	
		if data_str[0] not in [None, 0]:
			return round(data_str[0],2)
		else:
			return 'None'
		
'''thr'''
def get_trh25(meas):
	query_name_full = 'SELECT COUNT("app_throughput_downlink") FROM "Nemo"."DAS+" /*MEAS(' + meas + ')" */'
	query_name_trh = 'SELECT COUNT("app_throughput_downlink") FROM "Nemo"."DAS+" x WHERE "app_throughput_downlink" < 2500000 /*MEAS(' + meas + ')" */'

	trh = 0
	full = 0
	result = 0
	
	query_full = Query(query_name_full)
	query_trh = Query(query_name_trh)

	for data_str in query_full.Run():
		full = data_str[0]
	for data_str in query_trh.Run():
		trh = data_str[0]
		
	if full not in [None, 0]:	
		result = trh*100.0/full*1.0
		result = round(result,2)
	elif full == trh and full not in [None, 0]:
		result = 0.00
	else:
		result = None	
	return result
		
''' AVG MOS'''
def get_mos_dl(meas):
	query_name = 'SELECT  AVG("aq_mean_dl") FROM "Nemo"."AQDL+" WHERE mos_type_dl != 0 /* "MEAS('+ meas +')" */'
	query_file = Query(query_name)
	for data_str in query_file.Run():	
		if data_str[0] not in [None, 0]:
			return round(data_str[0],2)
		else:
			return 'None'
		
''' input for file'''
def get_result(fs_dict):

#	result = {floor_num : floor_data}
	result = {}
	for floor in fs_dict.keys():
		result.update({floor:get_one_floor_data(fs_dict.get(floor))})
	
	return result

''' Print result in log window (debug)'''
def print_result(result):
	for floor in result.keys():
		Analyze.Log.Write(floor)
		for data in result.get(floor):
			Analyze.Log.Write(data + ':     ' + result.get(floor).get(data))
			#for elem in data.value():
			#	Analyze.Log.Write(elem)

'''Write file'''
def write_file(result):
	path = 'C:/RC_data/services_report.txt'
	with open(path, 'w') as file:
		for floor in result.keys():
			file.write(str(floor) + ':')
			for data in result.get(floor):
				file.write(data + '::' + result.get(floor).get(data) + ';')
			file.write('\n')
			
	

''' Main '''
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
		print_result(result)
		write_file(result)
		Analyze.Log.Write('File creator finished')

#main()