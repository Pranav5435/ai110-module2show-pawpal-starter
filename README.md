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

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Today's Schedule
====================
- 07:30 | Feed breakfast | Priority: medium | Duration: 15 min
- 08:00 | Morning walk | Priority: high | Duration: 30 min
- 19:00 | Evening playtime | Priority: high | Duration: 45 min
Conflicts:
- None
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
============================= test session starts ==============================
platform darwin -- Python 3.13.5, pytest-8.3.4, pluggy-1.5.0
rootdir: /Users/pranavkishore/ai110-module2show-pawpal-starter
plugins: anyio-4.13.0
collected 17 items

tests/test_pawpal.py .................                                   [100%]

============================== 17 passed in 0.01s ==============================
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_by_time() | Sorts by time, then priority, then description |
| Filtering | filter_tasks() | Filters by completion status or pet name |
| Conflict handling | detect_conflicts() | Flags overlapping tasks using duration |
| Recurring tasks | handle_recurrence() | Creates next occurrence when task is marked complete |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Enter owner name and add a pet with a name and species
2. Select the pet and add tasks with title, duration, priority, and time
3. Click Generate Schedule to see tasks sorted chronologically
4. Conflict warnings appear if two tasks overlap
5. Mark a recurring task complete to generate the next occurrence



**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
