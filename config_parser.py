import re
from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel


class Sensor(BaseModel):
    sensor_number: Optional[str] = None


class ConductivitySensor(Sensor):
    conductivity_M: Optional[float] = None
    conductivity_A: Optional[float] = None
    conductivity_B: Optional[float] = None
    conductivity_C: Optional[float] = None
    conductivity_D: Optional[float] = None
    conductivity_PCOR: Optional[float] = None
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
        return SensorBuilder(
            conductivity_M = self.conf_data[num],
            conductivity_A = self.conf_data[num + 1],
            conductivity_B = self.conf_data[num + 2],
            conductivity_C = self.conf_data[num + 3],
            conductivity_D = self.conf_data[num + 4],
            conductivity_PCOR = self.conf_data[num + 5],
            conductivity_cell_const = self.conf_data[num + 6],
            conductivity_series_r = self.conf_data[num + 7],
            conductivity_slope = self.conf_data[num + 8],
            conductivity_offset = self.conf_data[num + 9],
            conductivity_GHIJ = self.conf_data[num + 10]
        )


class FabricSensor:
    fabric = {
        0: ConductivitySensor,
        1: TemperatureSensor,
        2: PressureSensor
    }


"""
class ConfigParser:
    def __init__(self, file_config_path):
        self.file_config_path: str = file_config_path
        self.file_data: str = str()

        with (open(self.file_config_path, 'r')) as file:
            self.file_data = file.read()

    def config_parse(self) -> ConfData:
        config_data = ConfData()

        regular = r'^\d+$'
        match = re.search(regular, self.file_data)
        if match:
            config_data.conductivity_sensor_number = match[0]

            print(config_data)

        return config_data
"""
