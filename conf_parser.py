import re
import datetime
from typing import Optional, List, Type, Union
from pydantic import BaseModel


class Sensor(BaseModel):
    sensor_number: Optional[str] = None


class ConductivitySensor(Sensor):
    name_sensor: Optional[str] = 'ConductivitySensor'
    M: Optional[float] = None
    A: Optional[float] = None
    B: Optional[float] = None
    C: Optional[float] = None
    D: Optional[float] = None
    CPCOR_1: Optional[float] = None
    cell_const: Optional[float] = None
    series_r: Optional[float] = None
    slope: Optional[float] = None
    offset: Optional[float] = None
    calibration_date: Optional[datetime.datetime] = None
    G: Optional[float] = None
    H: Optional[float] = None
    I: Optional[float] = None
    J: Optional[float] = None
    CTCOR_2: Optional[float] = None


class TemperatureSensor(Sensor):
    name_sensor: Optional[str] = 'TemperatureSensor'
    F0_1: Optional[float] = None
    A: Optional[float] = None
    B: Optional[float] = None
    C: Optional[float] = None
    D: Optional[float] = None
    slope: Optional[float] = None
    offset: Optional[float] = None
    GHIJ: Optional[float] = None
    calibration_date: Optional[datetime.datetime] = None
    F0_2: Optional[float] = None
    G: Optional[float] = None
    H: Optional[float] = None
    I: Optional[float] = None
    J: Optional[float] = None


class PressureSensor(Sensor):
    name_sensor: Optional[str] = 'PressureSensor'
    T1: Optional[float] = None
    T2: Optional[float] = None
    T3: Optional[float] = None
    T4: Optional[float] = None
    C1: Optional[float] = None
    C2: Optional[float] = None
    C3: Optional[float] = None
    C4: Optional[float] = None
    D1: Optional[float] = None
    D2: Optional[float] = None
    slope: Optional[float] = None
    offset: Optional[float] = None
    sensor_type: Optional[float] = None
    AD590_M: Optional[float] = None
    AD590_B: Optional[float] = None
    calibration_date: Optional[datetime.datetime] = None


class TransmissometerSensor(Sensor):
    name_sensor: Optional[str] = 'TransmissometerSensor'
    M: Optional[float] = None
    B: Optional[float] = None
    path_length: Optional[float] = None
    calibration_date: Optional[datetime.datetime] = None


class FirmwareVersion(BaseModel):
    name: Optional[str] = 'Firmware version'
    firmware_version: Optional[float] = None


class UserPolynomialSensor1(Sensor):
    name_sensor: Optional[str] = 'UserPolynomialSensor1'
    calibration_date: Optional[datetime.datetime] = None
    A0: Optional[float] = None
    A1: Optional[float] = None
    A2: Optional[float] = None
    A3: Optional[float] = None
    UserPoly1: Optional[str] = None


class UserPolynomialSensor2(Sensor):
    name_sensor: Optional[str] = 'UserPolynomialSensor2'
    calibration_date: Optional[datetime.datetime] = None
    A0: Optional[float] = None
    A1: Optional[float] = None
    A2: Optional[float] = None
    A3: Optional[float] = None
    UserPoly2: Optional[str] = None


class UserPolynomialSensor3(Sensor):
    name_sensor: Optional[str] = 'UserPolynomialSensor3'
    calibration_date: Optional[datetime.datetime] = None
    A0: Optional[float] = None
    A1: Optional[float] = None
    A2: Optional[float] = None
    A3: Optional[float] = None
    UserPoly3: Optional[str] = None


