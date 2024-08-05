import re
import datetime
from typing import Optional, Union, List
from pydantic import BaseModel


class HeaderData(BaseModel):
    name_file_cnv: Optional[str] = None
    file_name: Optional[str] = None
    software_version: Optional[str] = None
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
    def __init__(self, files_cnv):
        self.list_header_data: List[HeaderData] = []
        self.list_body_data: List[BodyData] = []

        self.files_cnv: List[str] = files_cnv if isinstance(files_cnv, list) else [files_cnv]

        self.files_data: List[str] = []
        self.names_files_cnv: List[str] = []

        for number, file_cnv in enumerate(self.files_cnv):
            name_file_cnv = file_cnv
            with (open(file_cnv, 'r') as file):
                file_data = file.read()
            self.names_files_cnv.append(name_file_cnv)
            self.files_data.append(file_data)

    def header_parse(self) -> List[HeaderData]:
        for number, file in enumerate(self.files_data):
            header_data = HeaderData()

            header_data.name_file_cnv = self.names_files_cnv[number]
            print(header_data.name_file_cnv, 'HeaderData')

            regular = r'(?<=\*\sFileName\s=\s).+'
            match = re.search(regular, file)
            if match:
                header_data.file_name = match[0]

            regular = r'(?<=\*\sSoftware\sVersion\s).+'
            match = re.search(regular, file)
            if match:
                header_data.software_version = str(match[0])

            regular = r'(?<=\*\sTemperature\sSN\s=\s).+'
            match = re.search(regular, file)
            if match:
                header_data.temperature_sn = int(match[0])

            regular = r'(?<=\*\sConductivity\sSN\s=\s).+'
            match = re.search(regular, file)
            if match:
                header_data.conductivity_sn = int(match[0])

            regular = r'(?<=Cruise:).+'
            match = re.search(regular, file)
            if match:
                header_data.cruise = match[0]

            regular = r'(?<=Vessel:).+'
            match = re.search(regular, file)
            if match:
                regular = r'\S+'
                match = re.search(regular, match[0])
                if match:
                    header_data.vessel_or_ship = match[0]

            regular = r'(?<=Ship:).+'
            match = re.search(regular, file)
            if match:
                regular = r'\S+'
                match = re.search(regular, match[0])
                if match:
                    header_data.vessel_or_ship = match[0]

            regular = r'(?<=Station:).+'
            match = re.search(regular, file)
            if match:
                header_data.station = match[0]

            regular = r'(?<=Latitude:).+'
            match = re.search(regular, file)
            if match:
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
            match = re.search(regular, file)
            if match:
                item = (match[0].replace(',', '.').replace('E', ' ')
                        .replace('..', ' ').replace("'", " ")
                        .replace("''", " ").replace('"', ' ')
                        .replace('y', '').replace('_', ' ')
                        .replace('/', ' ').replace('v', ' ')
                        .replace('`', ' '))
                regular = r'\d+\.\d+\.\d+'
                match = re.search(regular, item)
                if match:
                    item = item.replace('.',' ')
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
            match = re.search(regular, file)
            if match:
                header_data.battery_type = match[0]

            regular = r'(?<=stored\svoltage\s#\s\d\s=\s).+'
            match = re.findall(regular, file)
            if match:
                for i in range(len(match)):
                    header_data.stored_voltage.append(match[i])

            regular = r'\scast\s+\d{1,2}.+'
            match_data = re.search(regular, file)
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
            match = re.search(regular, file)
            if match:
                header_data.nquan = int(match[0])

            regular = r'(?<=nvalues\s=\s).+'
            match = re.search(regular, file)
            if match:
                header_data.nvalues = int(match[0])

            regular = r'(?<=units\s=\s).+'
            match = re.search(regular, file)
            if match:
                header_data.units = match[0]

            regular = r'#\sname\s\d{1,2}\s=\s(.+)'
            match = re.findall(regular, file)
            if match:
                for name in match:
                    header_data.name_list.append(name)

            regular = r'#\sspan\s\d{1,2}\s=\s(.+)'
            match = re.findall(regular, file)
            if match:
                for spans in match:
                    x_span, y_span = (spans.split(','))
                    header_data.spans_list.append([float(x_span), float(y_span)])

            regular = r'(?<=interval\s=\s).+'
            match = re.search(regular, file)
            if match:
                metric, measurement = match[0].split()
                header_data.interval = [metric, float(measurement)]

            regular = r'(?<=start_time\s=\s).+'
            match = re.search(regular, file)
            if match:
                regular = r'\w+\s\d+\s\d+\s\d+:\d+:\d+'
                match = re.search(regular, match[0])
                if match:
                    header_data.start_time = datetime.datetime.strptime(match[0], '%b %d %Y %X')

            regular = r'(?<=bad_flag\s=\s).+'
            match = re.search(regular, file)
            if match:
                header_data.bad_flag = float(match[0])

            regular = r'(?<=datcnv_in\s=\s).+'
            match = re.search(regular, file)
            if match:
                regular = r'.+\.hex'
                match = re.search(regular, match[0])
                if match:
                    header_data.hex_file = match[0]

                # НЕ РАБОТАЕТ!!!
                """
                regular = r'.+\.con'
                match = re.search(regular, file)
                if match:
                    print(match[0])
                    header_data.conf_file = match[0].split()
                """

            self.list_header_data.append(header_data)

        return self.list_header_data

    def body_parse(self, name) -> List[BodyData]:
        for number, file in enumerate(self.files_data):
            body_data = BodyData()
            print(name[number].name_file_cnv, 'BodyData')

            # Table parser
            regular = r'(?<=\*END\*).+'
            match = re.search(regular, file, flags=re.DOTALL)

            if match:
                table_row = match[0].split('\n')
                for row in table_row:
                    regular = r'\S+'
                    match = re.findall(regular, row)
                    if match:
                        body_data.table_data.append([float(item) for item in match])

            self.list_body_data.append(body_data)

        return self.list_body_data
