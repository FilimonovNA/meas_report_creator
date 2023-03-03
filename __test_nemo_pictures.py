def get_slave_number(meas):
    '''return number of slave (1, 2, 3, 4, 5, 6, 11)'''
    if meas.FullName[-2] == '.':
        return meas.FullName[-1:]
    else:
        return meas.FullName[-2:]



def main():
    measurements = Analyze.Workspace.GetSelectedMeasurements()  # get selected meas list
    all_meas_dict = {}
    for meas in measurements:  # number of slave (1, 2, 3, 5, 7, 11)

        slave_number = get_slave_number(meas)
        floor_list = []
        current_floor = get_floor(meas.FullName)

        if slave_number not in all_meas_dict.keys():
            all_meas_dict[slave_number] = []
        elif  slave_number in all_meas_dict.keys() and \
                current_floor not in all_meas_dict.get(slave_number):
            all_meas_dict.get(slave_number).append(current_floor)
        else:
            all_meas_dict.get(slave_number).append(current_floor + '.')

        if current_floor in floor_list:
            current_floor += '.' + i
            i += 1
        #
        # if current_floor not in ['Out', 'Undefined']:
        #     current_floor = current_floor + 'fl'

        if slave_number in workbook_dict:
            for workbook_str in workbook_dict.get(slave_number):

                Analyze.Log.Write(current_floor)

                if current_floor == 'out':
                    name_workbook = 'rg-outdoor-' + workbook_str
                else:
                    name_workbook = 'rg-indoor-' + workbook_str

                newWorkbook = Analyze.Workspace.OpenWorkbook(name_workbook,
                                                             meas)  # open 1 workbook and later save it in picture
                workbookpage = newWorkbook.CurrentPage
                crutch_1 = Analyze.Workspace.OpenWorkbook('crutch', meas)  # crutch for nemo)

                counter = 0
                for elem in workbookpage.Views:
                    counter += 1
                    if type(elem) is Analyze.MapDataView:  # zoom map to best fit

                        Analyze.Log.Write(elem.MapType())  # debug
                        Analyze.Log.Write(type(elem))  # debug
                    # elem.BestFitZoom()
                Analyze.Log.Write(str(counter))

                name = 'C:\\RG_data\\{0}_{1}_{2}.png'.format(current_floor, picture_dict[workbook_str], workbook_str)
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
    Analyze.Windows.MessageBox('Data from Nemo Analyze is ready. \nYou can start generating a report',
                                        'SUCCESS', "ok")
    Analyze.Log.Write('Pictures are Ready')