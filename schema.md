
# TaskPilot — Agent Schema

## 1. Input
The user provides:
- Task name
- Deadline
- Priority (High, Medium, Low)
- Estimated duration
- Available hours per day

## 2. Agent
The TaskPilot planning agent:
- Observes the task list
- Identifies pending tasks
- Decides task order using deadline and priority
- Calls the scheduling tool
- Checks whether tasks fit within time limits
- Reports unscheduled tasks

## 3. Tools
- prioritize_tasks(): sorts pending tasks
- create_schedule(): assigns tasks to available days
- run_agent(): coordinates planning and returns the result

## 4. State / Memory
The application keeps task details and completion status
in the current Streamlit session.

## 5. Output
- Scheduled task list
- Assigned dates and hours
- Unscheduled task warnings
- Updated plan after replanning

## 6. Feedback Loop
When a task is marked complete or planning constraints
change, the user can generate a revised schedule.