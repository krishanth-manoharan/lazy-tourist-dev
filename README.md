# 🌍 Lazy Tourist - AI Travel Planning Agent

An interactive, multi-agent travel planning system that creates personalized, end-to-end travel itineraries through natural conversation using LangGraph and GPT-4o-mini.

## 🎯 Features

- **Interactive Conversation**: Describe your trip, review results, and request changes in natural dialogue
- **Iterative Refinement**: Perfect your itinerary through multiple rounds of feedback
- **Natural Language Understanding**: Describe your trip in plain English
- **Multi-Agent Architecture**: Specialized agents for different aspects of trip planning
- **Real-time Data**: Mocked flight, hotel, and activity APIs (ready for real API integration)
- **Comprehensive Itineraries**: Day-by-day plans with flights, hotels, and activities
- **Budget Tracking**: Automatic budget breakdown and optimization
- **Destination Intelligence**: Visa requirements, safety tips, local customs, and more
- **Beautiful Output**: Markdown-formatted itineraries you can save and share

## 🏗️ Architecture

The system uses **LangGraph** to orchestrate multiple specialized agents in an interactive feedback loop:

```
Initial Request
      ↓
Extract Intent ←──┐ (if more info needed)
      ↓          │
      └──────────┘
      ↓
Research Destination → Search Flights
      ↓
Search Hotels → Search Activities → Compile Itinerary
      ↓
Format Output → GET FEEDBACK (shows itinerary by default)
      ↓
[User satisfied?]
   Yes ↓        No →
Save & Exit    Refine Itinerary
                     │
              ┌──────┴──────┐
              │             │
     Needs new search   Just recompile
              │             │
              ▼             ▼
      Search Flights   Compile Itinerary
              │             │
              └──────┬──────┘
                     ↓
              Format Output
                     ↓
              GET FEEDBACK (loop)
```

### Agent Responsibilities

- **Intent Extractor**: Parses natural language, extracts preferences
- **Destination Research**: Researches visa, weather, safety, tips
- **Flight Search**: Finds optimal flight options
- **Hotel Search**: Searches accommodations
- **Activity Research**: Discovers attractions & experiences
- **Itinerary Compiler**: Compiles day-by-day plan
- **Formatter**: Creates beautiful markdown output
- **Feedback Handler**: Processes user feedback and updates preferences
- **Refinement Agent**: Applies changes based on feedback

## 📁 Project Structure

```
lazy-tourist/
├── main.py                      # Main application entry point
├── graph.py                     # LangGraph orchestration with feedback loop
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── agents/                      # Agent implementations
│   ├── __init__.py
│   ├── state.py                 # Shared state schema
│   ├── intent_extractor.py     # Parses user intent
│   ├── search_agents.py        # Flight/hotel/activity search
│   ├── itinerary_compiler.py   # Compiles final itinerary
│   └── feedback_handler.py     # Handles user feedback and refinement
│
├── tools/                       # Tool definitions with mocked APIs
│   ├── __init__.py
│   ├── flight_tools.py         # Flight search (mocked)
│   ├── hotel_tools.py          # Hotel search (mocked)
│   ├── activity_tools.py       # Activity & destination research (mocked)
│   └── itinerary_tools.py      # Itinerary management tools
│
├── outputs/                     # Saved itineraries
│
└── tests/                       # Test files
    ├── test_conversational.py  # Interactive test
    ├── test_automated_conversation.py  # Automated test
    ├── test_missing_info.py    # Test missing info prompts
    └── test_examples.py        # Example queries
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to the project directory
cd lazy-tourist

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### 3. Run the Agent

**Interactive Mode**:
```bash
python main.py
```

**With Graph Visualization**:
```bash
python main.py --show-graph
```

**Show Help Guide**:
```bash
python main.py --help-guide
```

## 💬 Example Conversation

Here's what a typical interaction looks like:

```
✈️  Describe your dream trip: Plan a 5-day trip to Paris for 2, budget $3000, love food

[Agent creates itinerary...]

💬 Your feedback (or 'save' to finish): show me the itinerary

[Agent displays full itinerary]

💬 Your feedback (or 'save' to finish): Add more food activities and find a cheaper hotel

[Agent updates itinerary with more food tours and budget hotel]

💬 Your feedback (or 'save' to finish): Perfect! Save it

