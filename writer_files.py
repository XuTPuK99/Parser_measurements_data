import os
import pandas as pd

# Данный модуль отвечает запись данных в файл


class WriteToFile:
    @staticmethod
    def export_to_json_cnv(cnv_data, file_path, name_file):
        # Запись данных .cnv (header или body) в JSON файл
        file_json = cnv_data.model_dump_json(indent=2)
        with (open(f'{file_path}{name_file}.JSON', 'w') as file):
            file.write(file_json)

    @staticmethod
    def export_to_json_conf(conf_data, file_path, name_file):
        # Запись данных .conf в JSON файл
        file_json = conf_data.model_dump_json(indent=2)
        with (open(f'{file_path}{name_file}.JSON', 'w') as file):
            file.write(file_json)

    @staticmethod
    def write_to_file_tmd_result(result_tmd_data, file_path, name_file):
        # Запись результатов tmd анализа в файл .csv
        # Результаты дописываются в готовый файл, если файл не существует то создаётся новый
        file_path = f'{file_path}{name_file}'
        if not os.path.exists(file_path):
            result_file = pd.DataFrame(columns=['Path', 'SBE_version', 'Start_Time', 'System_Upload_Date', 'Latitude', 'Row_Latitude',
                                                'Longitude', 'Row_Longitude',
                                                'Station', 'Max_Depth', 'Surface_temperature',
                                                'Max_difference_Tmd_Temperature', 'Unit_Temperature',
                                                'Count_True', 'Count_Total', 'Dive_Begin_Index',
                                                'Dive_End_Index', 'Error'])
            result_file.to_csv(file_path, sep='\t', index=False)
        result_tmd_data.to_csv(file_path, sep='\t', header=False, index=False, mode='a')
