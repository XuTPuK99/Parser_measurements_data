import pandas as pd


class TmdSearch:
    def __init__(self, cnv_header_data, cnv_body_data):
        self.cnv_header_data = cnv_header_data

        self.list_pd_cnv_data = []

        for number in range(len(cnv_header_data)):
            print(self.cnv_header_data[number].name_file_cnv, 'Search')
            #print('count name_list:', len(cnv_header_data[number].name_list))
            #print('count column:', len(cnv_body_data[number].table_data[0]))
            self.pd_cnv_data = pd.DataFrame(columns=cnv_header_data[number].name_list,
                                            data=cnv_body_data[number].table_data)
            self.list_pd_cnv_data.append(self.pd_cnv_data)

    def search(self):
        result = pd.DataFrame(columns=['Path', 'Count_True', 'Count_Total'])

        for number, dataframe in enumerate(self.list_pd_cnv_data):

            k = -0.00000007610308758
            x = dataframe.iloc[:, 0] ** (2 - 0.0019619296) * dataframe.iloc[:, 0]
            b = 3.9667

            tdm = (k * x + b)

            second_column = dataframe.columns.size
            dataframe.insert(loc=second_column, column='Tdm', value=tdm)
            dataframe.insert(loc=second_column + 1, column='Temperature < Tdm',
                             value=dataframe.iloc[:, 2] < dataframe.iloc[:, second_column])
            result_tdm = dataframe['Temperature < Tdm'].value_counts()

            total_number = dataframe.shape[0]
            true_number = total_number - result_tdm.iloc[0]

            row = pd.DataFrame([{'Path': self.cnv_header_data[number].name_file_cnv,
                               'Count_True': true_number, 'Count_Total': total_number}])
            result = pd.concat([result, row])

        return result
