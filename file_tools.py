import re
import os


class FileTools:
    @staticmethod
    def search(path_to_direction):
        result = []

        for root, dirs, files in os.walk(path_to_direction):
            regular = r'.+(C?c?nv).+'
            match = re.search(regular, root)
            if match:
                files = os.listdir(match[0])
                for file in files:
                    regular = r'.+\.(cnv)?(CNV)?'
                    match = re.search(regular, file)
                    if match:
                        result.append(f'{root}\\{file}')

            regular = r'.+(CNV).+'
            match = re.search(regular, root)
            if match:
                files = os.listdir(match[0])
                for file in files:
                    regular = r'.+\.(cnv)?(CNV)?'
                    match = re.search(regular, file)
                    if match:
                        result.append(f'{root}\\{file}')

        return result

    @staticmethod
    def open_files(path_file):
        with (open(path_file, 'r') as file):
            file_data = file.read()

        return file_data
