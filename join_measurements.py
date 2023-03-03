import Analyze

def get_measurements_list(selected_meas):

	meas_for_query_list = []
	for i in range(len(selected_meas)):
		measurement = selected_meas[i]
		measurement = rename_for_query(measurement)
		meas_for_query_list.append(measurement)
	return meas_for_query_list #sorted(meas_for_query_list)
	
def get_meas_str(measurements_list):
	meas_str += measurements_list[0]
	for i in range(1, len(measurements_list)-1):
		meas_str += '|' + measurements_list[i] 
	return meas_str 
		
	

def main():
	selected_meas = Analyze.Workspace.GetSelectedMeasurements()
	if len(selected_meas) > 0:
		measurements_list = get_measurements_list(selected_meas)
		meas_str = get_meas_str(measurements_list)
		
		
	else:
		Analyze.Log.Write('Select Measurements')