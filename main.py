from cnv_parser import CnvParser
from conf_parser import ConfParser
from exporter_to_json import ExportToJson
from tmd_searcher_in_file_cnv import TmdSearch
from searcher_files import SearchFiles

if __name__ == '__main__':
    searcher_files = SearchFiles('cnv', '.CNV')
    found_files = searcher_files.search()

    cnv_files = CnvParser(found_files)
    conf_files = ConfParser('config\\s80_230321v0134_O2OtObs!.con')

    cnv_header_data = cnv_files.header_parse()
    cnv_body_data = cnv_files.body_parse()

    conf_data = conf_files.conf_parse()

    tmd_search = TmdSearch(cnv_header_data, cnv_body_data)
    #tmd_search.search()

    #ExportToJson.export_to_json_cnv(cnv_body_data, 'result\\', 'result')
    #ExportToJson.export_to_json_conf(conf_data, 'result\\', 'result')
