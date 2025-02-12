import datetime
import time

from data_tools import DataTools
from file_tools import FileTools
from rinko_parser import RinkoParser
from writer_files import WriteToFile

if __name__ == "__main__":
    start = time.time()
    current_date = datetime.datetime.now()

    file_tools = FileTools()
    data_type = "csv"
    found_files = file_tools.search_files(
        file_extension=data_type, path_to_direction="test_csvdata"
    )  # 'rinko' or 'test_rinko'

    for file in found_files:
        start_cycle = time.time()

        data = file_tools.open_file(file)

        try:
            rinko_header_data, rinko_body_data = RinkoParser.parse(file, data)
            rinko_header_data.name_file_csv = file

            rinko_body_data, index_list = DataTools.data_clipping(
                data_type, rinko_body_data
            )

            if rinko_body_data.table_data.empty is True:
                continue

            result_search = DataTools.tmd_analysis(
                data_type, rinko_header_data, rinko_body_data, index_list
            )

            WriteToFile.write_to_file_tmd_result(
                data_type, result_search, "result_tmd_search\\", "result.csv"
            )

        except Exception as e:
            log_text = f"Error file: {file}; {type(e)}, {e}"
            print(log_text)
            WriteToFile.write_logs_file(current_date, log_text)
            continue

        end_cycle = time.time() - start_cycle

        print(file, "Cycle running time:", end_cycle)

    end = time.time() - start

    print("Program running time:", end)
