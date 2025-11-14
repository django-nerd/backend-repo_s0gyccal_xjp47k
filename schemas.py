"""
Database Schemas for Ulin (Homestay & Tour Packages)

Each Pydantic model maps to a MongoDB collection using its lowercase class name.
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class Customer(BaseModel):
    name: str = Field(..., description="Full name of the customer")
    email: str = Field(..., description="Email of the customer")
    phone: Optional[str] = Field(None, description="Phone number")

class Homestay(BaseModel):
    name: str = Field(..., description="Homestay name")
    location: str = Field(..., description="City/Area")
    description: Optional[str] = Field(None, description="Description")
    price_per_night: float = Field(..., ge=0, description="Price per night")
    max_guests: int = Field(..., ge=1, description="Maximum number of guests")
    amenities: List[str] = Field(default_factory=list, description="Amenities list")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    rating: Optional[float] = Field(0.0, ge=0, le=5, description="Average rating")

class Package(BaseModel):
    title: str = Field(..., description="Package title")
    location: str = Field(..., description="Destination area")
    description: Optional[str] = Field(None, description="What’s included")
    price: float = Field(..., ge=0, description="Package price")
    duration_days: int = Field(..., ge=1, description="Duration in days")
    highlights: List[str] = Field(default_factory=list, description="Highlights/Itinerary points")
    images: List[str] = Field(default_factory=list, description="Image URLs")
    rating: Optional[float] = Field(0.0, ge=0, le=5, description="Average rating")

class Booking(BaseModel):
    type: str = Field(..., description="booking type: homestay | package")
    item_id: str = Field(..., description="ID of homestay or package")
    customer_name: str = Field(...)
    customer_email: str = Field(...)
    customer_phone: Optional[str] = None
    guests: Optional[int] = Field(1, ge=1)
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    travel_date: Optional[str] = None
    note: Optional[str] = None
