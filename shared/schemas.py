
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class TenantBase(BaseModel):
    tenant_id: str
    company_name: str
    logo_url: Optional[str]

class TenantCreate(TenantBase):
    pass

class TenantOut(TenantBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr
    # role_id: uuid.UUID

class UserCreate(UserBase):
    pass

class UserOut(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Pipe
class PipeBase(BaseModel):
    material: str
    schedule_or_class: str
    internal_roughness_in_inch: float
    size: int
    nominal_size_in_imperial_value: float
    nominal_size_in_imperial_unit: str
    nominal_size_in_metric_value: float
    nominal_size_in_metric_unit: str
    wall_thickness_in_inch: float
    outside_diameter_in_inch: float
    weight_in_lb_or_ft: float

class PipeCreate(PipeBase):
    pass

class PipeOut(PipeBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Component
class ComponentBase(BaseModel):
    name: str
    capacity_in_liters: float
    material: str
    description: Optional[str]

class ComponentCreate(ComponentBase):
    pass

class ComponentOut(ComponentBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Fitting
class FittingBase(BaseModel):
    size: int
    symbol: int
    type: str
    pipe_size_in_metric_value: float
    pipi_size_in_metric_unit: str
    pipe_size_in_imperial_value: float
    pipe_size_in_imperial_unit: str
    description: str
    k_factor: float

class FittingCreate(FittingBase):
    pass

class FittingOut(FittingBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Gas
class GasBase(BaseModel):
    name: str
    formula: str
    temperature_in_k: float
    pressure_in_bar_g: float
    density_in_kg_or_meter_cube: float
    viscosity_centipoise: float
    specific_heat_ratio: float
    state: str

class GasCreate(GasBase):
    pass

class GasOut(GasBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Liquid
class LiquidBase(BaseModel):
    name: str
    formula: str
    temperature_in_k: float
    pressure_in_bar_g: float
    density_in_kg_or_meter_cube: float
    viscosity_centipoise: float
    vapour_pressure_in_kpa_absolute: float
    state: str

class LiquidCreate(LiquidBase):
    pass

class LiquidOut(LiquidBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Unit
class UnitBase(BaseModel):
    name: str
    symbol: str
    measurement_type: str

class UnitCreate(UnitBase):
    pass

class UnitOut(UnitBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Role
class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# Permission
class PermissionBase(BaseModel):
    code: str
    description: Optional[str]

class PermissionCreate(PermissionBase):
    pass

class PermissionOut(PermissionBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# RolePermission
class RolePermissionBase(BaseModel):
    role_id: uuid.UUID
    permission_id: uuid.UUID

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermissionOut(RolePermissionBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True

# NetworkFlow
class NetworkFlowBase(BaseModel):
    name: str
    flow_url: str
    is_active: Optional[bool] = True

class NetworkFlowCreate(NetworkFlowBase):
    pass

class NetworkFlowOut(NetworkFlowBase):
    id: uuid.UUID
    created_at: Optional[datetime]
    class Config:
        orm_mode = True