✅ Itinerary saved to: outputs/itinerary_Paris_20251101_143227.md
```

### Example Queries to Start With

1. **Classic European Vacation**: "Plan a 5-day trip to Paris for 2 adults in July, budget $3,000, love food and history"
2. **Tropical Getaway**: "4-day Bali getaway for 2 people, budget $2,500, love beaches and culture"
3. **Family Adventure**: "One week Tokyo trip for family of 3 (2 adults, 1 child), budget $5,000, interested in technology and culture"
4. **Budget Trip**: "Cheap 3-day Paris trip for 1 person, $1000 budget, interested in museums"

## 📊 What You'll Get

The agent creates a comprehensive itinerary including:

- ✈️ **Flight Options**: Airlines, timings, prices, layovers
- 🏨 **Hotel Recommendations**: Star ratings, amenities, reviews, location
- 🎯 **Activities**: Day-by-day activities matching your interests
- 💰 **Budget Breakdown**: Detailed costs for flights, hotels, activities, meals
- 📍 **Destination Intel**: Visa requirements, weather, safety tips, local customs
- 📅 **Day-by-Day Plan**: Structured itinerary with timing and costs

All formatted in beautiful, shareable Markdown!

## 🛠️ Technical Details

### State Management

The system uses a `TravelState` TypedDict that flows through all agents:

```python
class TravelState(TypedDict):
    messages: List[BaseMessage]
    user_query: str
    preferences: TravelPreferences
    flights: List[FlightOption]
    hotels: List[HotelOption]
    activities: List[Activity]
    daily_itinerary: List[DayPlan]
    budget: BudgetBreakdown
    # ... more fields
```

### Mocked APIs

Currently, the tools use **mocked data** for:
- Flight searches (realistic pricing and routes)
- Hotel availability (ratings, amenities, prices)
- Activities and attractions
- Destination information

**Ready for Real Integration**: The tool interfaces are designed to easily swap mocked data with real API calls to services like:
- Amadeus API (flights & hotels)
- Skyscanner API
- Google Places API (activities)
- OpenWeather API
- And more!

### LLM Integration

Uses **gpt-4o-mini** for:
- Intent extraction from natural language
- Intelligent agent reasoning
- Natural language generation

## 🎨 Customization

### Adding New Destinations

Add data to the mock dictionaries in:
- `tools/flight_tools.py` → `MOCK_FLIGHTS`
- `tools/hotel_tools.py` → `MOCK_HOTELS`
- `tools/activity_tools.py` → `MOCK_ACTIVITIES` and destination info

### Integrating Real APIs

Replace the mocked data in tool functions with actual API calls. The tool signatures are designed to match common API patterns.

### Modifying the Agent Flow

Edit `graph.py` to change the agent orchestration, add new agents, or modify the workflow.

## 🧪 Testing

Several test files are provided:

```bash
# Automated conversation test (recommended)
python test_automated_conversation.py

# Automated test with refinements
python test_automated_conversation.py refine

# Interactive test (requires manual input)
python test_conversational.py

# Basic flow test only
python test_conversational.py basic

# Test missing information prompts
python test_missing_info.py

# View example queries
python test_examples.py
```

## 📝 Output Example

The agent generates detailed markdown itineraries like:

```markdown
# 🌍 Your Personalized Travel Itinerary
## Paris Adventure

---

## 📋 Trip Overview
**Destination:** Paris
**Dates:** 2025-07-15 to 2025-07-20
**Duration:** 5 days
**Travelers:** 2 adults, 0 children
**Budget:** $3000

## ✈️ Flight Details
**Outbound Flight:**
- Airline: Air France AF007
- Route: JFK → CDG
- Price: $1,300 ($650/person)
...
```

## 🔧 Dependencies

- **langchain**: Framework for LLM applications
- **langgraph**: State machine for multi-agent systems
- **langchain-openai**: OpenAI integration
- **python-dotenv**: Environment variable management

## 🤝 Contributing

This is a demonstration project. To extend it:

1. Add more destinations to the mock data
2. Integrate real APIs (Amadeus, Skyscanner, etc.)
3. Add more agent types (car rental, restaurant booking, etc.)
4. Enhance the feedback loop with more sophisticated preference updates
5. Add support for multi-city trips
6. Implement conversation memory across sessions

## 📄 License

This project is for educational and demonstration purposes.

## 🎉 Acknowledgments

Built with:
- LangGraph for multi-agent orchestration
- OpenAI GPT-4o-mini for intelligent reasoning
- LangChain for LLM application framework

---

**Happy Travels! 🌍✈️🏖️**

