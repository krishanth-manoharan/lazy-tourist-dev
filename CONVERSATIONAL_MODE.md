# 🗣️ Lazy Tourist - User Guide

## Overview

**Lazy Tourist** is an interactive travel planning assistant that helps you create personalized itineraries through natural conversation. You can describe your trip, review the plan, request changes, and perfect your itinerary before saving it.

---

## 🚀 Quick Start

### Run the Agent

```bash
python main.py
```

That's it! The agent will guide you through the process.

---

## 💬 How It Works

### The Conversation Flow

1. **Initial Request**
   - Describe your dream trip
   - Agent creates initial itinerary

2. **Review & Refine** (Loop)
   - View the itinerary
   - Request changes
   - Ask questions
   - Agent updates based on feedback

3. **Save & Finish**
   - Say "save" when satisfied
   - Itinerary saved to `outputs/` directory

---

## 🎯 Example Conversation

```
╔══════════════════════════════════════════════════════════════╗
║           🌍 LAZY TOURIST - AI Travel Planner 🌍            ║
║              ✨ Now with Conversational Mode! ✨            ║
╚══════════════════════════════════════════════════════════════╝

✈️  Describe your dream trip: 
> Plan a 5-day trip to Paris for 2, budget $3000, love food and art

[Agent creates itinerary...]

💬 Your feedback (or 'save' to finish): 
> show me the itinerary

[Agent displays full itinerary]

💬 Your feedback (or 'save' to finish): 
> Add more food activities and find a cheaper hotel

[Agent updates itinerary with more food activities and budget hotel]

💬 Your feedback (or 'save' to finish): 
> Perfect! Save it

✅ Itinerary saved to: outputs/itinerary_Paris_20251101_143227.md

🎉 YOUR TRIP IS ALL SET!
```

---

## 📝 What You Can Say

### Viewing the Itinerary

- "show me the itinerary"
- "display the plan"
- "what do you have?"
- "let me see it"

### Requesting Changes

**Budget Adjustments:**
- "find cheaper hotels"
- "reduce the budget"
- "I need to save money"

**Activity Changes:**
- "add more food activities"
- "include museum visits"
- "I want more adventure"
- "remove the expensive activities"

**Hotel Preferences:**
- "find a luxury hotel"
- "I want a hotel near the Eiffel Tower"
- "cheaper accommodation please"

**Flight Changes:**
- "find direct flights"
- "cheaper flights"
- "I prefer morning departures"

### Asking Questions

- "What's the weather like in July?"
- "Do I need a visa?"
- "Is it safe?"
- "What should I pack?"

### Finishing

- "save"
- "looks good"
- "perfect"
- "I'm happy with this"
- "done"
- "finish"

---

## 🔧 How It Works Under the Hood

### The Agent Graph

```
Initial Request
      ↓
Extract Intent → Research Destination → Search Flights
      ↓
Search Hotels → Search Activities → Compile Itinerary
      ↓
Format Output → GET FEEDBACK ← ┐
      ↓                         │
[User satisfied?]              │
   Yes ↓        No →           │
Save & Exit    Refine ─────────┘
```

### State Management

The agent maintains conversation state including:
- Your preferences (budget, duration, interests, etc.)
- Current itinerary
- Conversation history
- Satisfaction status

### Refinement Process

When you request changes:
1. Agent analyzes your feedback
2. Extracts updated preferences (budget, duration, etc.)
3. Updates the state with new preferences
4. Determines what needs to change
5. Re-searches if needed (flights/hotels with updated criteria)
6. Or just recompiles with modifications
7. Presents updated itinerary
8. Waits for more feedback

**Note**: The agent now properly handles preference updates like budget increases, duration changes, and traveler count modifications.

---

## 💾 Output Management

### Where Files Are Saved

All itineraries are saved to the **`outputs/`** directory (not the root folder).

### File Naming

Format: `itinerary_<destination>_<timestamp>.md`

Examples:
- `itinerary_Paris_France_20251101_143227.md`
- `itinerary_Bali_20251101_143245.md`
- `itinerary_Tokyo_20251101_144530.md`

### What Gets Saved

Complete markdown itinerary including:
- Trip overview
- Flight details
- Hotel information
- Day-by-day activities
- Budget breakdown
- Destination tips

---

## 🎓 Tips for Best Results

### Be Specific

❌ **Vague:** "Make it better"
✅ **Specific:** "Add more food activities and reduce hotel cost to $150/night"

### One Request at a Time

❌ **Too Much:** "Change the hotel, flights, add activities, and reduce budget"
✅ **Focused:** "First, let's find a cheaper hotel"

### Use Natural Language

You don't need special commands - just talk naturally:
- "I think the hotel is too expensive"
- "Can we add a museum visit?"
- "This looks perfect, save it"

### Review Before Saving

Always ask to see the itinerary before saving:
1. Request: "show me the itinerary"
2. Review the full plan
3. Request changes if needed
4. Save when satisfied

---

## 🧪 Testing

### Automated Tests

```bash
# Basic flow test
python test_conversational.py basic

# Full conversational test (automated)
python test_automated_conversation.py

# Test with refinements
python test_automated_conversation.py refine

# Test missing information prompts
python test_missing_info.py
```

### Manual Testing

```bash
# Interactive mode
python main.py

# With graph visualization
python main.py --show-graph

# Show help guide
python main.py --help-guide
```

---

## ✨ Key Features

- **Interactive Feedback Loop**: Request changes, ask questions, and refine your itinerary
- **Preference Updates**: Change budget, duration, interests, and more during the conversation
- **Smart Refinement**: Agent determines whether to re-search or just adjust the itinerary
- **Conversation Memory**: Agent remembers your preferences and feedback throughout the session
- **Organized Outputs**: All itineraries saved to `outputs/` directory with timestamps

---

## 🔄 Common Workflows

### Workflow 1: Quick Accept

```
You: "Paris trip, 5 days, $3000"
Agent: [creates itinerary]
You: "save"
✅ Done!
```

### Workflow 2: Review & Refine

```
You: "Paris trip, 5 days, $3000"
Agent: [creates itinerary]
You: "show me the itinerary"
Agent: [displays itinerary]
You: "add more museums"
Agent: [updates itinerary]
You: "perfect, save"
✅ Done!
```

### Workflow 3: Multiple Iterations

```
You: "Paris trip, 5 days, $3000"
Agent: [creates itinerary]
You: "cheaper hotel please"
Agent: [updates with budget hotel]
You: "add food activities"
Agent: [adds food tours]
You: "remove the expensive dinner cruise"
Agent: [removes cruise]
You: "show me the full itinerary"
Agent: [displays updated version]
You: "looks great, save it"
✅ Done!
```

---

## 🐛 Troubleshooting

### "Agent keeps asking for feedback"

➡️ Use a save keyword: "save", "looks good", "perfect"

### "My changes aren't being applied"

➡️ Be more specific about what you want changed
➡️ Example: Instead of "better activities", say "add museum visits"

### "I want to start over"

➡️ Currently: Exit (Ctrl+C) and restart
➡️ Future: "start over" command

### "Where's my saved file?"

➡️ Check the `outputs/` directory
➡️ Files are named with destination and timestamp

---

## 🎉 Enjoy Your Planning!

The conversational mode makes travel planning interactive and fun. Take your time, refine your itinerary, and create the perfect trip!

**Happy Planning! 🌍✈️🏖️**

