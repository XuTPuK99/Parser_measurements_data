import pandas as pd


class TmdSearch:
    def __init__(self, cnv_header_data, cnv_body_data):
        self.cnv_header_data = cnv_header_data

        self.list_pd_cnv_data = []
        for number in range(len(cnv_header_data)):
            self.pd_cnv_data = pd.DataFrame(columns=cnv_header_data[number].name_list,
                                            data=cnv_body_data[number].table_data)
            self.list_pd_cnv_data.append(self.pd_cnv_data)

    def search(self):
        result = []

        for number, dataframe in enumerate(self.list_pd_cnv_data):

            k = -0.00000007610308758
            x = dataframe.iloc[:, 0] ** (2 - 0.0019619296) * dataframe.iloc[:, 0]
            b = 3.9667

            tdm = (k * x + b)

            second_column = dataframe.columns.size
            dataframe.insert(loc=second_column, column='Tdm', value=tdm)
            dataframe.insert(loc=second_column + 1, column='Temperature < Tdm',
                             value=dataframe.iloc[:, 2] < dataframe.iloc[:, second_column])
            table_result = dataframe['Temperature < Tdm'].value_counts()
            table_result = table_result.rename(self.cnv_header_data[number].name_file_cnv)
            result.append(table_result)

        return result
