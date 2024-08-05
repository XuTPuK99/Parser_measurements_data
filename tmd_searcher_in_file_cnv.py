import pandas as pd


class TmdSearch:
    def __init__(self, cnv_header_data, cnv_body_data):
        self.cnv_header_data = cnv_header_data

        self.list_pd_cnv_data = []

        for number in range(len(cnv_header_data)):
            print(self.cnv_header_data[number].name_file_cnv, 'Search')

            self.pd_cnv_data = pd.DataFrame(columns=cnv_header_data[number].name_list,
                                            data=cnv_body_data[number].table_data)
            self.list_pd_cnv_data.append(self.pd_cnv_data)

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
        data = dataframe.loc[(dataframe['Temperature < Tmd'] == True)]
        result = data.iloc[:, 2].min()
        return result

    def search(self):   #Метод возвращает словарь {} с двумя массивами
        result_file = pd.DataFrame(columns=['Path', 'DateTime', 'Latitude', 'Longitude', 'Max_Depth',
                                            'Temperature(2m)', 'Max_difference_Tmd_Temperature',
                                            'Count_True', 'Count_Total'])

        for number, dataframe in enumerate(self.list_pd_cnv_data):

            tmd = -0.00000007610308758 * dataframe.iloc[:, 0] ** 2 - 0.0019619296 * dataframe.iloc[:, 0] + 3.9667

            second_column = dataframe.columns.size
            dataframe.insert(loc=second_column, column='Tmd', value=tmd)
            dataframe.insert(loc=second_column + 1, column='Temperature < Tmd',
                             value=dataframe.iloc[:, 2] < dataframe.iloc[:, second_column])
            result_tdm = dataframe['Temperature < Tmd'].value_counts()  # return True or False

            print(self.cnv_header_data[number].name_file_cnv)
            #dataframe.to_csv(f'result_tmd_search\\dataframe.csv', sep='\t', index=True)

            path = self.cnv_header_data[number].name_file_cnv
            datetime = self.cnv_header_data[number].start_time if self.cnv_header_data[number].start_time else 'None'
            latitude = self.cnv_header_data[number].latitude if self.cnv_header_data[number].latitude else 'None'
            longitude = self.cnv_header_data[number].longitude if self.cnv_header_data[number].longitude else 'None'
            max_depth = self.cnv_header_data[number].spans_list[0][1] if self.cnv_header_data[number].spans_list[0][1] else 'None'
            temperature_2m = self.search_temperature_2m(dataframe)
            max_tmd_vs_temperature = self.search_max_difference_tmd_temperature(dataframe)
            total_number = dataframe.shape[0]
            true_number = total_number - result_tdm.iloc[0]

            #depth = dataframe.iloc[:, 0].to_frame().T
            #depth.to_csv(f'result_tmd_search\\depth.csv', sep='\t', mode='a', index=False)
            #print(type(depth))

            row_file = pd.DataFrame([{'Path': path, 'DateTime': datetime, 'Latitude': latitude, 'Longitude': longitude,
                                      'Max_Depth': max_depth, 'Temperature(2m)': temperature_2m,
                                      'Max_difference_Tmd_Temperature': max_tmd_vs_temperature,
                                      'Count_True': true_number, 'Count_Total': total_number}])

            result_file = pd.concat([result_file, row_file], ignore_index=True)

        result = {'result_file': result_file}

        return result
