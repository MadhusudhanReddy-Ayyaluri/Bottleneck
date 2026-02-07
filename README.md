# Task Bottleneck & Approval Tracking System
<small>
This project is a role-based task monitoring system that enables organizations to efficiently manage employee tasks, track approval workflows, and identify process bottlenecks through a centralized dashboard, offering real-time visibility, secure role-based access, and enhanced accountability to improve overall operational efficiency and decision-making.
</small>
---

# Problem Statement

In many organizations, employees depend on managers for approvals such as:
- software access
- tool permissions
- data access
- client approvals

When approvals are delayed due to meetings or workload, employees are often blamed for delays without proper data evidence.

This system solves that problem by:
- tracking task assignments
- recording task progress
- logging approval requests with reasons
- giving managers a single dashboard to monitor and approve tasks

---

# Project Objectives

- Centralize task assignment and tracking
- Provide transparency in approval delays
- Eliminate dependency on email follow-ups
- Identify workflow bottlenecks
- Improve managerial decision-making using visual insights

---

# Roles & Responsibilities

# Manager (Admin)
- Assign tasks to employees
- View all employee task statuses
- Monitor approval requests
- Approve pending requests
- Analyze workload using charts
- Identify bottlenecks and delays

# Employee
- View only their assigned tasks
- Update task status
- Raise approval requests with reason for wait
- Cannot view other employees’ data
- Cannot approve tasks

---

# System Design Overview

- **Single Application**
- **Single Database**
- **Single Link**
- Role-based behavior inside the app

All users access the same link, but permissions differ based on selected role.

---

# Database Structure

# 1.task_assignment (Manager-controlled)
Stores task assignment details.

Fields:
- task_id
- task_title
- assigned_by
- employee_id
- assigned_time
- deadline
- priority

---

# 2.task_status (Employee-controlled)
Tracks task progress.

Fields:
- task_id
- current_status (ASSIGNED / IN_PROGRESS / WAITING_FOR_APPROVAL / COMPLETED)
- last_updated_time

---

# 3.approval_requests (Employee + Manager)
Tracks approval dependencies.

Fields:
- approval_id
- task_id
- requested_by
- requested_to
- reason_for_wait
- request_time
- approval_status (PENDING / APPROVED)

---
# Project Folder Structure

task-bottleneck-system/
│
├── dashboard/
│ └── app.py
│
├── src/
│ ├── db.py
│ ├── task_assignment.py
│ ├── task_status.py
│ ├── approval_requests.py
│ ├── bottleneck_analysis.py
│ └── suggestions.py
│
├── database/
│ └── workflow.db
│
├── requirements.txt
└── README.md

# Key Features

# Task Assignment
- Manager assigns tasks via dashboard
- Tasks linked to employees
- Priority and deadline supported

# Task Status Tracking
- Employees update progress
- Manager views real-time status

# Approval Request Management
- Employees raise approval requests
- Reason for wait is mandatory
- Manager approves directly from dashboard

# Bottleneck Detection
- Tasks waiting for approval are highlighted
- Approval delays are visible and countable

# Visual Analytics
- Bar chart showing employee workload
- Status distribution visualization
- Helps prevent employee overloading

# Clean Manager UX
- Assign Task section is collapsible
- Data-first, decision-driven layout

---

# User Interface Flow

# Employee View
- Select role: Employee
- Select employee ID
- View assigned tasks
- Update status
- Raise approval request

# Manager View
- Select role: Manager
- Assign new tasks (expandable section)
- View all assigned tasks
- Monitor task status
- Approve pending requests
- View workload charts

---

# Technology Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** SQLite
- **Data Handling:** Pandas
- **Visualization:** Streamlit Charts
- **Environment:** Virtual Environment (venv)

---



#  How to Run the Project

### Step 1: Activate virtual environment
    venv\Scripts\activate
### Step 2: Run the application
    streamlit run dashboard/app.py
### Step 3: Open in browser
    http://localhost:8501
