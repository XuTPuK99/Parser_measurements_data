import pandas as pd


class TmdSearch:
    def __init__(self, cnv_header_data, cnv_body_data):
        self.pd_cnv_data = pd.DataFrame(columns=cnv_header_data.name_list, data=cnv_body_data.table_data)

    def search(self):
        k = -0.00000007610308758
        x = self.pd_cnv_data.iloc[:, 0] ** (2 - 0.0019619296) * self.pd_cnv_data.iloc[:, 0]
        b = 3.9667

        tdm = (k * x + b)

        second_column = self.pd_cnv_data.columns.size
        self.pd_cnv_data.insert(loc=second_column, column='Tdm', value=tdm)
        self.pd_cnv_data.insert(loc=second_column + 1, column='Temperature < Tdm',
                                value=self.pd_cnv_data.iloc[:, 2] < self.pd_cnv_data.iloc[:, second_column])
        value_counts = self.pd_cnv_data['Temperature < Tdm'].value_counts()

        return value_counts
