from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class InputModel(BaseModel):
    model_config = ConfigDict(extra='forbid')


class TelegramAuth(InputModel):
    init_data: str = Field(min_length=1, max_length=16384)


class BookingCreate(InputModel):
    service_id: int = Field(gt=0, strict=True)
    therapist_id: int = Field(gt=0, strict=True)
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    time: str = Field(pattern=r'^\d{2}:\d{2}$')
    note: str = Field(default='', max_length=500)


class UserView(BaseModel):
    id: int
    name: str
    demo: bool


class AuthResponse(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = 'bearer'
    expires_in: int = 43200
    user: UserView


class ZoneView(BaseModel):
    id: str
    name: str


class ServiceView(BaseModel):
    id: int
    name: str
    description: str
    duration: int
    price: int
    category: str
    icon: str
    zones: list[str]


class TherapistView(BaseModel):
    id: int
    name: str
    specialty: str
    initials: str


class AvailabilityView(BaseModel):
    date: str
    timezone: str
    slots: list[str]


class BookingView(BaseModel):
    id: str
    date: str
    time: str
    end_time: str
    duration: int
    price: int
    status: Literal['confirmed', 'cancelled']
    past: bool
    started: bool
    service: str
    service_id: int
    therapist: str
    therapist_id: int
    note: str


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: list | dict | None = None


class ErrorResponse(BaseModel):
    error: ErrorDetail

