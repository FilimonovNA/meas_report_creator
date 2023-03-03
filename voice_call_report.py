import Analyze
from Analyze import Query

PATH = 'C://RC_data//voice_quality_report.txt'
COL_NUM_CA = 13		#number of colonums in call attempt query

def get_measurements_list(selected_measurements):
	meas_for_query_list = []
	for i in range(len(selected_measurements)):
		measurement = selected_measurements[i]
		measurement = rename_for_query(measurement)
		meas_for_query_list.append(measurement)
	return sorted(meas_for_query_list)


def rename_for_query(measurement):
	name = measurement.FullName			
	for letter in name:  			
	    if letter == '.':
	        name = name.replace(letter, ":")
	# return meas.HintTitle
	return name


def get_meas_string_for_query(measurements_list):
	if len(measurements_list) > 0:
		meas_str = measurements_list[0]
		for i in range(1, len(measurements_list)):
			meas_str += "|" + measurements_list[i]
		return meas_str
	else:
		return None


def get_voice_quality_report(dict):
	
	call_attempt = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_attempt_failure = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_connected = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_dropped = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_disconnected = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_setup_rate = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_completion_rate = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	call_dropped_rate = {'2G':'None', 'CSFB':'None', 'VoLTE':'None'} 
	
	for technology, meas_str in dict.items():
		if meas_str not in [None, 'None']:
			call_attempt.update({technology : get_call_attempt(meas_str)})
			call_attempt_failure.update({technology : get_call_attempt_failure(meas_str)})
			call_connected.update({technology : get_call_connected(meas_str)})
			call_dropped.update({technology : get_call_dropped(meas_str)})
			if technology == 'VoLTE':
				call_disconnected.update({technology : get_call_disconnected(meas_str)})
			else:
				call_disconnected.update({technology : get_call_disconnected(meas_str)})
	
	for technology, meas_str in call_attempt.items():
		if meas_str not in [None, 'None']:	
			call_setup_rate.update({technology : get_call_setup_rate(call_attempt.get(technology), call_attempt_failure.get(technology))})
			call_completion_rate.update({technology : get_call_completion_rate(call_connected.get(technology), call_disconnected.get(technology))})
			call_dropped_rate.update({technology : get_call_dropped_rate(call_connected.get(technology), call_dropped.get(technology))})
		
	
#	call_attempt = get_call_attempt(meas_str)
#	call_attempt_failure = get_call_attempt_failure(meas_str)
#	call_connected = get_call_connected(meas_str)
#	call_dropped = get_call_dropped(meas_str)
#	call_disconnected = get_call_disconnected(meas_str)
	
#	call_setup_rate = get_call_setup_rate(call_attempt, call_attempt_failure)
#	call_completion_rate = get_call_completion_rate(call_connected, call_disconnected)
#	call_dropped_rate = get_call_dropped_rate(call_connected, call_dropped)	
	
	
	voice_quality_report = {'1. Call attempt':call_attempt,
							'2. Call attempt failure': call_attempt_failure,
							'3. Call connected':call_connected,
							'4. Call dropped':call_dropped,
							'5. Call disconnected':call_disconnected,
							'6. Call setup success rate':call_setup_rate,
							'7. Call completion rate':call_completion_rate,
							'8. Call dropped rate':call_dropped_rate
							}
							
	#report = sorted(voice_quality_report)
	#return report
	return voice_quality_report


def get_call_attempt(meas_str):
	query = 'SELECT  x.event_id,x.time,x.sql_time _exclude_order,x.the_measured_system,CASE WHEN x.the_serving_band = 0 THEN CAST(NULL AS INT) ELSE x.the_serving_band END the_serving_band,x.call_type,"connection_direction","unique_id","phone_number","caller_phone_number","number_of_calls","call_timeout",x.gps_longitude,x.gps_latitude FROM Nemo."CAA+" x INNER JOIN "Nemo.Connection"."Voice+" z ON x.oid = z.the_attempt LEFT OUTER JOIN Nemo."CAF+" a ON a.oid = z.the_failure LEFT OUTER JOIN Nemo."CAD+" b ON b.oid = z.the_disconnect WHERE z.the_attempt IS NOT NULL AND (a.call_attempt_failure_status IS NULL OR a.call_attempt_failure_status NOT IN (3, 5)) AND (z.the_alerting IS NOT NULL OR z.the_conversation IS NOT NULL OR z.the_disconnect IS NULL OR b.call_disconnect_status NOT IN (5)) AND (call_disconnect_status IS NULL OR call_disconnect_status NOT IN (5)) AND connection_direction = 1 AND (z.the_failure IS NOT NULL OR z.the_disconnect IS NOT NULL) ORDER BY _exclude_order /* "MEAS(' + meas_str + ')" */'
	
	query_file = Query(query)
	i = 0
	for data_str in query_file.Run():
			i  += 1
	return i



