from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field

ApiStatus = Literal["active", "deprecated", "orphaned", "zombie"]


class DiscoveryRequest(BaseModel):
    urls: List[str] = Field(default_factory=list)
    swagger_urls: List[str] = Field(default_factory=list)
    log_paths: List[str] = Field(default_factory=list)


class ApiRecord(BaseModel):
    source: str
    endpoint: str
    method: str = "GET"
    status_code: Optional[int] = None
    is_reachable: bool
    status: ApiStatus
    security: Dict[str, str]
    notes: List[str] = Field(default_factory=list)


class DiscoveryResponse(BaseModel):
    total: int
    summary: Dict[str, int]
    apis: List[ApiRecord]


class AlertItem(BaseModel):
    endpoint: str
    severity: Literal["low", "medium", "high"]
    reason: str
    recommendation: str


class AlertResponse(BaseModel):
    total: int
    alerts: List[AlertItem]
