from datetime import datetime
from pydantic import BaseModel, Field, validator
from common.variables import MAX_EVENT_NAME_LENGTH, MAX_GROUP_LENGTH, MIN_AGE, MAX_AGE

class EventSchema(BaseModel):
    set_event_type: str
    set_event_name: str = Field(min_length=1, max_length=MAX_EVENT_NAME_LENGTH)
    set_event_date: str # Will be validated as date string initially

    @validator('set_event_date')
    def validate_event_date(cls, v):
        try:
            return datetime.strptime(v, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError('Дата мероприятия должна быть в формате ДД.ММ.ГГГГ')

class UserRegistrationSchema(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    group: str = Field(min_length=1, max_length=MAX_GROUP_LENGTH)
    age: int = Field(ge=MIN_AGE, le=MAX_AGE)

class SubmissionSchema(BaseModel):
    subm_text: str = Field(min_length=1)
    subm_date: str # Will be validated as date string initially

    @validator('subm_date')
    def validate_subm_date(cls, v):
        try:
            return datetime.strptime(v, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError('Дата заявки должна быть в формате ДД.ММ.ГГГГ')