def get_call_attempt_failure(meas_str):
	query = 'SELECT  a.event_id,\'Call attempt failure\' AS Event,SOS(1,a.oid) AS Event#,x.[the_measurement_title] || \'.\' || x.[the_device_extension] AS Measurement,a.time,a.sql_time _exclude_order,a.the_serving_system,a.the_serving_band,VAL_TO_STRING(\'call_attempt_failure_status\', "call_attempt_failure_status") AS "Call failure status",a.call_type,CASE WHEN a.the_serving_system = 512 THEN VAL_TO_STRING(\'cdma_call_failure_cause\', "call_failure_cause") ELSE VAL_TO_STRING(\'cc_cause\', "call_failure_cause") END AS "Network cause","call_failure_time",a.gps_longitude,a.gps_latitude FROM Nemo.[CAF+] a INNER JOIN [Nemo.Connection].[Voice+] z ON a.oid = z.the_failure INNER JOIN Nemo.[CAA+] x ON x.oid = z.the_attempt WHERE z.the_attempt IS NOT NULL AND (z.the_failure IS NOT NULL OR z.the_disconnect IS NOT NULL) AND (a.call_attempt_failure_status IS NULL OR a.call_attempt_failure_status NOT IN (3, 5)) AND connection_direction = 1 UNION ALL SELECT a.event_id,\'Call attempt failure\' AS Event, SOS(1,a.oid), x.[the_measurement_title] || \'.\' || x.[the_device_extension] AS Measurement, a.time, a.sql_time _exclude_order, a.the_serving_system, a.the_serving_band, VAL_TO_STRING(\'call_disconnect_status\', call_disconnect_status), a.call_type, VAL_TO_STRING(\'cc_cause\', cs_disc_cause), CAST(T_DIFFERENCE(a.time, x.time)/1000 AS SMALLINT) call_failure_time, a.gps_longitude, a.gps_latitude  FROM Nemo.[CAD+] a, (SELECT 0 AS call_failure_cause) INNER JOIN [Nemo.Connection].[Voice+] z ON a.oid = z.the_disconnect AND ((a.cs_disc_cause NOT IN (17) OR a.cs_disc_cause IS NULL)) AND a.call_disconnect_status NOT IN (5) INNER JOIN Nemo.[CAA+] x ON x.oid = z.the_attempt WHERE z.the_alerting IS NULL AND z.the_conversation IS NULL AND connection_direction = 1'\
	'ORDER BY _exclude_order /* "MEAS(' + meas_str + ')" */'
	i = 0
	for data_str in Query(query).Run():
		i+= 1
	return i


def get_call_connected(meas_str):
	query = 'SELECT  b.event_id,b.time,b.sql_time _exclude_order,b.the_serving_system,b.the_serving_band,b.call_type,CAST(NULL AS TINYINT) call_connection_status,TO_FLOAT(T_DIFFERENCE(b."time", T_WITH_MILLISEC_OFFSET(x.time, ISNULL(x.call_attempt_to_caa_timediff,0)*-1)))/1000 \'Call setup time\',CAST(NULL AS SMALLINT) current_tn,b.gps_longitude,b.gps_latitude FROM Nemo."CAD+" b INNER JOIN "Nemo.Connection"."Voice+" z ON b.oid = z.the_disconnect AND b.cs_disc_cause = 17 LEFT OUTER JOIN Nemo."CAA+" x  ON x.oid = z.the_attempt  WHERE z.the_attempt IS NOT NULL AND (z.the_failure IS NOT NULL OR z.the_disconnect IS NOT NULL) AND z.the_alerting IS NULL AND z.the_conversation IS NULL AND connection_direction = 1 AND (z.the_failure IS NOT NULL OR z.the_disconnect IS NOT NULL) UNION ALL SELECT IFNULL(c.event_id,cac3.event_id), IFNULL(c.time,cac3.time), IFNULL(c.sql_time,cac3.sql_time) _exclude_order, IFNULL(c.the_serving_system, cac3.the_serving_system), IFNULL(c.the_serving_band,cac3.the_serving_band), c.call_type, IFNULL(c.call_connection_status,cac3.call_connection_status), TO_FLOAT(T_DIFFERENCE(IFNULL(c.time,cac3.time), T_WITH_MILLISEC_OFFSET(x.time, ISNULL(x.call_attempt_to_caa_timediff,0)*-1)))/1000 \'Call setup time\', c.current_tn,c.gps_longitude,c.gps_latitude  FROM "Nemo.Connection"."Voice+" z LEFT OUTER JOIN Nemo."CAC+" c ON c.oid = z.the_alerting LEFT OUTER JOIN Nemo."CAC+" cac3 ON the_conversation = cac3.oid LEFT OUTER JOIN Nemo."CAA+" x  ON x.oid = z.the_attempt LEFT OUTER JOIN Nemo."CAD+" cad ON the_disconnect = cad.oid	WHERE IFNULL(z.the_alerting, z.the_conversation) IS NOT NULL  AND (connection_direction IS NULL OR connection_direction = 1) AND  (call_disconnect_status IS NULL OR call_disconnect_status <> 5) AND (z.the_failure IS NOT NULL OR z.the_disconnect IS NOT NULL)  ORDER BY _exclude_order /* "MEAS(' + meas_str + ')" */'
	i = 0
	for data_str in Query(query).Run():
		i+=1
	return  i


