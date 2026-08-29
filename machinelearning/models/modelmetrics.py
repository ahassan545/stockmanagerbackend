from pydantic import BaseModel

class ModelR2(BaseModel):        
    name: str
    r_2: float

class ModelMetrics(BaseModel):
    r_2: list[ModelR2] = []
