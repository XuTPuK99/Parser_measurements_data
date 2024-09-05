import os
import pandas as pd


class WriteToFile:
    @staticmethod
    def export_to_json_cnv(cnv_data, file_path, name_file):
        file_json = cnv_data.model_dump_json(indent=2)
        with (open(f'{file_path}{name_file}.JSON', 'w') as file):
            file.write(file_json)

    @staticmethod
    def export_to_json_conf(conf_data, file_path, name_file):
        file_json = conf_data.model_dump_json(indent=2)
        with (open(f'{file_path}{name_file}.JSON', 'w') as file):
            file.write(file_json)

    @staticmethod
    def write_to_file_tmd_result(result_tmd_data, file_path, name_file):
        file_path = f'{file_path}{name_file}'
        if not os.path.exists(file_path):
            result_file = pd.DataFrame(columns=['Path', 'DateTime', 'Latitude', 'Longitude', 'Max_Depth',
                                                'Temperature(2m)', 'Max_difference_Tmd_Temperature',
                                                'Count_True', 'Count_Total'])
            result_file.to_csv(file_path, sep='\t', index=False)
        result_tmd_data.to_csv(file_path, sep='\t', header=False, index=False, mode='a')
