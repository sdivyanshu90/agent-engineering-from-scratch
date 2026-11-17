"""Optional installed-extra comparison after first-principles validation."""
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,field_validator


class IssueOutput(BaseModel):
    model_config=ConfigDict(strict=True,extra='forbid')
    category: Literal['bug','feature','question']
    summary: str=Field(min_length=1,max_length=120)
    urgent: bool

    @field_validator('summary')
    @classmethod
    def nonblank(cls,value):
        if not value.strip():raise ValueError('blank summary')
        return value
