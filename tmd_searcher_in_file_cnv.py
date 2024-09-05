import pandas as pd


class TmdSearch:
    @staticmethod
    def search_temperature_2m(dataframe):
        target_value = int()
        closest_depth_2m = 2
        for number in range(dataframe.shape[0]):
            value_at_depth = dataframe.iloc[number, 0]
            closest_value = abs(2 - value_at_depth)
            if closest_value < closest_depth_2m:
                closest_depth_2m = float(closest_value)
                target_value = number
        result = dataframe.iloc[target_value, 2]
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
    def search(cnv_header_data, cnv_body_data):
        result_file = pd.DataFrame(columns=['Path', 'DateTime', 'Latitude', 'Longitude', 'Max_Depth',
                                            'Temperature(2m)', 'Max_difference_Tmd_Temperature',
                                            'Count_True', 'Count_Total'])

        dataframe = pd.DataFrame(columns=cnv_header_data.name_list, data=cnv_body_data.table_data)

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
        temperature_2m = TmdSearch.search_temperature_2m(dataframe)
        max_tmd_vs_temperature = TmdSearch.search_max_difference_tmd_temperature(dataframe)
        total_number = dataframe.shape[0]
        true_number = total_number - result_tdm.iloc[0]

        print(temperature_2m)

        #depth = dataframe.iloc[:, 0].to_frame().T
        #depth.to_csv(f'result_tmd_search\\depth.csv', sep='\t', mode='a', index=False)
        #print(type(depth))

        result_file.loc[0] = [path, datetime, latitude, longitude, max_depth, temperature_2m,
                              max_tmd_vs_temperature, total_number, true_number]

        return result_file
