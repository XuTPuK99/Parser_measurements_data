class ExportToJson:
    @staticmethod
    def export_to_json_cnv(cnv_data, file_path, name_file):
        file_json = cnv_data.model_dump_json(indent=2)
        with (open(f'{file_path}{name_file}.JSON', 'w') as file):
            file.write(file_json)

    @staticmethod
    def export_to_json_conf(conf_data, file_path, name_file):
        file_json = conf_data.model_dump_json(indent=2)
        with (open(f'{file_path}{name_file}.JSON', 'w') as file):
            file.write(file_json)
