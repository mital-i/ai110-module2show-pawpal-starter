# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The PawPal+ scheduler now includes advanced features for efficient pet care planning:

- **Time-based Sorting**: Tasks are sorted by preferred time slots (morning/afternoon/evening) using datetime parsing for accurate chronological ordering.
- **Flexible Filtering**: Filter tasks by pet name or completion status to focus on specific needs or incomplete items.
- **Recurring Task Management**: Daily and weekly tasks automatically generate new instances for the next occurrence when completed, using timedelta for precise date calculations.
- **Conflict Detection**: Lightweight detection of scheduling overlaps within the same pet or across different pets, returning warnings without crashing the program.

These enhancements make the app more practical for multi-pet households and busy owners.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Testing PawPal+

- Run tests using the command
  `python -m pytest tests/test_pawpal.py -v`
- Confidence level: 4-5 out 5

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
