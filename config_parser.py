from typing import Optional
from pydantic import BaseModel
from datetime import datetime


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
    calibration_date: Optional[datetime] = None
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
    calibration_date: Optional[datetime] = None
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
    calibration_date: Optional[datetime] = None


class TransmissometerSensor(Sensor):
    name_sensor: Optional[str] = 'TransmissometerSensor'
    M: Optional[float] = None
    B: Optional[float] = None
    path_length: Optional[float] = None
    calibration_date: Optional[datetime] = None


class FirmwareVersion(BaseModel):
    name: Optional[str] = 'Firmware version'
    firmware_version: Optional[float] = None


class PrimaryOxygenSensor(Sensor):
    name_sensor: Optional[str] = 'PrimaryOxygenSensor'
    calibration_date: Optional[datetime] = None
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
    calibration_date: Optional[datetime] = None
    a0: Optional[float] = None
    a1: Optional[float] = None
    a2: Optional[float] = None


class SensorBuilder:
    def __init__(self, conf_data):
        self.conf_data = conf_data


class ConductivitySensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        split_string_2 = self.conf_data[num + 2].split(' ')
        date = self.conf_data[num + 51]
        split_string_3 = self.conf_data[num + 109].split(' ')

        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        if len(date) == 0:
            date = None
        else:
            date = datetime.strptime(date, '%d-%b-%y')

        return ConductivitySensor(
            sensor_number=self.conf_data[num],
            M=split_string_1[0],
            A=split_string_1[1],
            B=split_string_1[2],
            C=split_string_1[3],
            D=split_string_1[4],
            CPCOR_1=split_string_1[5],
            cell_const=split_string_2[0],
            series_r=split_string_2[1],
            slope=split_string_2[2],
            offset=split_string_2[3],
            calibration_date=date,
            G=split_string_3[0],
            H=split_string_3[1],
            I=split_string_3[2],
            J=split_string_3[3],
            CTCOR_2=split_string_3[4]
        )


class TemperatureSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        split_string_2 = self.conf_data[num + 107].split(' ')
        date = self.conf_data[num + 49]

        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        if len(date) == 0:
            date = None
        else:
            date = datetime.strptime(date, '%d-%b-%y')

        return TemperatureSensor(
            sensor_number=self.conf_data[num],
            F0_1=split_string_1[0],
            A=split_string_1[1],
            B=split_string_1[2],
            C=split_string_1[3],
            D=split_string_1[4],
            slope=split_string_1[5],
            offset=split_string_1[6],
            GHIJ=split_string_1[7],
            calibration_date=date,
            F0_2=split_string_2[0],
            G=split_string_2[1],
            H=split_string_2[2],
            I=split_string_2[3],
            J=split_string_2[4]
        )


class PressureSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        split_string_2 = self.conf_data[num + 2].split(' ')
        split_string_3 = self.conf_data[num + 3].split(' ')
        date = self.conf_data[num + 45]

        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        if len(date) == 0:
            date = None
        else:
            date = datetime.strptime(date, '%d-%b-%y')

        return PressureSensor(
            sensor_number=self.conf_data[num],
            T1=split_string_1[0],
            T2=split_string_1[1],
            T3=split_string_1[2],
            T4=split_string_1[3],
            T5=split_string_1[4],
            C1=split_string_2[0],
            C2=split_string_2[1],
            C3=split_string_2[2],
            C4=split_string_2[3],
            D1=split_string_3[0],
            D2=split_string_3[1],
            slope=split_string_3[2],
            offset=split_string_3[3],
            sensor_type=split_string_3[4],
            AD590_M=split_string_3[5],
            AD590_B=split_string_3[6],
            calibration_date=date
            )


class TransmissometerSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        date = self.conf_data[num + 38]

        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        if len(date) == 0:
            date = None
        else:
            date = datetime.strptime(date, '%d-%b-%y')

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
            firmware_version=self.conf_data[num]
        )


class PrimaryOxygenSensorBuilder(SensorBuilder):
    def get(self, num):
        date = self.conf_data[num + 1]
        split_string_1 = self.conf_data[num + 2].split(' ')
        split_string_2 = self.conf_data[num + 3].split(' ')
        split_string_3 = self.conf_data[num + 94].split(' ')

        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        if len(date) == 0:
            date = None
        else:
            date = datetime.strptime(date, '%d-%b-%y')

        return PrimaryOxygenSensor(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            soc=split_string_1[0],
            tcor=split_string_1[1],
            offset=split_string_1[2],
            pcor=split_string_2[0],
            tau=split_string_2[1],
            boc=split_string_2[2],
            sea_beard_equation=split_string_3[0],
            soc2007=split_string_3[1],
            A=split_string_3[2],
            B=split_string_3[3],
            C=split_string_3[4],
            E=split_string_3[5],
            voffset=split_string_3[6],
            tau20=split_string_3[7],
            D0=split_string_3[8],
            D1=split_string_3[9],
            D2=split_string_3[10],
            H1=split_string_3[11],
            H2=split_string_3[12],
            H3=split_string_3[13]
        )


class OBSSensorBuilder(SensorBuilder):
    def get(self, num):
        date = self.conf_data[num + 1]
        split_string_1 = self.conf_data[num + 2].split(' ')

        if num >= len(self.conf_data) or len(self.conf_data[num]) == 0:
            return None

        if len(date) == 0:
            date = None
        else:
            date = datetime.strptime(date, '%d-%b-%y')

        return TransmissometerSensor(
            sensor_number=self.conf_data[num],
            calibration_date=date,
            a0=split_string_1[0],
            a1=split_string_1[1],
            a2=split_string_1[2]
        )


class FabricSensor:
    fabric = {
        0: ConductivitySensorBuilder,
        3: TemperatureSensorBuilder,
        10: PressureSensorBuilder,
        21: TransmissometerSensorBuilder,
        43: FirmwareVersionBuilder,
        163: PrimaryOxygenSensorBuilder,
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

