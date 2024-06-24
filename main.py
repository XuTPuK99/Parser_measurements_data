import config_parser
from cnv_parser import CnvParser
from config_parser import LaunchFabric
from export_to_json import ExportToJson

if __name__ == '__main__':
    cnv_data = CnvParser('cnv\\PESCH080.CNV')
    conf_data = LaunchFabric('config\\s80_230321v0134_O2OtObs!.con')

    cnv_header_data = cnv_data.header_parse()
    cnv_body_data = cnv_data.body_parse()
