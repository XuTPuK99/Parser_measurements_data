import re

import pandas as pd

# Данный модуль отвечает за Tmd анализ cnv файла


class DataTools:
    @staticmethod
    def search_temperature_in_depth(
        data_type, dataframe, temperature_deg_c_index_column=None
    ):  # surface_temperature
        # Данная функция принимает pandas.Dataframe и находит в нём

        if data_type == "cnv":
            dataframe.reset_index()
            tempreture = dataframe.iloc[0, temperature_deg_c_index_column]
            return tempreture
        if data_type == "csv":
            tempreture = dataframe.reset_index()
            tempreture = tempreture["Temp. [degC]"][0]
            return tempreture
        return None

    @staticmethod
    def search_max_difference_tmd_temperature(
        data_type, dataframe, temperature_deg_c_index_column=None
    ):
        if data_type == "cnv":
            data = dataframe.loc[dataframe["Temperature < Tmd"]]
            if data.empty:
                result = "None"
                return result
            result = data["Tmd"] - abs(data.iloc[:, temperature_deg_c_index_column])
            result = result.max()
            return result
        if data_type == "csv":
            data = dataframe.loc[dataframe["Temperature < Tmd"]]
            if data.empty:
                result = "None"
                return result
            result = data["Tmd"] - abs(data["Temp. [degC]"])
            result = result.max()
            return result
        return None

    @staticmethod
    def data_clipping(data_type, body_data):
        if data_type == "cnv":
            data = pd.DataFrame(body_data.table_data).loc[:, 0]
        if data_type == "csv":
            data = pd.DataFrame(body_data.table_data)["Depth [m]"]

        index_list = []

        dive_begin_index = 0
        max_depth = 0
        lift_begin_index = 0

        changing_values_range = 4  # start 0 value
        find_begin_dive = False

        for number, item in enumerate(data):
            if item == 0 and number <= len(data) / 2:
                find_begin_dive = False

            if (
                not find_begin_dive
                and number != 0
                and (data.loc[number - 1] >= item or data.loc[number - 1] == 0)
            ):
                dive_begin_index = number

            if (number - dive_begin_index) >= changing_values_range:
                find_begin_dive = True

            if float(item) > float(max_depth):
                max_depth = item
                lift_begin_index = number

        index_list.append(dive_begin_index)
        index_list.append(lift_begin_index)

        body_data.table_data = body_data.table_data.loc[
            range(dive_begin_index, lift_begin_index + 1)
        ]

        return body_data, index_list

    @staticmethod
    def log_error_flag_data(
        data_type,
        dataframe,
        depfm_index_column=None,
        temperature_deg_c_index_column=None,
    ):
        error = str()

        if data_type == "cnv":
            depth = dataframe.iloc[:, depfm_index_column]
            tempreture = dataframe.iloc[:, temperature_deg_c_index_column]
        if data_type == "csv":
            depth = dataframe["Depth [m]"]
            tempreture = dataframe["Temp. [degC]"]

        depth = depth.max()
        if depth > 1650:
            error = error + "depth"
        tempreture = tempreture.max()
        if tempreture >= 30:
            error = error + "temperature"
        if error == str():
            error = "not error"

        return error

    @staticmethod
    def tmd_analysis(data_type, header_data, body_data, index_list):
        if data_type == "cnv":
            return DataTools.tmd_analysis_cnv(
                data_type, header_data, body_data, index_list
            )
        if data_type == "csv":
            return DataTools.tmd_analysis_csv(
                data_type, header_data, body_data, index_list
            )
        return None

    @staticmethod
    def tmd_analysis_cnv(
        data_type, cnv_header_data, cnv_body_data, index_list
    ):  # придумать названия функции
        result_file = pd.DataFrame(
            columns=[
                "Path",
                "SBE_version",
                "Start_Time",
                "System_Upload_Date",
                "Date_from_the_Name_File",
                "Latitude",
                "Row_Latitude",
                "Longitude",
                "Row_Longitude",
                "Station",
                "Station_From_Name",
                "Max_Depth",
                "Surface_temperature",
                "Max_difference_Tmd_Temperature",
                "Unit_Temperature",
                "Count_True",
                "Count_Total",
                "Dive_Begin_Index",
                "Dive_End_Index",
                "Error",
            ]
        )
        dataframe = cnv_body_data.table_data
        dataframe.columns = cnv_header_data.name_list

        depfm_index_column = int()
        temperature_deg_c_index_column = int()
        name_temperature_deg_c_index_column = str()

        for number, name_column in enumerate(cnv_header_data.name_list):
            regular = r"depFM:.+"
            match = re.search(regular, name_column)
            if match:
                depfm_index_column = number
            regular = r".+(deg\sC).+"
            match = re.search(regular, name_column)
            if match:
                temperature_deg_c_index_column = number
                name_temperature_deg_c_index_column = match[0]

        tmd = (
            -0.00000007610308758 * dataframe.iloc[:, depfm_index_column] ** 2
            - 0.0019619296 * dataframe.iloc[:, depfm_index_column]
            + 3.9646054
        )

        second_column = dataframe.columns.size
        dataframe.insert(loc=second_column, column="Tmd", value=tmd)
        dataframe.insert(
            loc=second_column + 1,
            column="Temperature < Tmd",
            value=dataframe.iloc[:, temperature_deg_c_index_column]
            < dataframe.iloc[:, second_column],
        )
        result_tdm = dataframe[
            "Temperature < Tmd"
        ].value_counts()  # return True or False

        # save Dataframe (development instrument)
        # dataframe.to_csv('result_tmd_search\\dataframe.csv', sep='\t', index=False)
        # print(dataframe)

        path = cnv_header_data.name_file_cnv
        sbe_version = cnv_header_data.sbe_version
        start_time = (
            cnv_header_data.start_time if cnv_header_data.start_time else "None"
        )
        system_upload_date = (
            cnv_header_data.system_upload_time
            if cnv_header_data.system_upload_time
            else "None"
        )
        latitude = cnv_header_data.latitude if cnv_header_data.latitude else "None"
        row_latitude = (
            cnv_header_data.row_latitude if cnv_header_data.latitude else "None"
        )
        longitude = cnv_header_data.longitude if cnv_header_data.longitude else "None"
        row_longitude = (
            cnv_header_data.row_longitude if cnv_header_data.longitude else "None"
        )
        station = cnv_header_data.station if cnv_header_data.station else "None"
        max_depth = (
            cnv_header_data.spans_list[0][1]
            if cnv_header_data.spans_list[0][1]
            else "None"
        )
        surface_temperature = DataTools.search_temperature_in_depth(
            data_type, dataframe, temperature_deg_c_index_column
        )

        max_tmd_vs_temperature = DataTools.search_max_difference_tmd_temperature(
            data_type, dataframe, temperature_deg_c_index_column
        )
        station_name_file_cnv = cnv_header_data.station_name_file_cnv
        date_name_file_cnv = cnv_header_data.date_name_file_cnv

        total_number = dataframe.shape[0]
        true_number = total_number - result_tdm.iloc[0]
        dive_begin_index = index_list[0]
        lift_begin_index = index_list[1]
        error = DataTools.log_error_flag_data(
            data_type, dataframe, depfm_index_column, temperature_deg_c_index_column
        )
        name_temperature_deg_c_index_column = name_temperature_deg_c_index_column

        depth = dataframe.iloc[:, depfm_index_column].to_frame().T
        depth.insert(0, "0", cnv_header_data.name_file_cnv)
        temperature = dataframe.iloc[:, temperature_deg_c_index_column].to_frame().T
        temperature.insert(0, "0", cnv_header_data.name_file_cnv)
        depth.to_csv(
            f"result_tmd_search\\data.csv",
            sep="\t",
            header=False,
            mode="a",
            index=False,
        )
        temperature.to_csv(
            f"result_tmd_search\\data.csv",
            sep="\t",
            header=False,
            mode="a",
            index=False,
        )

        result_file.loc[0] = [
            path,
            sbe_version,
            start_time,
            system_upload_date,
            date_name_file_cnv,
            latitude,
            row_latitude,
            longitude,
            row_longitude,
            station,
            station_name_file_cnv,
            max_depth,
            surface_temperature,
            max_tmd_vs_temperature,
            name_temperature_deg_c_index_column,
            true_number,
            total_number,
            dive_begin_index,
            lift_begin_index,
            error,
        ]

        return result_file

    @staticmethod
    def tmd_analysis_csv(
        data_type, csv_header_data, csv_body_data, index_list
    ):  # придумать названия функции
        columns = [
            "Date",
            "Depth [m]",
            "Temp. [degC]",
            "Sal.",
            "Cond. [mS/cm]",
            "EC25 [mS/cm]",
            "Density [kg/m3]",
            "SigmaT",
            "Chl-Flu. [ppb]",
            "Chl-a [mg/l]",
            "Turb. [FTU]",
            "pH",
            "ORP [mV]",
            "DO [%]",
            "DO [mg/l]",
            "Quant. [mmol/(m2*s)]",
            "Mark",
        ]

        result_file = pd.DataFrame(
            columns=[
                "Path",
                "Sond_number",
                "Soft_Version",
                "Start_Time",
                "End_Time",
                "Date_name_file_csv",
                "Station_name_file_csv",
                "Max_Depth",
                "Surface_temperature",
                "Max_difference_Tmd_Temperature",
                "Count_True",
                "Count_Total",
                "Dive_Begin_Index",
                "Dive_End_Index",
                "Date_coef",
                "DO_coef(G,H)",
                "pH_coef(A,B)",
                "Error",
            ]
        )

        dataframe = csv_body_data.table_data
        dataframe.columns = columns

        tmd = (
            -0.00000007610308758 * dataframe["Depth [m]"] ** 2
            - 0.0019619296 * dataframe["Depth [m]"]
            + 3.9646054
        )

        second_column = dataframe.columns.size
        dataframe.insert(loc=second_column, column="Tmd", value=tmd)
        dataframe.insert(
            loc=second_column + 1,
            column="Temperature < Tmd",
            value=dataframe["Temp. [degC]"] < dataframe.iloc[:, second_column],
        )
        result_tdm = dataframe[
            "Temperature < Tmd"
        ].value_counts()  # return True or False

        # save Dataframe (development instrument)
        # dataframe.to_csv('result_tmd_search\\dataframe.csv', sep='\t', index=False)
        # print(dataframe)

        path = csv_header_data.name_file_csv
        sonde_no = csv_header_data.sonde_no
        soft_version = csv_header_data.version
        start_time = (
            csv_header_data.start_time if csv_header_data.start_time else "None"
        )
        end_time = csv_header_data.end_time if csv_header_data.end_time else "None"
        date_name_file_csv = (
            csv_header_data.date_name_file_csv
            if csv_header_data.date_name_file_csv
            else "None"
        )
        station_name_file_csv = (
            csv_header_data.station_name_file_csv
            if csv_header_data.station_name_file_csv
            else "None"
        )
        max_depth = (
            dataframe["Depth [m]"].max() if dataframe["Depth [m]"].max() else "None"
        )
        surface_temperature = DataTools.search_temperature_in_depth(
            data_type, dataframe
        )
        max_tmd_vs_temperature = DataTools.search_max_difference_tmd_temperature(
            data_type, dataframe
        )

        total_number = dataframe.shape[0]
        true_number = total_number - result_tdm.iloc[0]
        dive_begin_index = index_list[0]
        lift_begin_index = index_list[1]
        data_coef = csv_header_data.coef_date
        do_coef = (
            rf"{csv_header_data.ch_list[7][5]}"
            + "   "
            + rf"{csv_header_data.ch_list[7][6]}"
        )
        ph_coef = (
            rf"{csv_header_data.ch_list[9][0]}"
            + " "
            + rf"{csv_header_data.ch_list[9][1]}"
        )

        error = DataTools.log_error_flag_data(data_type, dataframe)

        depth = dataframe["Depth [m]"].to_frame().T
        depth.insert(0, "0", csv_header_data.name_file_csv)
        temperature = dataframe["Temp. [degC]"].to_frame().T
        temperature.insert(0, "0", csv_header_data.name_file_csv)
        depth.to_csv(
            f"result_tmd_search\\data.csv",
            sep="\t",
            header=False,
            mode="a",
            index=False,
        )
        temperature.to_csv(
            f"result_tmd_search\\data.csv",
            sep="\t",
            header=False,
            mode="a",
            index=False,
        )

        result_file.loc[0] = [
            path,
            sonde_no,
            soft_version,
            start_time,
            end_time,
            date_name_file_csv,
            station_name_file_csv,
            max_depth,
            surface_temperature,
            max_tmd_vs_temperature,
            true_number,
            total_number,
            dive_begin_index,
            lift_begin_index,
            data_coef,
            do_coef,
            ph_coef,
            error,
        ]

        return result_file
