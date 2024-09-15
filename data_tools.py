import numpy as np
import pandas as pd


class DataTools:
    @staticmethod
    def search_temperature_in_depth(dataframe):
        depth = 2
        index_value = 0
        minimal_difference = depth
        for number in range(dataframe.shape[0]):
            value = dataframe.iloc[number, 0]
            difference = abs(depth - value)
            if difference < minimal_difference:
                minimal_difference = float(difference)
                index_value = number
        result = dataframe.iloc[index_value, 2]
        if result == np.nan:
            result = 'None'
        return result

    @staticmethod
    def search_max_difference_tmd_temperature(dataframe):
        data = dataframe.loc[dataframe['Temperature < Tmd']]
        if data.empty:
            result = 'None'
            return result
        result = data['Tmd'] - abs(data.iloc[:, 2])
        result = result.max()
        return result

    @staticmethod
    def search(cnv_header_data, cnv_body_data):  # придумать названия функции
        result_file = pd.DataFrame(columns=['Path', 'DateTime', 'Latitude', 'Longitude', 'Max_Depth',
                                            'Temperature(2m)', 'Max_difference_Tmd_Temperature',
                                            'Count_True', 'Count_Total'])

        dataframe = cnv_body_data.table_data
        dataframe.columns = cnv_header_data.name_list

        tmd = (-0.00000007610308758 * dataframe.iloc[:, 0] ** 2
               - 0.0019619296 * dataframe.iloc[:, 0] + 3.9667)

        second_column = dataframe.columns.size
        dataframe.insert(loc=second_column, column='Tmd', value=tmd)
        dataframe.insert(loc=second_column + 1, column='Temperature < Tmd',
                         value=dataframe.iloc[:, 2] < dataframe.iloc[:, second_column])
        result_tdm = dataframe['Temperature < Tmd'].value_counts()  # return True or False

        path = cnv_header_data.name_file_cnv
        datetime = cnv_header_data.start_time if cnv_header_data.start_time else 'None'
        latitude = cnv_header_data.latitude if cnv_header_data.latitude else 'None'
        longitude = cnv_header_data.longitude if cnv_header_data.longitude else 'None'
        max_depth = cnv_header_data.spans_list[0][1] if cnv_header_data.spans_list[0][1] else 'None'
        temperature_2m = DataTools.search_temperature_in_depth(dataframe)
        max_tmd_vs_temperature = DataTools.search_max_difference_tmd_temperature(dataframe)
        total_number = dataframe.shape[0]
        true_number = total_number - result_tdm.iloc[0]

        depth = dataframe.iloc[:, 0].to_frame().T
        depth.insert(0, '0', cnv_header_data.name_file_cnv)
        temperature = dataframe.iloc[:, 2].to_frame().T
        temperature.insert(0, '0', cnv_header_data.name_file_cnv)
        depth.to_csv(f'result_tmd_search\\data.csv', sep='\t', header=False, mode='a', index=False)
        temperature.to_csv(f'result_tmd_search\\data.csv', sep='\t', header=False, mode='a', index=False)

        result_file.loc[0] = [path, datetime, latitude, longitude, max_depth, temperature_2m,
                              max_tmd_vs_temperature, true_number, total_number]

        return result_file

    @staticmethod
    def data_clipping(cnv_body_data):
        data = pd.DataFrame(cnv_body_data.table_data).loc[:, 0]

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

        cnv_body_data.table_data = cnv_body_data.table_data.loc[range(dive_begin_index, lift_begin_index + 1)]

        return cnv_body_data
