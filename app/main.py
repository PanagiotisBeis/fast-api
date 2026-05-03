from datetime import datetime
from typing import List

from fastapi import FastAPI, HTTPException, Query

from app.data import incidents, services
from app.models import (
    HealthResponse,
    Incident,
    IncidentCreate,
    IncidentUpdate,
    Service,
    ServiceCreate,
    ServiceUpdate,
    SummaryResponse,
)

APP_VERSION = "1.0.0"

app = FastAPI(
    title="Service Status API",
    description="A simple FastAPI application for service health and incident tracking.",
    version=APP_VERSION,
)


def get_service_or_404(service_id: int) -> dict:
    for service in services:
        if service["id"] == service_id:
            return service
    raise HTTPException(status_code=404, detail="Service not found")


def get_incident_or_404(incident_id: int) -> dict:
    for incident in incidents:
        if incident["id"] == incident_id:
            return incident
    raise HTTPException(status_code=404, detail="Incident not found")


@app.get("/", tags=["Root"])
def root() -> dict:
    return {
        "message": "Service Status API is running",
        "docs": "/docs",
        "version": APP_VERSION,
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="service-status-api",
        version=APP_VERSION,
        timestamp=datetime.utcnow(),
    )


@app.get("/summary", response_model=SummaryResponse, tags=["Summary"])
def get_summary() -> SummaryResponse:
    healthy = sum(1 for service in services if service["status"] == "healthy")
    degraded = sum(1 for service in services if service["status"] == "degraded")
    down = sum(1 for service in services if service["status"] == "down")
    open_incidents = sum(1 for incident in incidents if not incident["resolved"])

    return SummaryResponse(
        total_services=len(services),
        healthy_services=healthy,
        degraded_services=degraded,
        down_services=down,
        open_incidents=open_incidents,
    )


@app.get("/services", response_model=List[Service], tags=["Services"])
def list_services(
    status: str | None = Query(default=None, description="Filter by service status")
) -> List[Service]:
    if status is None:
        return [Service(**service) for service in services]

    filtered = [service for service in services if service["status"] == status]
    return [Service(**service) for service in filtered]


@app.get("/services/{service_id}", response_model=Service, tags=["Services"])
def get_service(service_id: int) -> Service:
    service = get_service_or_404(service_id)
    return Service(**service)


@app.post("/services", response_model=Service, status_code=201, tags=["Services"])
def create_service(payload: ServiceCreate) -> Service:
    new_id = max((service["id"] for service in services), default=0) + 1
    new_service = {
        "id": new_id,
        "name": payload.name,
        "description": payload.description,
        "owner": payload.owner,
        "status": payload.status,
        "updated_at": datetime.utcnow(),
    }
    services.append(new_service)
    return Service(**new_service)


@app.put("/services/{service_id}", response_model=Service, tags=["Services"])
def update_service(service_id: int, payload: ServiceUpdate) -> Service:
    service = get_service_or_404(service_id)

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    for key, value in update_data.items():
        service[key] = value

    service["updated_at"] = datetime.utcnow()
    return Service(**service)


@app.delete("/services/{service_id}", status_code=204, tags=["Services"])
def delete_service(service_id: int) -> None:
    service = get_service_or_404(service_id)
    services.remove(service)


@app.get("/incidents", response_model=List[Incident], tags=["Incidents"])
def list_incidents(
    resolved: bool | None = Query(default=None, description="Filter by resolved status")
) -> List[Incident]:
    if resolved is None:
        return [Incident(**incident) for incident in incidents]

    filtered = [incident for incident in incidents if incident["resolved"] == resolved]
    return [Incident(**incident) for incident in filtered]


@app.get("/incidents/{incident_id}", response_model=Incident, tags=["Incidents"])
def get_incident(incident_id: int) -> Incident:
    incident = get_incident_or_404(incident_id)
    return Incident(**incident)


@app.post("/incidents", response_model=Incident, status_code=201, tags=["Incidents"])
def create_incident(payload: IncidentCreate) -> Incident:
    get_service_or_404(payload.service_id)

    new_id = max((incident["id"] for incident in incidents), default=0) + 1
    new_incident = {
        "id": new_id,
        "service_id": payload.service_id,
        "title": payload.title,
        "description": payload.description,
        "severity": payload.severity,
        "resolved": payload.resolved,
        "created_at": datetime.utcnow(),
    }
    incidents.append(new_incident)
    return Incident(**new_incident)


@app.put("/incidents/{incident_id}", response_model=Incident, tags=["Incidents"])
def update_incident(incident_id: int, payload: IncidentUpdate) -> Incident:
    incident = get_incident_or_404(incident_id)

    update_data = payload.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    for key, value in update_data.items():
        incident[key] = value

    return Incident(**incident)


@app.delete("/incidents/{incident_id}", status_code=204, tags=["Incidents"])
def delete_incident(incident_id: int) -> None:
    incident = get_incident_or_404(incident_id)
    incidents.remove(incident)