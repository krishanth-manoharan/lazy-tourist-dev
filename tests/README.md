# Tests

This directory contains automated tests for the Lazy Tourist Travel Planning Agent.

## Unified Test Suite

All test scenarios have been consolidated into a single, comprehensive test suite for easier maintenance and execution.

### `test_agent.py`

Unified test suite covering all scenarios:
- Basic automated conversation
- Conversational refinement
- Missing information prompts
- Partial query handling

**Run All Tests:**
```bash
python tests/test_agent.py
```

**Run Specific Test:**
```bash
# Basic conversation test
python tests/test_agent.py basic

# Refinement flow test
python tests/test_agent.py refine

# Missing information test
python tests/test_agent.py missing

# Partial query test
python tests/test_agent.py partial
```

## Test Scenarios

### 1. Basic Conversation
Tests the complete flow from initial query to saved itinerary with a complete query.

### 2. Refinement Flow
Tests the agent's ability to handle user feedback and refine the itinerary based on requests.

### 3. Missing Information
Tests interactive prompting when critical information is missing from the initial query.

### 4. Partial Query
Tests handling of queries that have some information but are missing other critical fields.

## Requirements

All tests require:
- `.env` file with necessary API keys (see main README)
- All dependencies installed (`pip install -r requirements.txt`)

## Output

Tests will display:
- Progress indicators for each step
- Test results (✅ PASSED or ❌ FAILED)
- Summary of all test results
- Generated itineraries saved in the `outputs/` directory

