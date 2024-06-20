import re
from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel


class ConfData(BaseModel):
    conductivity_sensor_number: Optional[str] = None
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

    temperature_sensor_number: Optional[str] = None
    temperature_F0: Optional[float] = None
    temperature_A: Optional[float] = None
    temperature_B: Optional[float] = None
    temperature_C: Optional[float] = None
    temperature_D: Optional[float] = None
    temperature_slope: Optional[float] = None
    temperature_offset: Optional[float] = None
    temperature_GHIJ: Optional[float] = None

    pressure_sensor_number: Optional[str] = None
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


class ConfigParser:
    def __init__(self, file_config_path):
        self.file_config_path: str = file_config_path
        self.file_data: str = str()

        with (open(self.file_config_path, 'r')) as file:
            self.file_data = file.read()

    def config_parse(self) -> ConfData:
        config_data = ConfData()

        return config_data