class PrimaryOxygenSensor(Sensor):
    name_sensor: Optional[str] = 'PrimaryOxygenSensor'
    calibration_date: Optional[datetime.datetime] = None
    soc: Optional[float] = None
    tcor: Optional[float] = None
    offset: Optional[float] = None
    pcor: Optional[float] = None
    tau: Optional[float] = None
    boc: Optional[float] = None
    sea_beard_equation: Optional[float] = None
    soc2007: Optional[float] = None
    A: Optional[float] = None
    B: Optional[float] = None
    C: Optional[float] = None
    E: Optional[float] = None
    voffset: Optional[float] = None
    tau20: Optional[float] = None
    D0: Optional[float] = None
    D1: Optional[float] = None
    D2: Optional[float] = None
    H1: Optional[float] = None
    H2: Optional[float] = None
    H3: Optional[float] = None


class OBSSensor(Sensor):
    name_sensor: Optional[str] = 'OBSSensor'
    calibration_date: Optional[datetime.datetime] = None
    a0: Optional[float] = None
    a1: Optional[float] = None
    a2: Optional[float] = None


class SensorBuilder:
    def __init__(self, conf_data):
        self.conf_data = conf_data

    @staticmethod
    def convert_str_in_mouth(month):
        regular = r'\d{1,2}'
        match = re.search(regular, month)
        if match:
            return int(month)

        regulars = [r'Jan?(?:uary|\.?)', r'Feb?(?:ruary|\.?)', r'Mar?(?:ch|\.?)', r'Apr?(?:il|\.?)',
                    r'May', r'Jun(?:e|\.?)',  r'Jul(?:e|\.?)',  r'Aug?(?:ust|\.?)',r'Sept?(?:ember|\.?)',
                    r'Oct?(?:ober|\.?)', r'Nov?(?:ember|\.?)',  r'Dec?(?:ember|\.?)']

        for number, regular in enumerate(regulars):
            match = re.search(regular, month)
            if match:
                return int(number + 1)

    @staticmethod
    def convert_str_in_year(year):
        regular = r'\d{1,4}'
        match = re.search(regular, year)
        if match:
            if len(match[0]) == 2:
                if int(year) < 80:
                    year = f'20{year}'
                else:
                    year = f'19{year}'
            return int(year)
        return None

    def cheking_date(self, date_string):
        if len(date_string) == 0:
            return None

        for item in date_string:
            if item is None:
                return None

        regulars = [r'(\d{1,2})-(\d{1,2})-(\d{2,4})', r'(\d{1,2})-(\w+)-(\d{2,4})', r'(\d{1,2})-(\d{1,2})-(\d{2,4})\w']
        for regular in regulars:
            match = re.search(regular, date_string[0])
            if match:
                date = match[0].split('-')
                day = int(date[0])
                month = self.convert_str_in_mouth(date[1])
                year = self.convert_str_in_year(date[2])

                date = datetime.date(year=year, month=month, day=day)
                return date

    def split_string(self, num):
        if num < 0 or num >= len(self.conf_data):
            return None
        else:
            list_split_string = self.conf_data[num].split(' ')
            return list_split_string


class ConductivitySensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.split_string(num + 1)
        split_string_2 = self.split_string(num + 2)
        date = self.cheking_date(self.split_string(num + 51))
        split_string_3 = self.split_string(num + 109)

        return ConductivitySensor(
            sensor_number=self.conf_data[num],
            M=float(split_string_1[0]) if split_string_1 else None,
            A=float(split_string_1[1]) if split_string_1 else None,
            B=float(split_string_1[2]) if split_string_1 else None,
            C=float(split_string_1[3]) if split_string_1 else None,
            D=float(split_string_1[4]) if split_string_1 else None,
            CPCOR_1=float(split_string_1[5]) if split_string_1 else None,
            cell_const=float(split_string_2[0]) if split_string_2 else None,
            series_r=float(split_string_2[1]) if split_string_2 else None,
            slope=float(split_string_2[2]) if split_string_2 else None,
            offset=float(split_string_2[3]) if split_string_2 else None,
            calibration_date=date,
            G=float(split_string_3[0]) if split_string_3 else None,
            H=float(split_string_3[1]) if split_string_3 else None,
            I=float(split_string_3[2]) if split_string_3 else None,
            J=float(split_string_3[3]) if split_string_3 else None,
            CTCOR_2=float(split_string_3[4]) if split_string_3 else None
        )


class TemperatureSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.split_string(num + 1)
        split_string_2 = self.split_string(num + 107)
        date = self.cheking_date(self.split_string(num + 49))

        return TemperatureSensor(
            sensor_number=self.conf_data[num],
            F0_1=float(split_string_1[0]) if split_string_1 else None,
            A=float(split_string_1[1]) if split_string_1 else None,
            B=float(split_string_1[2]) if split_string_1 else None,
            C=float(split_string_1[3]) if split_string_1 else None,
            D=float(split_string_1[4]) if split_string_1 else None,
            slope=float(split_string_1[5]) if split_string_1 else None,
            offset=float(split_string_1[6]) if split_string_1 else None,
            GHIJ=float(split_string_1[7]) if split_string_1 else None,
            calibration_date=date,
            F0_2=float(split_string_2[0]) if split_string_2 else None,
            G=float(split_string_2[1]) if split_string_2 else None,
            H=float(split_string_2[2]) if split_string_2 else None,
            I=float(split_string_2[3]) if split_string_2 else None,
            J=float(split_string_2[4]) if split_string_2 else None
        )


class PressureSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.split_string(num + 1)
        split_string_2 = self.split_string(num + 2)
        split_string_3 = self.split_string(num + 3)
        date = self.cheking_date(self.split_string(num + 45))

        return PressureSensor(
            sensor_number=self.conf_data[num],
            T1=float(split_string_1[0]) if split_string_1 else None,
            T2=float(split_string_1[1]) if split_string_1 else None,
            T3=float(split_string_1[2]) if split_string_1 else None,
            T4=float(split_string_1[3]) if split_string_1 else None,
            T5=float(split_string_1[4]) if split_string_1 else None,
            C1=float(split_string_2[0]) if split_string_2 else None,
            C2=float(split_string_2[1]) if split_string_2 else None,
            C3=float(split_string_2[2]) if split_string_2 else None,
            C4=float(split_string_2[3]) if split_string_2 else None,
            D1=float(split_string_3[0]) if split_string_3 else None,
            D2=float(split_string_3[1]) if split_string_3 else None,
            slope=float(split_string_3[2])  if split_string_3 else None,
            offset=float(split_string_3[3]) if split_string_3 else None,
            sensor_type=float(split_string_3[4]) if split_string_3 else None,
            AD590_M=float(split_string_3[5]) if split_string_3 else None,
            AD590_B=float(split_string_3[6]) if split_string_3 else None,
            calibration_date=date
            )


class TransmissometerSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.split_string(num + 1)
        date = self.cheking_date(self.split_string(num + 38))

        return TransmissometerSensor(
            sensor_number=self.conf_data[num],
            M=split_string_1[0] if split_string_1 else None,
            B=split_string_1[1] if split_string_1 else None,
            path_length=split_string_1[2] if split_string_1 else None,
            calibration_date=date
        )


class FirmwareVersionBuilder:
    def __init__(self, conf_data):
        self.conf_data = conf_data

    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        return FirmwareVersion(
            firmware_version=float(self.conf_data[num])
        )


class UserPolynomialSensorBuilder1(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self.split_string(num + 1))
        split_string_1 = self.split_string(num + 2)
        split_string_2 = self.conf_data[num + 128]

        return UserPolynomialSensor1(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            A0=float(split_string_1[0]) if split_string_1 else None,
            A1=float(split_string_1[1]) if split_string_1 else None,
            A2=float(split_string_1[2]) if split_string_1 else None,
            A3=float(split_string_1[3]) if split_string_1 else None,
            UserPoly1=str(split_string_2) if split_string_2 else None
        )


