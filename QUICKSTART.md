# 🚀 Quick Start Guide - Lazy Tourist

Get started with the AI Travel Planning Agent in minutes!

## Prerequisites

1. Python 3.9 or higher
2. OpenAI API key

## Installation (5 minutes)

### Step 1: Install Dependencies

```bash
# Install from requirements.txt (recommended)
pip install -r requirements.txt

# Or install manually
pip install langchain langchain-core langchain-openai langgraph python-dotenv streamlit
```

### Step 2: Set Up API Key

Create a `.env` file in the project root (or parent directory):

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

## Usage

### Option 1: 🎨 Streamlit Web UI (Recommended)

The easiest and most beautiful way to use Lazy Tourist:

```bash
streamlit run streamlit_app.py
```

This will open a web interface at `http://localhost:8501` with:
- 💬 Chat-like conversation
- 📄 Real-time itinerary preview
- 💡 Example queries to get started
- 📥 Download your itinerary
- 🔄 Easy reset for new trips

**Just describe your trip in the chat and start planning!**

See [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) for detailed UI guide.

### Option 2: 💻 Command Line Interactive Mode

For terminal enthusiasts:

```bash
python3 main.py
```

Then describe your dream trip in natural language!

**Example interaction:**
```
🎯 What trip would you like to plan?

> Plan a 5-day trip to Paris for 2 adults in July, budget $3,000, 
  love food and history
```

### Option 3: 🧪 Run Test Examples

Test the agent with pre-configured scenarios:

```bash
# Run all test scenarios
python3 tests/test_agent.py

# Run specific test scenarios
python3 tests/test_agent.py basic
python3 tests/test_agent.py refine
```

## What to Include in Your Query

For best results, include:

✅ **Destination**: Where you want to go
✅ **Duration**: How many days (or specific dates)
✅ **Travelers**: Number of adults and children
✅ **Budget**: Total budget in USD
✅ **Interests**: What you like (food, history, adventure, culture, etc.)

**Optional:**
- Departure city (defaults to NYC)
- Specific dates
- Hotel preferences

## Example Queries

### Budget Trip
```
"Cheap 3-day weekend in Paris for 1 person, $1000 budget, interested in museums"
```

### Romantic Getaway
```
"Romantic 4-day Bali trip for couple, $2500 budget, love beaches and sunsets"
```

### Family Vacation
```
"Week-long Tokyo adventure for 2 adults and 2 kids, $6000 budget, 
interested in culture and theme parks"
```

### Foodie Trip
```
"5-day Paris culinary experience for 2, $4000 budget, 
obsessed with French cuisine and wine"
```

## Understanding the Output

The agent will generate a comprehensive itinerary including:

📋 **Trip Overview** - Dates, budget, travelers  
✈️ **Flights** - Options with prices and timings  
🏨 **Hotels** - Recommendations with ratings and amenities  
📅 **Day-by-Day Plan** - Activities for each day  
💰 **Budget Breakdown** - Detailed cost analysis  
🌟 **Destination Tips** - Visa, safety, local customs, emergency numbers

## Saving Your Itinerary

**Interactive Mode**: You'll be asked if you want to save  
**Direct Query Mode**: Automatically saves to a markdown file

Saved files are named like: `itinerary_Paris_20231101_143022.md`

## Troubleshooting

### "ModuleNotFoundError"
Install missing packages:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install langchain langchain-openai langgraph python-dotenv streamlit
```

### "OpenAI API key not found"
Make sure your `.env` file exists and contains:
```
OPENAI_API_KEY=sk-...your-key...
```

### "No matching destination"
The agent has mocked data for:
- Paris
- Bali  
- Tokyo
- Generic destinations (will use default data)

To add more destinations, edit the mock data in `tools/` directory.

## Command Line Options

```bash
# Show help
python3 main.py --help

# Direct query
python3 main.py --query "your trip description"

# Show agent graph visualization (requires graphviz)
python3 main.py --show-graph
```

## Next Steps

1. ✅ Try the interactive mode
2. ✅ Test with different destinations and budgets
3. ✅ Review the generated markdown itineraries
4. 🔧 Customize mock data for your favorite destinations
5. 🔧 Integrate real APIs (Amadeus, Skyscanner, etc.)

## Tips for Best Results

💡 **Be specific** - More details = better itinerary  
💡 **Include interests** - Gets you relevant activities  
💡 **Set realistic budgets** - Agent will optimize within constraints  
💡 **Review and refine** - Use interactive mode to iterate

## Support

For issues or questions:
- Check the main README.md
- Review the code documentation
- Examine test_examples.py for working examples

---

**Happy Planning! 🌍✈️🏖️**

