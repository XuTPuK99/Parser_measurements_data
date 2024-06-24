from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class Sensor(BaseModel):
    sensor_number: Optional[str] = None


class ConductivitySensor(Sensor):
    conductivity_M: Optional[float] = None
    conductivity_A: Optional[float] = None
    conductivity_B: Optional[float] = None
    conductivity_C: Optional[float] = None
    conductivity_D: Optional[float] = None
    conductivity_CPCOR: Optional[float] = None
    conductivity_cell_const: Optional[float] = None
    conductivity_series_r: Optional[float] = None
    conductivity_slope: Optional[float] = None
    conductivity_offset: Optional[float] = None
    conductivity_GHIJ: Optional[float] = None


class TemperatureSensor(Sensor):
    temperature_F0: Optional[float] = None
    temperature_A: Optional[float] = None
    temperature_B: Optional[float] = None
    temperature_C: Optional[float] = None
    temperature_D: Optional[float] = None
    temperature_slope: Optional[float] = None
    temperature_offset: Optional[float] = None
    temperature_GHIJ: Optional[float] = None


class PressureSensor(Sensor):
    pressure_T1: Optional[float] = None
    pressure_T2: Optional[float] = None
    pressure_T3: Optional[float] = None
    pressure_T4: Optional[float] = None
    pressure_C1: Optional[float] = None
    pressure_C2: Optional[float] = None
    pressure_C3: Optional[float] = None
    pressure_C4: Optional[float] = None
    pressure_D1: Optional[float] = None
    pressure_D2: Optional[float] = None
    pressure_slope: Optional[float] = None
    pressure_offset: Optional[float] = None
    pressure_sensor_type: Optional[float] = None
    pressure_AD590_M: Optional[float] = None
    pressure_AD590_B: Optional[float] = None


class SensorBuilder:
    def __init__(self, conf_data):
        self.conf_data = conf_data


class ConductivitySensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        split_string_2 = self.conf_data[num + 2].split(' ')
        return ConductivitySensor(
            conductivity_sensor_number=self.conf_data[num],
            conductivity_M=split_string_1[0],
            conductivity_A=split_string_1[1],
            conductivity_B=split_string_1[2],
            conductivity_C=split_string_1[3],
            conductivity_D=split_string_1[4],
            conductivity_CPCOR=split_string_1[5],
            conductivity_cell_const=split_string_2[0],
            conductivity_series_r=split_string_2[1],
            conductivity_slope=split_string_2[2],
            conductivity_offset=split_string_2[3],
            conductivity_GHIJ=split_string_2[4]
        )


class TemperatureSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        return TemperatureSensor(
            temperature_sensor_number=self.conf_data[num],
            temperature_F0=split_string_1[0],
            temperature_A=split_string_1[1],
            temperature_B=split_string_1[2],
            temperature_C=split_string_1[3],
            temperature_D=split_string_1[4],
            temperature_slope=split_string_1[5],
            temperature_offset=split_string_1[6],
            temperature_GHIJ=split_string_1[7]
        )


class PressureSensorBuilder(SensorBuilder):
    def get(self, num):
        split_string_1 = self.conf_data[num + 1].split(' ')
        split_string_2 = self.conf_data[num + 2].split(' ')
        split_string_3 = self.conf_data[num + 3].split(' ')
        return PressureSensor(
            pressure_sensor_number=self.conf_data[num],
            pressure_T1=split_string_1[0],
            pressure_T2=split_string_1[1],
            pressure_T3=split_string_1[2],
            pressure_T4=split_string_1[3],
            pressure_T5=split_string_1[4],
            pressure_C1=split_string_2[0],
            pressure_C2=split_string_2[1],
            pressure_C3=split_string_2[2],
            pressure_C4=split_string_2[3],
            pressure_D1=split_string_3[0],
            pressure_D2=split_string_3[1],
            pressure_slope=split_string_3[2],
            pressure_offset=split_string_3[3],
            pressure_sensor_type=split_string_3[4],
            pressure_AD590_M=split_string_3[5],
            pressure_AD590_B=split_string_3[6]
        )


class FabricSensor:
    fabric = {
        0: ConductivitySensor,
        3: TemperatureSensor,
        10: PressureSensor
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
            print(config_file_data)

        for i in range(len(config_file_data)):
            entity = fabric.get(i, config_file_data)
            print(entity)

