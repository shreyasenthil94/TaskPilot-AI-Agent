
# TaskPilot — Smart Task Planning Agent

## Project Overview
TaskPilot is a Python-based rule-driven task planning agent
that helps users prioritize tasks, allocate available time,
track completion, and regenerate schedules.

## Problem Statement
Students and individuals often struggle to manage multiple
tasks with different deadlines and priorities.

## Objectives
- Organize tasks and deadlines
- Prioritize pending work
- Allocate tasks within daily time limits
- Identify tasks that cannot be scheduled
- Support replanning after changes

## Technologies
- Python
- Streamlit

## Agent Workflow
1. Collect task details and planning constraints.
2. Identify pending tasks.
3. Sort tasks by deadline and priority.
4. Allocate tasks using the scheduling tool.
5. Display the plan and any scheduling conflicts.
6. Allow the user to update task status and replan.

## Installation
Install Python, then run:

pip install -r requirements.txt

## Run the application

streamlit run app.py

## Limitations
The prototype uses predefined rules rather than a
large language model. Tasks are kept in the current
session and are not stored in a permanent database.
The scheduler plans up to seven days ahead.

## Future Enhancements
- Persistent task storage
- Calendar integration
- Natural-language task input
- More advanced scheduling algorithms

## Author
S. Shreya 23BME1090