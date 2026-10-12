
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="TaskPilot AI Agent",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 TaskPilot")
st.subheader("Smart Task Planning Agent")
st.write(
    "Add your tasks and let TaskPilot prioritize, schedule, "
    "track, and replan your work."
)

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "last_plan" not in st.session_state:
    st.session_state.last_plan = []

PRIORITY_RANK = {"High": 0, "Medium": 1, "Low": 2}


# TOOL 1: Prioritize pending tasks
def prioritize_tasks(tasks):
    pending = [t for t in tasks if not t["completed"]]
    return sorted(
        pending,
        key=lambda t: (
            t["due_date"],
            PRIORITY_RANK[t["priority"]]
        )
    )


# TOOL 2: Create a schedule within daily time limits
def create_schedule(tasks, hours_per_day):
    ordered_tasks = prioritize_tasks(tasks)
    daily_load = {}
    schedule = []
    unscheduled = []

    for task in ordered_tasks:
        assigned = False

        for offset in range(8):
            day = date.today() + timedelta(days=offset)

            if day > task["due_date"]:
                break

            used = daily_load.get(day, 0)
            if used + task["hours"] <= hours_per_day:
                daily_load[day] = used + task["hours"]
                schedule.append({
                    "task": task["title"],
                    "date": day,
                    "hours": task["hours"],
                    "priority": task["priority"]
                })
                assigned = True
                break

        if not assigned:
            unscheduled.append(task["title"])

    return schedule, unscheduled


# AGENT: Observe the tasks, decide, use tools, and report
def run_agent(tasks, hours_per_day):
    pending = [t for t in tasks if not t["completed"]]

    if not pending:
        return [], [], "All tasks are complete!"

    plan, unscheduled = create_schedule(tasks, hours_per_day)

    if unscheduled:
        message = (
            "Plan created, but some tasks need more time "
            "or an earlier deadline."
        )
    else:
        message = (
            "Plan created successfully. Tasks are scheduled "
            "within your daily time limit."
        )

    return plan, unscheduled, message


st.sidebar.header("Planning Settings")
hours_per_day = st.sidebar.slider(
    "Available study/work hours per day",
    min_value=1,
    max_value=12,
    value=4
)

st.header("1. Add a task")

with st.form("add_task_form", clear_on_submit=True):
    title = st.text_input("Task name", placeholder="Finish assignment")
    due_date = st.date_input("Deadline", value=date.today())
    priority = st.selectbox(
        "Priority", ["High", "Medium", "Low"]
    )
    hours = st.number_input(
        "Estimated hours needed",
        min_value=1,
        max_value=12,
        value=2
    )
    add_task = st.form_submit_button("Add Task")

    if add_task:
        if not title.strip():
            st.error("Please enter a task name.")
        elif due_date < date.today():
            st.error("Choose today or a future deadline.")
        else:
            st.session_state.tasks.append({
                "title": title.strip(),
                "due_date": due_date,
                "priority": priority,
                "hours": int(hours),
                "completed": False
            })
            st.session_state.last_plan = []
            st.success("Task added!")

st.header("2. Manage your tasks")

if not st.session_state.tasks:
    st.info("Add your first task to get started.")
else:
    for i, task in enumerate(st.session_state.tasks):
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.write(f"**{task['title']}**")
                st.caption(
                    f"Deadline: {task['due_date']} | "
                    f"Priority: {task['priority']} | "
                    f"Duration: {task['hours']} hour(s)"
                )

            with right:
                checked = st.checkbox(
                    "Completed",
                    value=task["completed"],
                    key=f"done_{i}"
                )
                if checked != task["completed"]:
                    task["completed"] = checked
                    st.session_state.last_plan = []

    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        st.session_state.last_plan = []
        st.rerun()

st.header("3. Run the AI planning agent")

if st.button("Generate / Replan Schedule", type="primary"):
    plan, unscheduled, message = run_agent(
        st.session_state.tasks, hours_per_day
    )
    st.session_state.last_plan = plan
    st.session_state.unscheduled = unscheduled
    st.session_state.agent_message = message

if st.session_state.last_plan or (
    "agent_message" in st.session_state
):
    st.success(st.session_state.agent_message)

    if st.session_state.last_plan:
        st.subheader("Your schedule")
        st.dataframe(
            [
                {
                    "Task": item["task"],
                    "Scheduled Date": str(item["date"]),
                    "Hours": item["hours"],
                    "Priority": item["priority"]
                }
                for item in st.session_state.last_plan
            ],
            use_container_width=True,
            hide_index=True
        )

    if st.session_state.get("unscheduled"):
        st.warning("These tasks could not be scheduled:")
        for item in st.session_state.unscheduled:
            st.write(f"- {item}")

st.caption(
    "TaskPilot uses a transparent rule-based planning algorithm. "
    "It is a prototype and does not guarantee task completion."
)