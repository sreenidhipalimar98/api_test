
import uuid
from sqlalchemy import Column, String, DateTime, Integer, Float, Boolean, ForeignKey, NUMERIC
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# --- GLOBAL MODELS ---
class Tenant(Base):
    __tablename__ = 'tenant'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(String(128), unique=True, nullable=False)
    company_name = Column(String(128))
    logo_url = Column(String(256))
    created_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(UUID(as_uuid=True), nullable=True)

class Pipe(Base):
    __tablename__ = 'pipe'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    material = Column(String(64))
    schedule_or_class = Column(String(64))
    internal_roughness_in_inch = Column(NUMERIC(20, 10))
    size = Column(NUMERIC(10))
    nominal_size_in_imperial_value = Column(NUMERIC(30, 20))
    nominal_size_in_imperial_unit = Column(String(4))
    nominal_size_in_metric_value = Column(NUMERIC(30, 20))
    nominal_size_in_metric_unit = Column(String(2))
    wall_thickness_in_inch = Column(NUMERIC(20, 10))
    outside_diameter_in_inch = Column(NUMERIC(20, 10))
    weight_in_lb_or_ft = Column(NUMERIC(20, 10))
    created_at = Column(DateTime)
    created_by = Column(String(64))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(String(64), nullable=True)

class Component(Base):
    __tablename__ = 'component'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64))
    capacity_in_liters = Column(NUMERIC(30, 20))
    material = Column(String(64))
    description = Column(String(256))
    created_at = Column(DateTime)
    created_by = Column(String(64))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(String(64), nullable=True)

class Fitting(Base):
    __tablename__ = 'fitting'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    size = Column(Integer)
    symbol = Column(Integer)
    type = Column(String(64))
    pipe_size_in_metric_value = Column(NUMERIC(30, 20))
    pipi_size_in_metric_unit = Column(String(2))
    pipe_size_in_imperial_value = Column(NUMERIC(30, 20))
    pipe_size_in_imperial_unit = Column(String(4))
    description = Column(String(256))
    k_factor = Column(NUMERIC(10, 5))
    created_at = Column(DateTime)
    created_by = Column(String(64))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(String(64), nullable=True)

class Gas(Base):
    __tablename__ = 'gas'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64))
    formula = Column(String(64))
    temperature_in_k = Column(NUMERIC(10, 5))
    pressure_in_bar_g = Column(NUMERIC(10, 5))
    density_in_kg_or_meter_cube = Column(NUMERIC(10, 5))
    viscosity_centipoise = Column(NUMERIC(20, 10))
    specific_heat_ratio = Column(NUMERIC(20, 10))
    state = Column(String(3))
    created_at = Column(DateTime)
    created_by = Column(String(64))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(String(64), nullable=True)

class Liquid(Base):
    __tablename__ = 'liquid'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64))
    formula = Column(String(64))
    temperature_in_k = Column(NUMERIC(10, 5))
    pressure_in_bar_g = Column(NUMERIC(10, 5))
    density_in_kg_or_meter_cube = Column(NUMERIC(20, 10))
    viscosity_centipoise = Column(NUMERIC(20, 10))
    vapour_pressure_in_kpa_absolute = Column(NUMERIC(20, 10))
    state = Column(String(6))
    created_at = Column(DateTime)
    created_by = Column(String(64))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(String(64), nullable=True)

class Unit(Base):
    __tablename__ = 'unit'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64))
    symbol = Column(String(64))
    measurement_type = Column(String(64))
    created_at = Column(DateTime)
    created_by = Column(String(64))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(String(64), nullable=True)

# --- TENANT DATABASE MODELS ---
class Role(Base):
    __tablename__ = 'role'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(UUID(as_uuid=True), nullable=True)

class Permission(Base):
    __tablename__ = 'permission'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(64), unique=True)
    description = Column(String(256))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(UUID(as_uuid=True), nullable=True)

class RolePermission(Base):
    __tablename__ = 'role_permission'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.id'))
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permission.id'))
    created_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(UUID(as_uuid=True), nullable=True)

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(64))
    email = Column(String(64), unique=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('role.id'))
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(UUID(as_uuid=True), nullable=True)

class NetworkFlow(Base):
    __tablename__ = 'network_flow'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(64))
    flow_url = Column(String(256))
    is_active = Column(Boolean)
    created_at = Column(DateTime)
    created_by = Column(UUID(as_uuid=True))
    modified_at = Column(DateTime, nullable=True)
    modified_by = Column(UUID(as_uuid=True), nullable=True)
