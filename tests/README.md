# Tests

This directory contains automated tests for the Lazy Tourist Travel Planning Agent.

## Available Tests

### `test_automated_conversation.py`
Automated tests with mocked user inputs for conversational flow.

**Run:**
```bash
# Basic automated conversation test
python tests/test_automated_conversation.py

# Test with refinement flow
python tests/test_automated_conversation.py refine
```

### `test_conversational.py`
Interactive and basic flow tests.

**Run:**
```bash
# Interactive test (requires manual input)
python tests/test_conversational.py

# Automated basic flow test
python tests/test_conversational.py basic
```

### `test_missing_info.py`
Tests the agent's ability to prompt for missing information.

**Run:**
```bash
python tests/test_missing_info.py
```

## Running All Tests

To run all automated tests sequentially:

```bash
cd lazy-tourist
python tests/test_automated_conversation.py && \
python tests/test_conversational.py basic && \
python tests/test_missing_info.py
```

## Requirements

All tests require:
- `.env` file with necessary API keys (see main README)
- All dependencies installed (`pip install -r requirements.txt`)

