from cnv_parser import CnvParser
from conf_parser import ConfParser
from export_to_json import ExportToJson
from tmd_search import TmdSearch

if __name__ == '__main__':
    cnv_file = CnvParser('cnv\\mLT0530.cnv')   #  'cnv\\mLTpup0729.cnv'
    conf_file = ConfParser('config\\s80_230321v0134_O2OtObs!.con')

    cnv_header_data = cnv_file.header_parse()
    cnv_body_data = cnv_file.body_parse()

    conf_data = conf_file.conf_parse()
    print(len(cnv_header_data.name_list))
    print(len(cnv_body_data.table_data[0]))
    print(cnv_body_data.table_data[1])

    #tmd_search = TmdSearch(cnv_header_data, cnv_body_data)
    #tmd_search.search()

    #ExportToJson.export_to_json_cnv(cnv_body_data, 'result\\', 'result')
    #ExportToJson.export_to_json_conf(conf_data, 'result\\', 'result')
