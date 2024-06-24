from typing import Optional
from pydantic import BaseModel


class Sensor(BaseModel):
    sensor_number: Optional[str] = None


class ConductivitySensor(Sensor):
    M: Optional[float] = None
    A: Optional[float] = None
    B: Optional[float] = None
    C: Optional[float] = None
    D: Optional[float] = None
    CPCOR: Optional[float] = None
    cell_const: Optional[float] = None
    series_r: Optional[float] = None
    slope: Optional[float] = None
    offset: Optional[float] = None
    GHIJ: Optional[float] = None


class TemperatureSensor(Sensor):
    F0: Optional[float] = None
    A: Optional[float] = None
    B: Optional[float] = None
    C: Optional[float] = None
    D: Optional[float] = None
    slope: Optional[float] = None
    offset: Optional[float] = None
    GHIJ: Optional[float] = None


class PressureSensor(Sensor):
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


class SensorBuilder:
    def __init__(self, conf_data):
        self.conf_data = conf_data


class ConductivitySensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' '),
        split_string_2 = self.conf_data[num + 2].split(' ')
        return ConductivitySensor(
            sensor_number=self.conf_data[num],
            M=split_string_1[0],
            A=split_string_1[1],
            B=split_string_1[2],
            C=split_string_1[3],
            D=split_string_1[4],
            CPCOR=split_string_1[5],
            cell_const=split_string_2[0],
            series_r=split_string_2[1],
            slope=split_string_2[2],
            offset=split_string_2[3],
            GHIJ=split_string_2[4]
        )


class TemperatureSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        return TemperatureSensor(
            sensor_number=self.conf_data[num],
            F0=split_string_1[0],
            A=split_string_1[1],
            B=split_string_1[2],
            C=split_string_1[3],
            D=split_string_1[4],
            slope=split_string_1[5],
            offset=split_string_1[6],
            GHIJ=split_string_1[7]
        )


class PressureSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        split_string_2 = self.conf_data[num + 2].split(' ')
        split_string_3 = self.conf_data[num + 3].split(' ')
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
            AD590_B=split_string_3[6]
        )


class FabricSensor:
    fabric = {
        0: ConductivitySensorBuilder,
        3: TemperatureSensorBuilder,
        10: PressureSensorBuilder
    }

    def get(self, num, conf_data):
        if num in self.fabric:
            return self.fabric.get(num)(conf_data).get(num)
        return None


class LaunchFabric:
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

