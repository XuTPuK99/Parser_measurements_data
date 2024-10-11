import re
import datetime
from typing import Optional, Union, List

import pandas as pd
from pydantic import BaseModel, ConfigDict


class HeaderData(BaseModel):
    full_path_file: Optional[str] = None
    name_file_cnv: Optional[str] = None
    station_name_file_cnv: Optional[str] = None
    date_name_file_cnv: Optional[str] = None
    sbe_version: Optional[str] = None
    file_name: Optional[str] = None
    software_version: Optional[str] = None
    temperature_sn: Optional[int] = None
    conductivity_sn: Optional[int] = None
    system_upload_time: Union[datetime.datetime, str] = None
    cruise: Optional[str] = None
    vessel_or_ship: Optional[str] = None
    station: Optional[str] = None
    latitude: Optional[float] = None
    row_latitude: Optional[str] = None
    longitude: Optional[float] = None
    row_longitude: Optional[str] = None
    battery_type: Optional[str] = None
    stored_voltage: Optional[List[str]] = []
    cast: Optional[int] = None
    cast_date: Optional[datetime.datetime] = None
    samples: Optional[int] = None
    nv: Optional[int] = None
    avg: Optional[int] = None
    stop: Optional[str] = None
    nquan: Optional[int] = None
    nvalues: Optional[int] = None
    units: Optional[str] = None
    name_list: Optional[List[str]] = []
    spans_list: Optional[List[List[float]]] = []
    interval: Optional[List[Union[str, float]]] = None
    start_time: Optional[datetime.datetime] = None
    bad_flag: Optional[float] = None
    hex_file: Optional[str] = None
    conf_file: Optional[str] = None


class BodyData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    table_data: Optional[pd.DataFrame] = []


