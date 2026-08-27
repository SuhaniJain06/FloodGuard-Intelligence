from typing import Optional, List
from pydantic import BaseModel, Field


class Location(BaseModel):
    text: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class People(BaseModel):
    total: Optional[str] = None
    children: Optional[str] = None
    elderly: Optional[str] = None
    pregnant: Optional[str] = None
    injured: Optional[str] = None
    missing: Optional[str] = None
    deceased: Optional[str] = None
    mobility_impaired: Optional[str] = None


class Request(BaseModel):
    type: Optional[str] = None
    resources: List[str] = Field(default_factory=list)


class Needs(BaseModel):
    food: bool = False
    water: bool = False
    medicine: bool = False
    shelter: bool = False
    rescue: bool = False
    medical_transfer: bool = False


class SOSIncident(BaseModel):
    incident_id: str
    source_type: str

    location: Location
    people: People

    situation: Optional[str] = None

    request: Request
    needs: Needs

    contact_info: List[str] = Field(default_factory=list)

    original_message: str