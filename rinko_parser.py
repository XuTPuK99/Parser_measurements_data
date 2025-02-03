import datetime
import re
from typing import Dict, List, Optional, Union

import pandas as pd
from pydantic import BaseModel, ConfigDict


class HeaderData(BaseModel):
    full_path_file: Optional[str] = None
    name_file_csv: Optional[str] = None
    station_name_file_csv: Optional[str] = None
    date_name_file_csv: Optional[str] = None
    version: Optional[float] = None
    file_date: Optional[datetime.datetime] = None
    format_version: Optional[float] = None
    data_format: Optional[float] = None
    delimiter: Optional[float] = None
    meas_mode: Optional[float] = None
    model: Optional[str] = None
    sonde_name: Optional[str] = None
    sonde_no: Optional[str] = None
    senser_type_1: Optional[str] = None
    senser_type_2: Optional[str] = None
    channel: Optional[int] = None
    comment: Optional[str] = None
    preheat: Optional[int] = None
    interval: Optional[int] = None
    samplecnt: Optional[int] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    eca: Optional[float] = None
    ecb: Optional[float] = None
    ecdeg: Optional[float] = None
    eccoef: Optional[float] = None
    chla: Optional[float] = None
    chlb: Optional[float] = None
    pc_swa: Optional[float] = None
    pc_swb: Optional[float] = None
    pc_swc: Optional[float] = None
    pc_swd: Optional[float] = None
    depth_zero: Optional[float] = None
    start_depth_a: Optional[float] = None
    start_depth_b: Optional[float] = None
    film_no: Optional[str] = None
    use_micro_mol: Optional[float] = None
    coef_date: Optional[datetime.datetime] = None
    ch_list: Optional[List[List[float]]] = []


class BodyData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    table_data: Optional[pd.DataFrame] = []