class CnvParser:
    @staticmethod
    def parse(file_name, data):
        regular = r'(.+)\*END\*\s*(.+)'
        match = re.search(regular, data, flags=re.DOTALL)
        header_text = match[1] if match else data
        body_text = match[2] if match else data

        header_data = CnvParser.header_parse(file_name, header_text)
        body_data = CnvParser.body_parse(body_text)
        return header_data, body_data

    @staticmethod
    def header_parse(file_name, data) -> HeaderData:
        header_data = HeaderData()

        header_data.full_path_file = file_name

        regular = r'(?<=\*\sSea-Bird\s)SBE\s?\d+'
        match = re.search(regular, data)
        if match:
            header_data.sbe_version = match[0]

        regular = r'(?<=\*\sFileName\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.file_name = match[0]

        regular = r'\\cnvdata(\\du)?\\(\d?\.?\d?[a-zA-Z]+)'
        match = re.search(regular, header_data.full_path_file, flags=re.I)
        if match:
            header_data.station_name_file_cnv = match[2]

        regular = r'(\d+)\.CNV'
        match = re.search(regular, header_data.full_path_file, flags=re.I)
        if match:
            regular = r'\d*(\d{2})(\d{2})'
            match = re.search(regular, match[1], flags=re.I)
            if match:
                header_data.date_name_file_cnv = f'{match[2]}.{match[1]}'
            regular = r'\\(\d{4})\\'
            match = re.search(regular, header_data.full_path_file, flags=re.I)
            if match:
                header_data.date_name_file_cnv = f'{header_data.date_name_file_cnv}.{match[1]}'

        regular = r'(?<=\*\sSoftware\sVersion\s).+'
        match = re.search(regular, data)
        if match:
            header_data.software_version = str(match[0])

        regular = r'(?<=\*\sTemperature\sSN\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.temperature_sn = int(match[0])

        regular = r'(?<=\*\sConductivity\sSN\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.conductivity_sn = int(match[0])

        regular = r'(?<=\*\sSystem\sUpLoad\sTime\s=\s).+'
        match = re.search(regular, data)
        if match:
            regular = r'\w+\s\d+\s\d+\s\d+:\d+:\d+'
            match = re.search(regular, match[0])
            if match:
                try:
                    header_data.system_upload_time = datetime.datetime.strptime(match[0], '%b %d %Y %X')
                except ValueError as e:
                    header_data.system_upload_time = match[0]

        regular = r'(?<=Cruise:).+'
        match = re.search(regular, data)
        if match:
            header_data.cruise = match[0]

        regular = r'(?<=Vessel:).+'
        match = re.search(regular, data)
        if match:
            regular = r'\S+'
            match = re.search(regular, match[0])
            if match:
                header_data.vessel_or_ship = match[0]

        regular = r'(?<=Ship:).+'
        match = re.search(regular, data)
        if match:
            regular = r'\S+'
            match = re.search(regular, match[0])
            if match:
                header_data.vessel_or_ship = match[0]

        regular = r'(?<=Station:).+'
        match = re.search(regular, data)
        if match:
            header_data.station = match[0]

        regular = r'(?<=Latitude:).+'
        match = re.search(regular, data)
        if match:
            header_data.row_latitude = match[0]
            item = (match[0].replace(',', '.').replace('N', ' ')
                    .replace('..', ' ').replace("'", " ")
                    .replace("''", " ").replace('"', ' ')
                    .replace('y', ' ').replace('_', ' ')
                    .replace('/', ' ').replace('v', ' ')
                    .replace('`', ''))
            regular = r'\d+\.\d+\.\d+'
            match = re.search(regular, item)
            if match:
                item = item.replace('.', ' ')
            regular = r'\d+\s\.\d+\.\d+'
            match = re.search(regular, item)
            if match:
                item = item.replace('.', ' ')

            items = item.split()
            if items:
                if len(items) == 3:
                    header_data.latitude = float(items[0]) + (float(items[1]) / 60) + (float(items[2]) / 3600)
                if len(items) == 2:
                    header_data.latitude = float(items[0]) + (float(items[1]) / 60)
                if len(items) == 1:
                    header_data.latitude = float(items[0])

        regular = r'(?<=Longitude:).+'
        match = re.search(regular, data)
        if match:
            header_data.row_longitude = match[0]
            item = (match[0].replace(',', '.').replace('E', ' ')
                    .replace('..', ' ').replace("'", " ")
                    .replace("''", " ").replace('"', ' ')
                    .replace('y', '').replace('_', ' ')
                    .replace('/', ' ').replace('v', ' ')
                    .replace('`', ' '))
            regular = r'\d+\.\d+\.\d+'
            match = re.search(regular, item)
            if match:
                item = item.replace('.', ' ')
            regular = r'\d+\s\.\d+\.\d+'
            match = re.search(regular, item)
            if match:
                item = item.replace('.', ' ')

            items = item.split()
            if items:
                if len(items) == 3:
                    header_data.longitude = float(items[0]) + (float(items[1]) / 60) + (float(items[2]) / 3600)
                if len(items) == 2:
                    header_data.longitude = float(items[0]) + (float(items[1]) / 60)
                if len(items) == 1:
                    header_data.longitude = float(items[0])

        regular = r'(?<=battery\stype\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.battery_type = match[0]

        regular = r'(?<=stored\svoltage\s#\s\d\s=\s).+'
        match = re.findall(regular, data)
        if match:
            for i in range(len(match)):
                header_data.stored_voltage.append(match[i])

        regular = r'\scast\s+\d{1,2}.+'
        match_data = re.search(regular, data)
        if match_data:
            regular = r'\scast\s+(\d{1,2})'
            match = re.search(regular, match_data[0])
            if match:
                header_data.cast = int(match[1])

            regular = r's.{5,6}\s(\d+)\sto\s(\d+)'
            match = re.search(regular, match_data[0])
            if match:
                header_data.samples = int(match[2]) - int(match[1])

            regular = r'\snv\s+=\s+(\d{1,2})'
            match = re.search(regular, match_data[0])
            if match:
                header_data.nv = int(match[1])

            regular = r'\savg\s+=\s+(\d{1,2})'
            match = re.search(regular, match_data[0])
            if match:
                header_data.avg = int(match[1])

            regular = r'\sst.{1,2}\s+=\s+(.+)'
            match = re.search(regular, match_data[0])
            if match:
                header_data.stop = match[1]

        regular = r'(?<=nquan\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.nquan = int(match[0])

        regular = r'(?<=nvalues\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.nvalues = int(match[0])

        regular = r'(?<=units\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.units = match[0]

        regular = r'#\sname\s\d{1,2}\s=\s(.+)'
        match = re.findall(regular, data)
        if match:
            for name in match:
                header_data.name_list.append(name)

        regular = r'#\sspan\s\d{1,2}\s=\s(.+)'
        match = re.findall(regular, data)
        if match:
            for spans in match:
                x_span, y_span = (spans.split(','))
                header_data.spans_list.append([float(x_span), float(y_span)])

        regular = r'(?<=interval\s=\s).+'
        match = re.search(regular, data)
        if match:
            metric, measurement = match[0].split()
            header_data.interval = [metric, float(measurement)]

        regular = r'(?<=start_time\s=\s).+'
        match = re.search(regular, data)
        if match:
            regular = r'\w+\s\d+\s\d+\s\d+:\d+:\d+'
            match = re.search(regular, match[0])
            if match:
                try:
                    header_data.start_time = datetime.datetime.strptime(match[0], '%b %d %Y %X')
                except ValueError as e:
                    header_data.system_upload_time = match[0]


        regular = r'(?<=bad_flag\s=\s).+'
        match = re.search(regular, data)
        if match:
            header_data.bad_flag = float(match[0])

        regular = r'(?<=datcnv_in\s=\s).+'
        datcnv_in_match = re.search(regular, data)
        if datcnv_in_match:
            regular = r'.+\.hex'
            match = re.search(regular, datcnv_in_match[0], flags=re.I)
            if match:
                header_data.hex_file = match[0]
            else:
                regular = r'.+\.dat'
                match = re.search(regular, datcnv_in_match[0], flags=re.I)
                if match:
                    header_data.hex_file = match[0]

            regular = r'\s(.+\.con)'
            match = re.search(regular, datcnv_in_match[0], flags=re.I)
            if match:
                header_data.conf_file = match[1]

        return header_data

    @staticmethod
    def body_parse(data) -> BodyData:
        body_data = BodyData()

        regular = r'(?<=\*END\*).+'
        match = re.search(regular, data, flags=re.DOTALL)
        if match:
            data = match[0]

        table_row = data.split('\n')
        for row in table_row:
            if not len(row):
                continue
            regular = r'\s+'
            values = re.split(regular, row)

            body_data.table_data.append([float(item) for item in values if len(item)])
        body_data.table_data = pd.DataFrame(body_data.table_data)

        return body_data
