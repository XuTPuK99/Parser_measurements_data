import re
from datetime import datetime
from typing import Optional, Union, List
from pydantic import BaseModel


class ConfData(BaseModel):
    conductivity_sensor_number: Optional[int] = None
    conductivity_data: Optional[List[float]] = None
    #conductivity_co
