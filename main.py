import config_parser
from cnv_parser import CnvParser
from config_parser import ConfigParser
from export_to_json import ExportToJson

if __name__ == '__main__':
    cnv_data = CnvParser('cnv\\PESCH080.CNV')
    conf_data = ConfigParser('config\\s80_230321v0134_O2OtObs!.con')

    cnv_header_data = cnv_data.header_parse()
    cnv_body_data = cnv_data.body_parse()
    conf_body_data = conf_data.config_parse()

    export_to_json = ExportToJson.export_to_json(conf_body_data, 'D:\\work\\python\\Hydrophysic_works'
                                                              '\\Parser_measurements_data\\', 'result')