class RinkoParser:
    @staticmethod
    def parse(file_name, data):
        regular = r"(.+)[Item]\s*(.+)"
        match = re.search(regular, data, flags=re.DOTALL)
        header_text = match[1] if match else data
        body_text = match[2] if match else data

        header_data = RinkoParser.header_parse(file_name, header_text)
        body_data = RinkoParser.body_parse(body_text)
        return header_data, body_data

    @staticmethod
    def header_parse(file_name, data) -> HeaderData:
        header_data = HeaderData()

        header_data.full_path_file = file_name

        regular = r"\\(.+)_\w{2}_"
        match = re.search(regular, header_data.full_path_file, flags=re.I)
        if match:
            header_data.station_name_file_csv = match[1]
        regular = r".+_(\d{8})_(\d{6})"
        match = re.search(regular, header_data.full_path_file, flags=re.I)
        if match:
            header_data.date_name_file_csv = datetime.datetime.strptime(
                f"{match[1]}.{match[2]}", "%Y%m%d.%H%M%S"
            )

        regular = r"(//\sVersion\s)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.version = match[2]

        regular = r"(//\sFile Date:)(.+)"
        match = re.search(regular, data)
        if match:
            try:
                header_data.file_date = datetime.datetime.strptime(
                    match[2], "%Y.%m.%d %X"
                )
            except ValueError as e:
                header_data.file_date = match[0]

        regular = r"(FormatVersion=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.format_version = match[2]

        regular = r"(DataFormat=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.data_format = match[2]

        regular = r"(Delimiter=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.delimiter = match[2]

        regular = r"(MeasMode=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.meas_mode = match[2]

        regular = r"(Model=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.model = match[2]

        regular = r"(SondeName=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.sonde_name = match[2]

        regular = r"(SondeNo=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.sonde_no = match[2]

        regular = r"(SensorType=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.senser_type_1 = match[2]

        regular = r"(SensorType2=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.senser_type_2 = match[2]

        regular = r"(Channel=)(\d+)"
        match = re.search(regular, data)
        if match:
            header_data.model = match[2]

        regular = r"(Comment=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.comment = match[2]

        regular = r"(PreHeat=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.preheat = match[2]

        regular = r"(Interval=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.interval = match[2]

        regular = r"(SampleCnt=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.interval = match[2]

        regular = r"(StartTime=)(.+)"
        match = re.search(regular, data)
        if match:
            try:
                header_data.start_time = datetime.datetime.strptime(
                    match[2], "%Y.%m.%d %X"
                )
            except ValueError as e:
                header_data.start_time = match[0]

        regular = r"(EndTime=)(.+)"
        match = re.search(regular, data)
        if match:
            try:
                header_data.end_time = datetime.datetime.strptime(
                    match[2], "%Y.%m.%d %X"
                )
            except ValueError as e:
                header_data.end_time = match[0]

        regular = r"(ECA=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.eca = match[2]

        regular = r"(ECB=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.ecb = match[2]

        regular = r"(ECDeg=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.ecdeg = match[2]

        regular = r"(ECCoef=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.eccoef = match[2]

        regular = r"(CHLA=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.chla = match[2]

        regular = r"(CHLB=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.chlb = match[2]

        regular = r"(PC_SWA=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.pc_swa = match[2]

        regular = r"(PC_SWB=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.pc_swb = match[2]

        regular = r"(PC_SWC=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.pc_swc = match[2]

        regular = r"(PC_SWD=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.pc_swd = match[2]

        regular = r"(DepthZero=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.depth_zero = match[2]

        regular = r"(StartDepthA=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.start_depth_a = match[2]

        regular = r"(StartDepthB=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.start_depth_b = match[2]

        regular = r"(FilmNo=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.film_no = match[2]

        regular = r"(UseMicroMol=)(.+)"
        match = re.search(regular, data)
        if match:
            header_data.use_micro_mol = match[2]

        regular = r"(CoefDate=)(.+)"
        match = re.search(regular, data)
        if match:
            try:
                header_data.coef_date = datetime.datetime.strptime(match[2], "%Y/%m/%d")
            except ValueError as e:
                header_data.coef_date = match[0]

        regular = r"Ch\d{1,2}=(.+)"
        match = re.findall(regular, data)
        if match:
            for ch in match:
                ch = ch.split(sep=",")
                ch.remove("")
                ch = [float(item) for item in ch]
                header_data.ch_list.append(ch)

        return header_data

    @staticmethod
    def body_parse(data) -> BodyData:
        body_data = BodyData()
        regular = r",Mark,(.+)"
        match = re.search(regular, data, flags=re.DOTALL)
        if match:
            data = match[1]

        table_row = data.split("\n")
        for row in table_row:
            if not len(row):
                continue
            regular = r","
            values = re.split(regular, row)

            body_data.table_data.append([item for item in values if len(item)])
        body_data.table_data = pd.DataFrame(body_data.table_data)

        body_data.table_data.columns = [
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

        body_data.table_data["Date"] = pd.to_datetime(
            body_data.table_data["Date"], dayfirst=True
        )
        body_data.table_data["Depth [m]"] = body_data.table_data["Depth [m]"].astype(
            "float"
        )
        body_data.table_data["Temp. [degC]"] = body_data.table_data[
            "Temp. [degC]"
        ].astype("float")
        body_data.table_data["Sal."] = body_data.table_data["Sal."].astype("float")
        body_data.table_data["Cond. [mS/cm]"] = body_data.table_data[
            "Cond. [mS/cm]"
        ].astype("float")
        body_data.table_data["EC25 [mS/cm]"] = body_data.table_data[
            "EC25 [mS/cm]"
        ].astype("float")
        body_data.table_data["Density [kg/m3]"] = body_data.table_data[
            "Density [kg/m3]"
        ].astype("float")
        body_data.table_data["SigmaT"] = body_data.table_data["SigmaT"].astype("float")
        body_data.table_data["Chl-Flu. [ppb]"] = body_data.table_data[
            "Chl-Flu. [ppb]"
        ].astype("float")
        body_data.table_data["Chl-a [mg/l]"] = body_data.table_data[
            "Chl-a [mg/l]"
        ].astype("float")
        body_data.table_data["Turb. [FTU]"] = body_data.table_data[
            "Turb. [FTU]"
        ].astype("float")
        body_data.table_data["pH"] = body_data.table_data["pH"].astype("float")
        body_data.table_data["ORP [mV]"] = body_data.table_data["ORP [mV]"].astype(
            "float"
        )
        body_data.table_data["DO [%]"] = body_data.table_data["DO [%]"].astype("float")
        body_data.table_data["DO [mg/l]"] = body_data.table_data["DO [mg/l]"].astype(
            "float"
        )
        body_data.table_data["Quant. [mmol/(m2*s)]"] = body_data.table_data[
            "Quant. [mmol/(m2*s)]"
        ].astype("float")
        body_data.table_data["Mark"] = body_data.table_data["Mark"].astype("int")

        return body_data
