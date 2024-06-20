from cnv_parser import CnvParser

from export_to_json import ExportToJson

if __name__ == '__main__':
    cnv_data = CnvParser('cnv\\PESCH080.CNV')

    header_data = cnv_data.header_parse()
    body_data = cnv_data.body_parse()

    export_to_json = ExportToJson.export_to_json(header_data, 'D:\\work\\python\\Hydrophysic_works'
                                                              '\\Parser_measurements_data\\', 'result')
