from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr, computed_field


class BaseDBModel(BaseModel):
    """Base model for all database entities."""
    id: int = Field(..., ge=1, example=1)
    created_at: datetime = Field(default_factory=datetime.utcnow, example="2025-02-09T12:00:00Z")
    updated_at: datetime = Field(default_factory=datetime.utcnow, example="2025-02-09T12:00:00Z")

    model_config = ConfigDict(from_attributes=True)  # Enables ORM-like behavior


class User(BaseDBModel):
    """User entity representing an application user."""
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    email: EmailStr = Field(..., example="user@example.com")
    full_name: str = Field(..., example="John Doe")

    @computed_field
    @property
    def display_name(self) -> str:
        """Compute display name from full name or fallback to username."""
        return self.full_name if self.full_name else self.username

class Log(BaseDBModel):
    """Log entity representing application logs."""
    message: str = Field(..., example="Application started successfully")
    level: str = Field(..., example="INFO")

    @computed_field
    @property
    def is_error(self) -> bool:
        """Check if log level is error."""
        return self.level.lower() == "error"
