import time
import datetime

from cnv_parser import CnvParser
from conf_parser import ConfParser
from writer_files import WriteToFile
from data_tools import DataTools
from file_tools import FileTools

if __name__ == '__main__':
    start = time.time()
    current_date = datetime.datetime.now()

    file_tools = FileTools()
    found_files = file_tools.search_files('CTD_Data')  # 'ctddata' or 'CTD Data' or
    # 'test_cnv_data\\cnv'

    for file in found_files:
        start_cycle = time.time()

        data = file_tools.open_file(file)

        try:
            cnv_header_data, cnv_body_data = CnvParser.parse(file, data)
            cnv_header_data.name_file_cnv = file

            cnv_body_data, index_list = DataTools.data_clipping(cnv_body_data)

            if cnv_body_data.table_data.empty is True:
                continue

            # conf_data = ConfParser.conf_parse(cnv_header_data.conf_file) # path: config\\*.con
            result_search = DataTools.tmd_analysis(cnv_header_data, cnv_body_data, index_list)

            # WriteToFile.export_to_json_conf(conf_data, 'result\\', 'result_conf') #
            WriteToFile.write_to_file_tmd_result(result_search, 'result_tmd_search\\', 'result.csv')

        except Exception as e:
            log_text = f'Error file: {file}; {type(e)}, {e}'
            print(log_text)
            WriteToFile.write_logs_file(current_date, log_text)
            continue

        end_cycle = time.time() - start_cycle

        print(file, 'Cycle running time:', end_cycle)

    end = time.time() - start

    print('Program running time:', end)
