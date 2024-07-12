import os


class SearchFiles:
    def __init__(self, path_to_direction, type_file):
        self.path_to_direction = path_to_direction
        self.type_file = type_file

    def search(self):
        result = []
        for root, dirs, files in os.walk(self.path_to_direction):
            for file in files:
                if file.endswith(self.type_file.lower()) or file.endswith(self.type_file.upper()):
                    result.append(os.path.join(root, file))

        return result
