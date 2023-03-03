import Analyze
from Analyze import Query
import sys
sys.path.append('C:\\Nemo Tools\\Nemo Analyze\\Macros\\V2.0') 	# path with macros

from pictures import get_floor

''' WORK PROPERLY BUT NOT OPTIMIZED '''
'''	NEED RE-WRITE '''

#get one str
def get_meas_string_for_query(measurements_list):
	if len(measurements_list) > 0:
		meas_str = rename_for_query(measurements_list[0])
		for i in range(1, len(measurements_list)):
			meas_str += "|" + rename_for_query(measurements_list[i])
		return meas_str
	else:
		return None
		
		
def rename_for_query(measurement):
	name = measurement.FullName			
	for letter in name:  			
	    if letter == '.':
	        name = name.replace(letter, ":")
	# return meas.HintTitle
	return name


# get data for all selected measurements 
def Collector_PCI_Channel():
    Selected_meas_data = {}  # dict [measurement_name] = [data(PCI, Channel)]
    Selected_meas_data_1 = {}
    all_measurements = Analyze.Workspace.GetSelectedMeasurements()  # selected measurement list
    measurements = []
    for meas in all_measurements:
        if meas.FullName.endswith('.3'):
            measurements.append(meas)
            
    meas = get_meas_string_for_query(measurements)
    measurements = []
    measurements.append(meas)

    for meas in sorted(measurements):
        PCI_channel_data = {}  # dict [PCI] = [Channel]
        name = meas  # full meas name

        Query_name_0 = 'SELECT  "channel_number","lte_physical_layer_cell_id","lte_received_power",OID_SHORT("the_parent") AS "the_parent" FROM "Nemo.LTE.CELLMEAS"."Cell+" x WHERE "lte_cell_type"=0  /* "MEAS(' + str(
            name) + ')" */'  # text SQL query
        Query_name_1 = 'SELECT  "channel_number","lte_physical_layer_cell_id","lte_received_power",OID_SHORT("the_parent") AS "the_parent" FROM "Nemo.LTE.CELLMEAS"."Cell+" x WHERE "lte_cell_type"=2  /* "MEAS(' + str(
            name) + ')" */'

        detected_pci_file = Query(Query_name_1)
        primary_pci_file = Query(Query_name_1)

        # Primary PCI
        ''' put in a separate function '''
        for data_str in primary_pci_file.Run():  # writing data in dict
        	if int(data_str[2]) > -110:
        		if data_str[1] in PCI_channel_data and data_str[0] != PCI_channel_data.get(data_str[1]): 
        			PCI_channel_data[int(data_str[1]) + 1080] = data_str[0]  # if PCI with other channel in dict: plus 1080 ( 3*6*30)
        		else:
        			PCI_channel_data[int(data_str[1])] = int(data_str[0])

            # Analyze.Log.Write(PCI_channel_data)	 		# debug PCI:{Channel}

        Selected_meas_data[name] = PCI_channel_data

        # Detected PCI
        ''' working like primary '''
        for data_str in detected_pci_file.Run():
        	if int(data_str[2]) > -110:
        		if data_str[1] in PCI_channel_data and data_str[0] != PCI_channel_data.get(data_str[1]):
        			PCI_channel_data[int(data_str[1]) + 1080] = data_str[0]
        		else:
        			PCI_channel_data[int(data_str[1])] = int(data_str[0])

        # Analyze.Log.Write(PCI_channel_data)	 #debug PCI:{Channel}

        Selected_meas_data_1[name] = PCI_channel_data

        x = Selected_meas_data.update(Selected_meas_data_1)

    return Selected_meas_data  # dict [measurement_name] = [data(PCI, channel)]



#from data generate response with crossmod pci/channel

def Result_PCI(data, Mod):
	Full_PCI_List = []
	full_response = []
	i = 0
	
	for PCI_1 in data:
		
		#Analyze.Log.Write(PCI_1)
		Mod_list = []
		if PCI_1 > 1000:
				PCI_1 -= 1080
				
		for PCI_2 in data:
			if PCI_1 == PCI_2:
				#Analyze.Log.Write(PCI_1%Mod) # debug
				#Analyze.Log.Write(PCI_2%Mod) #	debug
				continue
				
			elif PCI_1%Mod == PCI_2%Mod and data.get(PCI_1) == data.get(PCI_2): # if cross mod and channels equal
				
				#Analyze.Log.Write(Mod_list) # debug
				if PCI_2 > 1000:			 # if PCI_2 recurring ( >=2 in 1 dict)
					Mod_list.append(PCI_2-1080)
				else:
					Mod_list.append(PCI_2)
				Full_PCI_List.append(PCI_2)	# add viewed PCI in list to prevent duplication
				
				
		if len(Mod_list) < 1 or (PCI_1 in Full_PCI_List):	# if in cross mod list no elements or  PCI in duplication list
			pass
		else:
			answer = 'Ch = ' + str(data.get(PCI_1)) + ', PCI = ' + str(PCI_1) + ' - ' + str(Mod_list) + ';\n'	# output sting 
			if answer in full_response:
				pass
			else:
				full_response.append(answer) #list of sttings ALL crossed PCI 
	return full_response
			
		
		
		
def main():
	Analyze.Log.Write('Crossmod started work')
	ready_data = Collector_PCI_Channel()

	# Analyze.Log.Write(ready_data) # debug
	Mod_List = [30, 6]				# mod list 3/6/30
	
	path = 'C:/RC_data/crossmod.txt'
	file = open(path, 'w')
	
	for data in ready_data:
	
		floor = get_floor(str(data))
		#Analyze.Log.Write(ready_data.get(data))
		flag = 0
		
		for mod in Mod_List:
			
			result = Result_PCI(ready_data.get(data), mod)
			
			if result != [] :
				if flag != 1:
					#floor_text = '\n' + str(floor) + ':\n'  
					#file.write(floor_text)
				#	Analyze.Log.Write(floor_text)
					flag = 1
					
				mod1_text = 'Mod = ' + str(mod) + '\n'
				file.write(mod1_text)
				#Analyze.Log.Write(mod1_text)
			
			#file.write(str(result))
			for elem in result:
				file.write(elem)
				#Analyze.Log.Write(elem)
	file.close()
	Analyze.Log.Write('Crossmod finished work')

#main()
