from cnv_parser import CnvParser
from conf_parser import ConfParser
from writer_files import WriteToFile
from tmd_searcher_in_file_cnv import TmdSearch
from searcher_files import SearchFiles

if __name__ == '__main__':
    searcher_files = SearchFiles('CTD_Data\\2019', '.CNV')
    found_files = searcher_files.search()

    cnv_files = CnvParser(found_files)
    conf_files = ConfParser('config\\s80_230321v0134_O2OtObs!.con')

    cnv_header_data = cnv_files.header_parse()
    cnv_body_data = cnv_files.body_parse(cnv_header_data)

    conf_data = conf_files.conf_parse()

    tmd_search = TmdSearch(cnv_header_data, cnv_body_data)

    WriteToFile.write_to_file_tmd_result(tmd_search.search(), 'result_tmd_search\\', 'result.txt')

    #WriteToFile.export_to_json_cnv(cnv_body_data, 'result\\', 'result')
    #WriteToFile.export_to_json_conf(conf_data, 'result\\', 'result')
