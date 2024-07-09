import pandas as pd


class TmdSearch:
    def __init__(self, cnv_header_data, cnv_body_data):
        self.pd_cnv_data = pd.DataFrame(columns=cnv_header_data.name_list, data=cnv_body_data.table_data)

    def search(self):
        tdm = (-0.002 * self.pd_cnv_data['depFM: Depth [fresh water, m]']) + 3.9667
        self.pd_cnv_data.insert(loc=11, column='Tdm', value=tdm)
        self.pd_cnv_data['Temperature < Tdm '] = (self.pd_cnv_data['t090C: Temperature [ITS-90, deg C]'] <
                                                  self.pd_cnv_data['Tdm'])
        score_tdm = self.pd_cnv_data['Temperature < Tdm '].value_counts()
        print(self.pd_cnv_data[['t090C: Temperature [ITS-90, deg C]', 'Tdm',
                                'Temperature < Tdm ']].head())
        print(score_tdm)
