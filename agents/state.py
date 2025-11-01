"""State schema for the Travel Planning Agent"""
from typing import TypedDict, List, Dict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class TravelPreferences(TypedDict, total=False):
    """User preferences extracted from query"""
    origin: str
    destination: str
    departure_date: str
    return_date: str
    duration_days: int
    num_adults: int
    num_children: int
    total_passengers: int
    budget: int
    interests: List[str]
    accommodation_preference: str
    min_hotel_stars: int

class FlightOption(TypedDict, total=False):
    """Flight option details"""
    airline: str
    flight_number: str
    departure: str
    arrival: str
    duration: str
    price: int
    total_price: int
    stops: int
    departure_time: str
    arrival_time: str
    layover: str

class HotelOption(TypedDict, total=False):
    """Hotel option details"""
    name: str
    stars: int
    price_per_night: int
    total_price: int
    location: str
    rating: float
    reviews: int
    amenities: List[str]
    distance_to_center: str
    nights: int

class Activity(TypedDict, total=False):
    """Activity/attraction details"""
    name: str
    category: str
    duration: str
    price: int
    rating: float
    description: str
    best_time: str
    day: int

class DayPlan(TypedDict, total=False):
    """Single day itinerary"""
    day: int
    date: str
    activities: List[Activity]
    estimated_cost: int
    notes: str

class BudgetBreakdown(TypedDict, total=False):
    """Budget breakdown"""
    flights: int
    accommodation: int
    activities: int
    meals: int
    transportation: int
    miscellaneous: int
    total: int
    remaining: int

class TravelState(TypedDict):
    """Main state that flows through the agent graph"""
    messages: Annotated[Sequence[BaseMessage], add_messages]
    user_query: str
    preferences: TravelPreferences
    flights: List[FlightOption]
    return_flights: List[FlightOption]
    hotels: List[HotelOption]
    activities: List[Activity]
    destination_info: Dict
    daily_itinerary: List[DayPlan]
    budget: BudgetBreakdown
    selected_flight: FlightOption
    selected_return_flight: FlightOption
    selected_hotel: HotelOption
    next_step: str
    final_itinerary: str
    needs_user_input: bool
    iteration_count: int
    user_satisfied: bool
    feedback_message: str
    conversation_history: List[str]
    show_itinerary: bool  # Flag to control when to show itinerary in feedback loop
    assistant_response: str  # Store assistant's clarification/response message
    user_feedback_input: str  # User feedback input collected in main.py

