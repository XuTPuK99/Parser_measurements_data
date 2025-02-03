import os
import re

# В данном модуле записаные функции для работы с файлами


class FileTools:
    @staticmethod
    def search_files(file_extension, path_to_direction):
        # Функция ищет все директории в указаной папке с cnv в названии
        # и возвращает список этих файлов
        result = []

        for root, _, files in os.walk(path_to_direction):
            regular = rf".*({file_extension}).*"
            match = re.search(regular, root, flags=re.I)
            if match:
                files = os.listdir(match[0])
                for file in files:
                    regular = rf".+\.{file_extension}"
                    match = re.search(regular, file, flags=re.I)
                    if match:
                        result.append(f"{root}\\{file}")

        return result

    @staticmethod
    def open_file(path_file):
        # Функция считывает данные из файла и возвращает их в виде str()
        with open(path_file, "r") as file:
            return file.read()
