import streamlit as st
import pandas as pd
import sys
import os
######

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import get_connection
from src.bottleneck_analysis import get_pending_approvals
from src.approval_requests import approve_task, request_approval
from src.task_status import update_status
from src.task_assignment import assign_task
from src.suggestions import generate_suggestions

st.set_page_config(layout="wide")
st.title("🧠 Task Bottleneck & Approval Tracking System")

# =====================================================
# ROLE SELECTION (ONE LINK, TWO ROLES)
# =====================================================
st.sidebar.title("Role Selection")
role = st.sidebar.selectbox("Select Role", ["Employee", "Manager"])

conn = get_connection()

# =====================================================
# EMPLOYEE VIEW (UNCHANGED)
# =====================================================
if role == "Employee":
    st.header("👨‍💻 Employee Portal")

    emp_id = st.selectbox(
        "Select Your Employee ID",
        ["E01", "E02", "E03", "E04", "E05"]
    )

    tasks = pd.read_sql(
        f"SELECT * FROM task_assignment WHERE employee_id='{emp_id}'",
        conn
    )

    st.subheader("📋 Your Assigned Tasks")
    st.dataframe(tasks)

    if not tasks.empty:
        task_id = st.selectbox("Select Task ID", tasks["task_id"])

        new_status = st.selectbox(
            "Update Status",
            ["IN_PROGRESS", "WAITING_FOR_APPROVAL", "COMPLETED"]
        )

        if st.button("Update Task Status"):
            update_status(task_id, new_status)
            st.success("Task status updated successfully")

        if new_status == "WAITING_FOR_APPROVAL":
            st.subheader("📝 Raise Approval Request")

            reason = st.selectbox(
                "Reason for Wait",
                [
                    "Software license pending",
                    "Tool access pending",
                    "Data access pending",
                    "Client approval pending"
                ]
            )

            if st.button("Submit Approval Request"):
                request_approval(task_id, emp_id, "ADMIN01", reason)
                st.warning("Approval request submitted")

    else:
        st.info("No tasks assigned yet.")

# =====================================================
# MANAGER VIEW
# =====================================================
elif role == "Manager":
    st.header("👨‍💼 Manager Dashboard")

    tab = st.sidebar.radio(
        "Navigation",
        ["Task Assignment", "Task Status", "Approval Requests"]
    )

    # ---------------- TAB 1: TASK ASSIGNMENT (FINAL FIX) ----------------
    if tab == "Task Assignment":

        # 1️⃣ ASSIGN NEW TASK (TOP - TOGGLE)
        with st.expander("➕ Assign New Task", expanded=False):

            task_id = st.number_input("Task ID", min_value=100)
            title = st.text_input("Task Title")

            employee = st.selectbox(
                "Assign To Employee",
                ["E01", "E02", "E03", "E04", "E05"]
            )

            deadline = st.date_input("Deadline")
            priority = st.selectbox("Priority", ["Low", "Medium", "High"])

            if st.button("Assign Task"):
                assign_task(
                    task_id,
                    title,
                    "ADMIN01",
                    employee,
                    str(deadline),
                    priority
                )
                st.success("Task assigned successfully. Refresh to see updates.")

        st.divider()

        # 2️⃣ ASSIGNED TASKS TABLE (MIDDLE)
        st.subheader("📋 Tasks Assigned to Employees")

        df = pd.read_sql("SELECT * FROM task_assignment", conn)
        st.dataframe(df)

        st.divider()

        # 3️⃣ VISUALIZATION (BOTTOM)
        st.subheader("📊 Employee Workload Visualization")

        if not df.empty:
            workload = df["employee_id"].value_counts()
            st.bar_chart(workload)
        else:
            st.info("No tasks assigned yet.")

    # ---------------- TAB 2 ----------------
    elif tab == "Task Status":
        st.subheader("📊 Task Status Tracking")

        df = pd.read_sql("SELECT * FROM task_status", conn)
        st.dataframe(df)

        if not df.empty:
            st.bar_chart(df["current_status"].value_counts())

        waiting = df[df["current_status"] == "WAITING_FOR_APPROVAL"]
        if not waiting.empty:
            st.warning(f"{len(waiting)} tasks are waiting for approval.")

    # ---------------- TAB 3 ----------------
    elif tab == "Approval Requests":
        st.subheader("⏳ Approval Requests")

        approvals = get_pending_approvals()
        st.dataframe(approvals)

        for _, row in approvals.iterrows():
            if st.button(
                f"Approve Task {row['task_id']} (Approval ID {row['approval_id']})"
            ):
                approve_task(row["approval_id"])
                st.success("Approved successfully. Refresh page.")

        st.subheader("💡 Suggestions")
        for s in generate_suggestions(len(approvals)):
            st.info(s)

conn.close()