class UserPolynomialSensorBuilder2(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self.split_string(num + 1))
        split_string_1 = self.split_string(num + 2)
        split_string_2 = self.conf_data[num + 126]

        return UserPolynomialSensor2(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            A0=float(split_string_1[0]) if split_string_1 else None,
            A1=float(split_string_1[1]) if split_string_1 else None,
            A2=float(split_string_1[2]) if split_string_1 else None,
            A3=float(split_string_1[3]) if split_string_1 else None,
            UserPoly2=str(split_string_2) if split_string_2 else None
        )


class UserPolynomialSensorBuilder3(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self.split_string(num + 1))
        split_string_1 = self.split_string(num + 2)
        split_string_2 = self.conf_data[num + 124]

        return UserPolynomialSensor3(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            A0=float(split_string_1[0]) if split_string_1 else None,
            A1=float(split_string_1[1]) if split_string_1 else None,
            A2=float(split_string_1[2]) if split_string_1 else None,
            A3=float(split_string_1[3]) if split_string_1 else None,
            UserPoly3=str(split_string_2) if split_string_2 else None
        )


class PrimaryOxygenSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self.split_string(num + 1))
        split_string_1 = self.split_string(num + 2)
        split_string_2 = self.split_string(num + 3)
        split_string_3 = self.split_string(num + 95)

        return PrimaryOxygenSensor(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            soc=float(split_string_1[0]) if split_string_1 else None,
            tcor=float(split_string_1[1]) if split_string_1 else None,
            offset=float(split_string_1[2]) if split_string_1 else None,
            pcor=float(split_string_2[0]) if split_string_2 else None,
            tau=float(split_string_2[1]) if split_string_2 else None,
            boc=float(split_string_2[2]) if split_string_2 else None,
            sea_beard_equation=float(split_string_3[0]) if split_string_3 else None,
            soc2007=float(split_string_3[1]) if split_string_3 else None,
            A=float(split_string_3[2]) if split_string_3 else None,
            B=float(split_string_3[3]) if split_string_3 else None,
            C=float(split_string_3[4]) if split_string_3 else None,
            E=float(split_string_3[5]) if split_string_3 else None,
            voffset=float(split_string_3[6]) if split_string_3 else None,
            tau20=float(split_string_3[7]) if split_string_3 else None,
            D0=float(split_string_3[8]) if split_string_3 else None,
            D1=float(split_string_3[9]) if split_string_3 else None,
            D2=float(split_string_3[10]) if split_string_3 else None,
            H1=float(split_string_3[11]) if split_string_3 else None,
            H2=float(split_string_3[12]) if split_string_3 else None,
            H3=float(split_string_3[13]) if split_string_3 else None
        )


class OBSSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self.split_string(num + 1))
        split_string_1 = self.split_string(num + 2)

        return TransmissometerSensor(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            a0=float(split_string_1[0]) if split_string_1 else None,
            a1=float(split_string_1[1]) if split_string_1 else None,
            a2=float(split_string_1[2]) if split_string_1 else None
        )


class FabricSensor:
    fabric = {
        0: ConductivitySensorBuilder,
        3: TemperatureSensorBuilder,
        10: PressureSensorBuilder,
        21: TransmissometerSensorBuilder,
        43: FirmwareVersionBuilder,
        73: UserPolynomialSensorBuilder1,
        76: UserPolynomialSensorBuilder2,
        79: UserPolynomialSensorBuilder3,
        162: PrimaryOxygenSensorBuilder,
        250: OBSSensorBuilder
    }

    def get(self, num, conf_data):
        if num in self.fabric:
            return self.fabric.get(num)(conf_data).get(num)
        return None


class ConfData(BaseModel):
    sensors: List[Type[Sensor]] = []


class ConfParser:
    def __init__(self, file_config_path):
        self.file_config_path: str = file_config_path

    def conf_parse(self):
        fabric = FabricSensor()
        conf_data = ConfData()

        with (open(self.file_config_path, 'r')) as file:
            config_file_data = file.read().splitlines()

        for i in range(len(config_file_data)):
            entity = fabric.get(i, config_file_data)
            if entity:
                conf_data.sensors.append(entity)

        return conf_data
