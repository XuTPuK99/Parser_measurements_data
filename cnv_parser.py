import re
import datetime
from typing import Optional, Union, List
from pydantic import BaseModel


class HeaderData(BaseModel):
    file_name: Optional[str] = None
    software_version: Optional[float] = None
    temperature_sn: Optional[int] = None
    conductivity_sn: Optional[int] = None
    cruise: Optional[str] = None
    vessel_or_ship: Optional[str] = None
    station: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
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
    table_data: Optional[List[List[float]]] = []


class CnvParser:
    def __init__(self, file_cnv_path):
        self.file_cnv_path: str = file_cnv_path
        self.file_data: str = str()

        with (open(self.file_cnv_path, 'r') as file):
            self.file_data = file.read()

    def header_parse(self) -> HeaderData:
        header_data = HeaderData()

        regular = r'(?<=\*\sFileName\s=\s).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.file_name = match[0]

        regular = r'(?<=\*\sSoftware\sVersion\s).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.software_version = float(match[0])

        regular = r'(?<=\*\sTemperature\sSN\s=\s).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.temperature_sn = int(match[0])

        regular = r'(?<=\*\sConductivity\sSN\s=\s).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.conductivity_sn = int(match[0])

        regular = r'(?<=Cruise:\s).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.cruise = match[0]

        regular = r'(?<=Vessel:\s).+'
        match = re.search(regular, self.file_data)
        if match:
            regular = r'\S+'
            match = re.search(regular, match[0])
            header_data.vessel_or_ship = match[0]
        else:
            regular = r'(?<=Ship:\s).+'
            match = re.search(regular, self.file_data)
            if match:
                regular = r'\S+'
                match = re.search(regular, match[0])
                header_data.vessel_or_ship = match[0]

        regular = r'(?<=Station:).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.station = match[0]

        regular = r'(?<=Latitude:\s).+'
        match = re.search(regular, self.file_data)
        if match:
            items = match[0].split()
            if len(items) == 3:
                header_data.latitude = float(items[0]) + (float(f'{items[1]}.{items[2]}') / 60)
            else:
                header_data.latitude = float(items[0]) + (float(items[1]) / 60)

        regular = r'(?<=Longitude:\s).+'
        match = re.search(regular, self.file_data)
        if match:
            items = match[0].split()
            if len(items) == 3:
                header_data.longitude = float(items[0]) + (float(f'{items[1]}.{items[2]}') / 60)
            else:
                header_data.longitude = float(items[0]) + (float(items[1]) / 60)

        regular = r'(?<=battery\stype\s=\s).+'
        match = re.search(regular, self.file_data)
        if match:
            header_data.battery_type = match[0]

        regular = r'(?<=stored\svoltage\s#\s\d\s=\s).+'
        match = re.findall(regular, self.file_data)
        if match:
            for i in range(len(match)):
                header_data.stored_voltage.append(match[i])

        regular = r'\scast\s+\d{1,2}.+'
        match_data = re.search(regular, self.file_data)
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
            match = re.search(regular, self.file_data)
            if match:
                header_data.nquan = int(match[0])

            regular = r'(?<=nvalues\s=\s).+'
            match = re.search(regular, self.file_data)
            if match:
                header_data.nvalues = int(match[0])

            regular = r'(?<=units\s=\s).+'
            match = re.search(regular, self.file_data)
            if match:
                header_data.units = match[0]

            regular = r'#\sname\s\d{1,2}\s=\s(.+)'
            match = re.findall(regular, self.file_data)
            if match:
                for name in match:
                    header_data.name_list.append(name)

            regular = r'#\sspan\s\d{1,2}\s=\s(.+)'
            match = re.findall(regular, self.file_data)
            if match:
                for spans in match:
                    x_span, y_span = (spans.split(','))
                    header_data.spans_list.append([float(x_span), float(y_span)])

            regular = r'(?<=interval\s=\s).+'
            match = re.search(regular, self.file_data)
            if match:
                metric, measurement = match[0].split()
                header_data.interval = [metric, float(measurement)]

            regular = r'(?<=start_time\s=\s).+'
            match = re.search(regular, self.file_data)
            if match:
                regular = r'\w+\s\d+\s\d+\s\d+:\d+:\d+'
                match = re.search(regular, match[0])
                header_data.start_time = datetime.datetime.strptime(match[0], '%b %d %Y %X')

            regular = r'(?<=bad_flag\s=\s).+'
            match = re.search(regular, self.file_data)
            if match:
                header_data.bad_flag = float(match[0])

            # XML parser, НЕ РАБОТАЕТ
            """
            regular = r'\<.+\>'
            match = re.findall(regular, self.data)
            string_data: str = str()
            if match:
                for data in match:
                    string_data = string_data + data
                regular = r'<Sensors count="\d"\s>'
                match = re.search(regular, string_data)
                self.xml_data.sensors_count = match[0]

                regular = r'<sensor\sChannel="\d"\s>.+?</sensor>'
                match = re.findall(regular, string_data)
                for i in match:
                    print(i)
            """

            regular = r'(?<=datcnv_in\s=\s).+'
            match = re.search(regular, self.file_data)
            if match:
                header_data.hex_file, header_data.conf_file = match[0].split()

            return header_data

    def body_parse(self) -> BodyData:
        body_data = BodyData()

        # Table parser
        regular = r'(?<=\*END\*\n).+'
        match = re.search(regular, self.file_data, flags=re.DOTALL)
        table_row = match[0].split('\n')
        for row in table_row:
            regular = r'\d+.\d+'
            match = re.findall(regular, row)
            if match:
                body_data.table_data.append([float(item) for item in match])

        return body_data
