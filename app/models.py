from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


ServiceStatus = Literal["healthy", "degraded", "down"]
IncidentSeverity = Literal["low", "medium", "high", "critical"]


class ServiceBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., min_length=5, max_length=300)
    owner: str = Field(..., min_length=2, max_length=100)
    status: ServiceStatus


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, min_length=5, max_length=300)
    owner: Optional[str] = Field(default=None, min_length=2, max_length=100)
    status: Optional[ServiceStatus] = None


class Service(ServiceBase):
    id: int
    updated_at: datetime


class IncidentBase(BaseModel):
    service_id: int
    title: str = Field(..., min_length=3, max_length=120)
    description: str = Field(..., min_length=5, max_length=500)
    severity: IncidentSeverity
    resolved: bool = False


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=120)
    description: Optional[str] = Field(default=None, min_length=5, max_length=500)
    severity: Optional[IncidentSeverity] = None
    resolved: Optional[bool] = None


class Incident(IncidentBase):
    id: int
    created_at: datetime


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    timestamp: datetime


class SummaryResponse(BaseModel):
    total_services: int
    healthy_services: int
    degraded_services: int
    down_services: int
    open_incidents: int