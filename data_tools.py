import re
import pandas as pd


# Данный модуль отвечает за Tmd анализ cnv файла


class DataTools:
    @staticmethod
    def search_temperature_in_depth(dataframe, temperature_deg_c_index_column):
        # Данная функция принимает pandas.Dataframe и находит в нём
        dataframe.reset_index()
        tempreture = dataframe.iloc[0, temperature_deg_c_index_column]
        return tempreture

    @staticmethod
    def search_max_difference_tmd_temperature(dataframe, temperature_deg_c_index_column):
        data = dataframe.loc[dataframe['Temperature < Tmd']]
        if data.empty:
            result = 'None'
            return result
        result = data['Tmd'] - abs(data.iloc[:, temperature_deg_c_index_column])
        result = result.max()
        return result

    @staticmethod
    def data_clipping(cnv_body_data):
        data = pd.DataFrame(cnv_body_data.table_data).loc[:, 0]

        index_list = []

        dive_begin_index = 0
        max_depth = 0
        lift_begin_index = 0
        changing_values_range = 4   # start 0 value
        find_begin_dive = False

        for number, item in enumerate(data):
            if not find_begin_dive and number != 0 and data.loc[number - 1] >= item:
                dive_begin_index = number

            if (number - dive_begin_index) >= changing_values_range:
                find_begin_dive = True

            if item > max_depth:
                max_depth = item
                lift_begin_index = number

        index_list.append(dive_begin_index)
        index_list.append(lift_begin_index)

        cnv_body_data.table_data = cnv_body_data.table_data.loc[range(dive_begin_index, lift_begin_index + 1)]

        return cnv_body_data, index_list

    @staticmethod
    def log_error_flag_data(dataframe, depfm_index_column, temperature_deg_c_index_column):
        error = str()

        depth = dataframe.iloc[:, depfm_index_column]
        depth = depth.max()
        if depth > 1650:
            error = error + 'depth'
        tempreture = dataframe.iloc[:, temperature_deg_c_index_column]
        tempreture = tempreture.max()
        if tempreture >= 30:
            error = error + 'temperature'
        if error == str():
            error = 'not error'

        return error

    @staticmethod
    def tmd_analysis(cnv_header_data, cnv_body_data, index_list):  # придумать названия функции
        result_file = pd.DataFrame(columns=['Path', 'SBE_version', 'Start_Time', 'System_Upload_Date',
                                            'Date_from_the_Name_File', 'Latitude', 'Row_Latitude', 'Longitude',
                                            'Row_Longitude', 'Station', 'Station_From_Name', 'Max_Depth',
                                            'Surface_temperature', 'Max_difference_Tmd_Temperature', 'Unit_Temperature',
                                            'Count_True', 'Count_Total', 'Dive_Begin_Index',
                                            'Dive_End_Index', 'Error'])

        dataframe = cnv_body_data.table_data
        dataframe.columns = cnv_header_data.name_list

        depfm_index_column = int()
        temperature_deg_c_index_column = int()
        name_temperature_deg_c_index_column = str()

        for number, name_column in enumerate(cnv_header_data.name_list):
            regular = r'depFM:.+'
            match = re.search(regular, name_column)
            if match:
                depfm_index_column = number
            regular = r'.+(deg\sC).+'
            match = re.search(regular, name_column)
            if match:
                temperature_deg_c_index_column = number
                name_temperature_deg_c_index_column = match[0]

        tmd = (- 0.00000007610308758 * dataframe.iloc[:, depfm_index_column] ** 2
               - 0.0019619296 * dataframe.iloc[:, depfm_index_column] + 3.9646054)

        second_column = dataframe.columns.size
        dataframe.insert(loc=second_column, column='Tmd', value=tmd)
        dataframe.insert(loc=second_column + 1, column='Temperature < Tmd',
                         value=dataframe.iloc[:, temperature_deg_c_index_column] < dataframe.iloc[:, second_column])
        result_tdm = dataframe['Temperature < Tmd'].value_counts()  # return True or False

        # save Dataframe (development instrument)
        # dataframe.to_csv('result_tmd_search\\dataframe.csv', sep='\t', index=False)
        # print(dataframe)

        path = cnv_header_data.name_file_cnv
        sbe_version = cnv_header_data.sbe_version
        start_time = cnv_header_data.start_time if cnv_header_data.start_time else 'None'
        system_upload_date= cnv_header_data.system_upload_time if cnv_header_data.system_upload_time else 'None'
        latitude = cnv_header_data.latitude if cnv_header_data.latitude else 'None'
        row_latitude = cnv_header_data.row_latitude if cnv_header_data.latitude else 'None'
        longitude = cnv_header_data.longitude if cnv_header_data.longitude else 'None'
        row_longitude = cnv_header_data.row_longitude if cnv_header_data.longitude else 'None'
        station = cnv_header_data.station if cnv_header_data.station else 'None'
        max_depth = cnv_header_data.spans_list[0][1] if cnv_header_data.spans_list[0][1] else 'None'
        surface_temperature = DataTools.search_temperature_in_depth(dataframe, temperature_deg_c_index_column)
        max_tmd_vs_temperature = DataTools.search_max_difference_tmd_temperature(dataframe,
                                                                                 temperature_deg_c_index_column)
        station_name_file_cnv = cnv_header_data.station_name_file_cnv
        date_name_file_cnv = cnv_header_data.date_name_file_cnv

        total_number = dataframe.shape[0]
        true_number = total_number - result_tdm.iloc[0]
        dive_begin_index = index_list[0]
        lift_begin_index = index_list[1]
        error = DataTools.log_error_flag_data(dataframe, depfm_index_column, temperature_deg_c_index_column)
        name_temperature_deg_c_index_column = name_temperature_deg_c_index_column

        depth = dataframe.iloc[:, depfm_index_column].to_frame().T
        depth.insert(0, '0', cnv_header_data.name_file_cnv)
        temperature = dataframe.iloc[:, temperature_deg_c_index_column].to_frame().T
        temperature.insert(0, '0', cnv_header_data.name_file_cnv)
        depth.to_csv(f'result_tmd_search\\data.csv', sep='\t', header=False, mode='a', index=False)
        temperature.to_csv(f'result_tmd_search\\data.csv', sep='\t', header=False, mode='a', index=False)

        result_file.loc[0] = [path, sbe_version, start_time, system_upload_date, date_name_file_cnv, latitude,
                              row_latitude, longitude,
                              row_longitude, station, station_name_file_cnv, max_depth, surface_temperature,
                              max_tmd_vs_temperature, name_temperature_deg_c_index_column, true_number, total_number,
                              dive_begin_index,
                              lift_begin_index, error]

        return result_file