def get_call_dropped(meas_str):
	query = ' SELECT  b.event_id,\'Call dropped\' AS "Event",b.call_disconnect_status,CASE WHEN b.the_serving_system = 512 THEN VAL_TO_STRING(\'cdma_call_failure_cause\',"cs_disc_cause") ELSE VAL_TO_STRING(\'cc_cause\',"cs_disc_cause") END AS "Network cause",SOS(1,x.oid) AS Event#,x."the_measurement_title" || \'.\' || x."the_device_extension" AS "Measurement",b.time,b.sql_time _exclude_order,b.the_serving_system,b.the_serving_band,x.call_type,"connection_direction","call_duration",HOUR(TI_2_TIME(call_duration)) * 3600 + MINUTE(TI_2_TIME(call_duration)) * 60 + SECOND(TI_2_TIME(call_duration)) AS "Call duration (s)",b.gps_longitude,b.gps_latitude FROM Nemo."CAD+" b INNER JOIN "Nemo.Connection"."Voice+" z ON b.oid = z.the_disconnect AND (((b.call_disconnect_status > 1 AND b.call_disconnect_status NOT IN (5))  OR b.call_disconnect_status IS NULL) AND (b.cs_disc_cause NOT IN(16, 17, 18) OR b.cs_disc_cause IS NULL)) INNER JOIN Nemo."CAA+" x ON x.oid = z.the_attempt WHERE z.the_attempt IS NOT NULL AND (z.the_failure IS NOT NULL OR z.the_disconnect IS NOT NULL) AND (z.the_alerting IS NOT NULL OR z.the_conversation IS NOT NULL) AND connection_direction = 1  ORDER BY _exclude_order /* "MEAS(' + meas_str + ')" */'
	
	i = 0
	for data_str in Query(query).Run():
		i+=1
	return i


def get_call_disconnected(meas_str):
	query = 'SELECT  b.event_id,b.time,b.sql_time _exclude_order,b.the_serving_system,b.the_serving_band,b.call_type,"call_disconnect_status",CASE WHEN b.the_serving_system = 512 THEN VAL_TO_STRING(\'cdma_call_failure_cause\',"cs_disc_cause") ELSE VAL_TO_STRING(\'cc_cause\',"cs_disc_cause") END AS "Network cause",TO_FLOAT(T_DIFFERENCE(b.time, x.time))/1000 AS "Call duration",b.gps_longitude,b.gps_latitude FROM Nemo.[CAD+] b INNER JOIN [Nemo.Connection].[Voice+] z ON b.oid = z.the_disconnect INNER JOIN Nemo.[CAA+] x ON x.oid = z.the_attempt WHERE (b.cs_disc_cause IN (16,17,18) OR b.call_disconnect_status = 1) AND connection_direction = 1  ORDER BY _exclude_order /* "MEAS(' + meas_str + ')" */'
	i = 0
	for data_str in Query(query).Run():
		i+=1
	return i


def get_call_setup_rate(attempt, attempt_failure):
	if attempt == 0:
		return 0
	else:
		return round((attempt - attempt_failure)*100.0 / attempt,2)



def get_call_completion_rate(connected, disconnected):
	if connected == 0:
		return 0
	else:
		return round(disconnected*100.0 / connected, 2)



def get_call_dropped_rate(connected, dropped):
	if connected ==0:
		return 0
	else:
		return round(dropped*100.0/connected, 2)


def write_file(report):
	sorted_report = {k:report[k] for k in sorted(report)}
	with open(PATH, 'w') as f:
		for k in sorted(sorted_report):
			f.write((k + ':'))
			for kpi, value in sorted_report[k].items():
				f.write(kpi + '::' + str(value) + ';')
			f.write('\n')
			

def print_meas_in_log(meas_dict):
	for k in meas_dict.keys():
		Analyze.Log.Write('\n\n' + str(k) + ' : ' + str(meas_dict[k]))
		#Analyze.Log.Write('\n\n' + str(k))
		#for elem in meas_dict[k]:
		#	Analyze.Log.Write(elem)


def main():
	selected_measurements = Analyze.Workspace.GetSelectedMeasurements()
	if len(selected_measurements) > 0 :
		measurements_list = get_measurements_list(selected_measurements)
		group_by_num_dict = {'2G':[], 'CSFB':[], 'VoLTE':[]}
		for meas in measurements_list:
			if meas.endswith(':1'):
				group_by_num_dict['2G'].append(meas)
			
			if meas.endswith(':6'):
				group_by_num_dict['CSFB'].append(meas)
				
			if meas.endswith(':4') or meas.endswith(':5'):
				group_by_num_dict['VoLTE'].append(meas)
			

		for key in group_by_num_dict.keys():
			meas_str = get_meas_string_for_query(group_by_num_dict[key])
			group_by_num_dict.update({key:meas_str})
				
		# print_meas_in_log(group_by_num_dict)
		
		write_file(get_voice_quality_report(group_by_num_dict))		
		#write_file(get_voice_quality_report(meas_str))
		
	else:
		Analyze.Log.Write("Select measurements")

#main()