from cnv_parser import CnvParser
from config_parser import ConfParser
from export_to_json import ExportToJson

if __name__ == '__main__':
    cnv_file = CnvParser('cnv\\mLTpup0729.cnv')
    conf_file = ConfParser('config\\Se060828.con')

    cnv_header_data = cnv_file.header_parse()
    cnv_body_data = cnv_file.body_parse()

    conf_data = conf_file.conf_parse()

    ExportToJson.export_to_json_conf(conf_data, 'result\\', 'result')
