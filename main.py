from cnv_parser import CnvParser
from conf_parser import ConfParser
from writer_files import WriteToFile
from tmd_searcher_in_file_cnv import TmdSearch
from file_tools import FileTools

if __name__ == '__main__':
    file_tools = FileTools()
    found_files = file_tools.search('CTD_Data')
    #'CTD_Data\\2023\\07_Ver\\sbe25\\cnvdata\\du\\test'

    #conf_parser = ConfParser('config\\s80_230321v0134_O2OtObs!.con')

    for file in found_files:
        print(file)
        data = file_tools.open_files(file)

        cnv_header_data, cnv_body_data = CnvParser.parse(data)
        cnv_header_data.name_file_cnv = file

        #conf_data = conf_parser.conf_parse()
        result_search = TmdSearch.search(cnv_header_data, cnv_body_data)

        WriteToFile.write_to_file_tmd_result(result_search, 'result_tmd_search\\', 'result_2022.csv')



    #WriteToFile.write_to_file_tmd_result(result_search['result_data'], 'result_tmd_search\\',
    #                                     'row_data_result_2022.csv')

    #WriteToFile.export_to_json_cnv(cnv_body_data, 'result\\', 'result')
    #WriteToFile.export_to_json_conf(conf_data, 'result\\', 'result')
