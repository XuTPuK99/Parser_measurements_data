import re
import datetime
from typing import Optional
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


class UserPolynomialSensor2(Sensor):
    name_sensor: Optional[str] = 'UserPolynomialSensor2'
    calibration_date: Optional[datetime.datetime] = None
    A0: Optional[float] = None
    A1: Optional[float] = None
    A2: Optional[float] = None
    A3: Optional[float] = None


class UserPolynomialSensor3(Sensor):
    name_sensor: Optional[str] = 'UserPolynomialSensor3'
    calibration_date: Optional[datetime.datetime] = None
    A0: Optional[float] = None
    A1: Optional[float] = None
    A2: Optional[float] = None
    A3: Optional[float] = None


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
    def convert_str_in_mouth(self, month):
        regular = r'\d{1,2}'
        match = re.search(regular, month)
        if match:
            return month

        regulars = [r'Jan?(?:uary|\.?)', r'Feb?(?:ruary|\.?)', r'Mar?(?:ch|\.?)', r'Apr?(?:il|\.?)',
                    r'May', r'Jun(?:e|\.?)',  r'Jul(?:e|\.?)',  r'Aug?(?:ust|\.?)',r'Sept?(?:ember|\.?)',
                    r'Oct?(?:ober|\.?)', r'Nov?(?:ember|\.?)',  r'Dec?(?:ember|\.?)']

        for number, regular in enumerate(regulars):
            match = re.search(regular, month)
            if match:
                return int(number + 1)


    @staticmethod
    def convert_str_in_year(self, year):
        regular = r'\d{1,2}'
        match = re.search(regular, year)
        if match:
            if int(year) < 80:
                year = f'20{year}'
            else:
                year = f'19{year}'

            return int(year)

    @staticmethod
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
                month = self.convert_str_in_mouth(self, date[1])
                year = self.convert_str_in_year(self, date[2])

                date = datetime.date(year=year, month=month, day=day)
                return date

    @staticmethod
    def cheking_split_string(self, conf_data, num, offset=0):
        if num + offset >= len(self.conf_data):
            list_split_string = (None for i in range(len(conf_data[num + offset])))
            return list_split_string
        else:
            list_split_string = conf_data[num + offset].split(' ')
            return list_split_string


class ConductivitySensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 1)
        split_string_2 = self.cheking_split_string(self, self.conf_data, num, 2)
        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 51))
        split_string_3 = self.cheking_split_string(self, self.conf_data, num, 109)

        return ConductivitySensor(
            sensor_number=self.conf_data[num],
            M=float(split_string_1[0]),
            A=float(split_string_1[1]),
            B=float(split_string_1[2]),
            C=float(split_string_1[3]),
            D=float(split_string_1[4]),
            CPCOR_1=float(split_string_1[5]),
            cell_const=float(split_string_2[0]),
            series_r=float(split_string_2[1]),
            slope=float(split_string_2[2]),
            offset=float(split_string_2[3]),
            calibration_date=date,
            G=float(split_string_3[0]),
            H=float(split_string_3[1]),
            I=float(split_string_3[2]),
            J=float(split_string_3[3]),
            CTCOR_2=float(split_string_3[4])
        )


class TemperatureSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 1)
        split_string_2 = self.cheking_split_string(self, self.conf_data, num, 107)
        date = self.cheking_date(self, self.cheking_split_string(
            self, self.conf_data, num, 49))

        return TemperatureSensor(
            sensor_number=self.conf_data[num],
            F0_1=float(split_string_1[0]),
            A=float(split_string_1[1]),
            B=float(split_string_1[2]),
            C=float(split_string_1[3]),
            D=float(split_string_1[4]),
            slope=float(split_string_1[5]),
            offset=float(split_string_1[6]),
            GHIJ=float(split_string_1[7]),
            calibration_date=date,
            F0_2=float(split_string_2[0]),
            G=float(split_string_2[1]),
            H=float(split_string_2[2]),
            I=float(split_string_2[3]),
            J=float(split_string_2[4])
        )


class PressureSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 1)
        split_string_2 = self.cheking_split_string(self, self.conf_data, num, 2)
        split_string_3 = self.cheking_split_string(self, self.conf_data, num, 3)
        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 45))

        return PressureSensor(
            sensor_number=self.conf_data[num],
            T1=float(split_string_1[0]),
            T2=float(split_string_1[1]),
            T3=float(split_string_1[2]),
            T4=float(split_string_1[3]),
            T5=float(split_string_1[4]),
            C1=float(split_string_2[0]),
            C2=float(split_string_2[1]),
            C3=float(split_string_2[2]),
            C4=float(split_string_2[3]),
            D1=float(split_string_3[0]),
            D2=float(split_string_3[1]),
            slope=float(split_string_3[2]),
            offset=float(split_string_3[3]),
            sensor_type=float(split_string_3[4]),
            AD590_M=float(split_string_3[5]),
            AD590_B=float(split_string_3[6]),
            calibration_date=date
            )


class TransmissometerSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 1)
        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 38))

        return TransmissometerSensor(
            sensor_number=self.conf_data[num],
            M=split_string_1[0],
            B=split_string_1[1],
            path_length=split_string_1[2],
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

        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 1))
        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 2)

        return UserPolynomialSensor1(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            A0=float(split_string_1[0]),
            A1=float(split_string_1[1]),
            A2=float(split_string_1[2]),
            A3=float(split_string_1[3])
        )


class UserPolynomialSensorBuilder2(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 1))
        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 2)

        return UserPolynomialSensor2(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            A0=float(split_string_1[0]),
            A1=float(split_string_1[1]),
            A2=float(split_string_1[2]),
            A3=float(split_string_1[3])
        )


class UserPolynomialSensorBuilder3(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 1))
        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 2)

        return UserPolynomialSensor3(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            A0=float(split_string_1[0]),
            A1=float(split_string_1[1]),
            A2=float(split_string_1[2]),
            A3=float(split_string_1[3])
        )


class PrimaryOxygenSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 1))
        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 2)
        split_string_2 = self.cheking_split_string(self, self.conf_data, num, 3)
        split_string_3 = self.cheking_split_string(self, self.conf_data, num, 95)

        return PrimaryOxygenSensor(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            soc=float(split_string_1[0]),
            tcor=float(split_string_1[1]),
            offset=float(split_string_1[2]),
            pcor=float(split_string_2[0]),
            tau=float(split_string_2[1]),
            boc=float(split_string_2[2]),
            sea_beard_equation=float(split_string_3[0]),
            soc2007=float(split_string_3[1]),
            A=float(split_string_3[2]),
            B=float(split_string_3[3]),
            C=float(split_string_3[4]),
            E=float(split_string_3[5]),
            voffset=float(split_string_3[6]),
            tau20=float(split_string_3[7]),
            D0=float(split_string_3[8]),
            D1=float(split_string_3[9]),
            D2=float(split_string_3[10]),
            H1=float(split_string_3[11]),
            H2=float(split_string_3[12]),
            H3=float(split_string_3[13])
        )


class OBSSensorBuilder(SensorBuilder):
    def get(self, num):
        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        date = self.cheking_date(self, self.cheking_split_string(self, self.conf_data, num, 1))
        split_string_1 = self.cheking_split_string(self, self.conf_data, num, 2)

        return TransmissometerSensor(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            a0=float(split_string_1[0]),
            a1=float(split_string_1[1]),
            a2=float(split_string_1[2])
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


class ConfParser:
    def __init__(self, file_config_path):
        file_config_path: str = file_config_path
        config_file_data: list[str]

        fabric = FabricSensor()

        with (open(file_config_path, 'r')) as file:
            config_file_data = file.read().splitlines()

        for i in range(len(config_file_data)):
            entity = fabric.get(i, config_file_data)
            if entity:
                print(entity)
