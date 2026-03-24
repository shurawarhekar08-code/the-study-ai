# ==============================================================
#  planner.py  —  Weekly Study Plan Generator
# ==============================================================
#  Distributes subjects evenly across 7 days using a
#  round-robin rotation. Each session = 1 hour.
# ==============================================================

import math

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Subject-specific study tips
TIPS: dict[str, str] = {
    "math":      "Work through at least 5 practice problems.",
    "science":   "Draw diagrams to visualise key processes.",
    "history":   "Build a timeline of major events.",
    "english":   "Read one article and write a brief summary.",
    "biology":   "Use flashcards for terminology.",
    "physics":   "Solve numericals step-by-step.",
    "chemistry": "Balance equations aloud as you write them.",
    "geography": "Study maps alongside your written notes.",
    "computer":  "Code along — don't just read the examples.",
    "economics": "Anchor theory to real-world examples.",
    "literature":"Annotate key passages before class.",
    "language":  "Speak out loud for 10 minutes every session.",
}

DEFAULT_TIP = "Review your last session's notes before starting."


def _get_tip(subject: str) -> str:
    """Returns a study tip matched to the subject name."""
    sl = subject.lower()
    for key, tip in TIPS.items():
        if key in sl:
            return tip
    return DEFAULT_TIP


def generate_study_plan(subjects: list[str], hours_per_day: int) -> dict:
    """
    Builds a 7-day study timetable.

    Args:
        subjects:      List of subject names.
        hours_per_day: Study hours per day (1–8).

    Returns:
        Dict keyed by day name, each value a list of session dicts.

    Example return value:
        {
            "Monday": [
                {"subject": "Math", "duration": "1 hour",
                 "tip": "Work through at least 5 practice problems."}
            ],
            ...
        }
    """
    hours_per_day = max(1, min(8, hours_per_day))
    plan: dict    = {day: [] for day in DAYS}

    if not subjects:
        return plan

    # Create enough subjects to fill every slot (round-robin)
    total_slots   = hours_per_day * 7
    repeats       = math.ceil(total_slots / len(subjects))
    subject_cycle = (subjects * repeats)[:total_slots]

    slot = 0
    for day in DAYS:
        for _ in range(hours_per_day):
            subj = subject_cycle[slot]
            plan[day].append({
                "subject":  subj,
                "duration": "1 hour",
                "tip":      _get_tip(subj),
            })
            slot += 1

    return plan
