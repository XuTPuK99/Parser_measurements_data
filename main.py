from cnv_parser import CnvParser
from conf_parser import ConfParser
from writer_files import WriteToFile
from data_tools import DataTools
from file_tools import FileTools

if __name__ == '__main__':
    file_tools = FileTools()
    found_files = file_tools.search_files('CTD_Data\\test_cnvdata')  # 'CTD_Data\\test_cnvdata'

    for file in found_files:
        print(file)
        data = file_tools.open_files(file)

        cnv_header_data, cnv_body_data = CnvParser.parse(data)
        cnv_header_data.name_file_cnv = file

        cnv_body_data = DataTools.data_clipping(cnv_body_data)

        # conf_data = ConfParser.conf_parse(cnv_header_data.conf_file) # path: config\\*.con
        result_search = DataTools.search(cnv_header_data, cnv_body_data)

        WriteToFile.write_to_file_tmd_result(result_search, 'result_tmd_search\\', 'result_2022.csv')

    #WriteToFile.write_to_file_tmd_result(result_search['result_data'], 'result_tmd_search\\',
    #                                     'row_data_result_2022.csv')

    # WriteToFile.export_to_json_cnv(cnv_body_data, 'result\\', 'result')
    # WriteToFile.export_to_json_conf(conf_data, 'result\\', 'result')
