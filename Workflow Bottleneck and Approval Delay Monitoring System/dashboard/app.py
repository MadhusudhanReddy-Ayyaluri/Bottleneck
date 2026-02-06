import streamlit as st
import sys, os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.data_loader import load_data
from src.bottleneck_detector import detect_bottlenecks
from src.predictor import train_model
from src.suggestions import generate_suggestions


st.set_page_config(layout="wide")
st.title("🚀 AI Bottleneck Detection & Delay Prediction Dashboard")


file = st.file_uploader("Upload Workflow CSV", type=["csv"])


if file:

    # -------------------------
    # Load data
    # -------------------------
    df = load_data(file)


    # -------------------------
    # Employee Filter
    # -------------------------
    st.subheader("🔍 Filter by Employee")

    employees = df["employee_id"].unique()

    selected_employee = st.selectbox(
        "Choose Employee",
        ["All"] + list(employees)
    )

    if selected_employee != "All":
        df = df[df["employee_id"] == selected_employee]


    # -------------------------
    # Train ML model
    # -------------------------
    model = train_model(df)

    X = df[[
        "approval_wait_hours",
        "workload_level",
        "total_duration_hours"
    ]]

    predictions = model.predict(X)

    proba = model.predict_proba(X)

    # safe probability fix
    if proba.shape[1] == 1:
        probabilities = [0.0] * len(df)
    else:
        probabilities = proba[:, 1]

    df["prediction"] = predictions
    df["risk_%"] = (pd.Series(probabilities) * 100).round(2)


    # -------------------------
    # KPI Metrics
    # -------------------------
    st.subheader("📊 Summary")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Tasks", len(df))
    c2.metric("Delayed Tasks", int(df["delayed"].sum()))
    c3.metric("Average Risk %", round(df["risk_%"].mean(), 2))


    # -------------------------
    # Bottleneck Charts
    # -------------------------
    st.subheader("📈 Bottleneck Analysis")

    stage_delay, approver_delay = detect_bottlenecks(df)

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Stage Bottlenecks")
        st.bar_chart(stage_delay)

    with col2:
        st.write("### Approver Bottlenecks")
        st.bar_chart(approver_delay)


    # -------------------------
    # Role Analysis
    # -------------------------
    st.subheader("👥 Role Based Delay")

    role_delay = df.groupby("role")["approval_wait_hours"].mean()
    st.bar_chart(role_delay)


    # -------------------------
    # Prediction Table
    # -------------------------
    st.subheader("🤖 Task Delay Predictions")

    display_cols = [
        "task_id",
        "employee_id",
        "stage_name",
        "approver_id",
        "approval_wait_hours",
        "risk_%",
        "prediction"
    ]

    st.dataframe(df[display_cols])


    # -------------------------
    # Suggestions
    # -------------------------
    st.subheader("💡 Recommendations")

    for s in generate_suggestions(stage_delay, approver_delay):
        st.success(s)


    # -------------------------
    # Download Report
    # -------------------------
    st.subheader("⬇️ Download Report")

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "Download Report CSV",
        csv,
        "bottleneck_report.csv",
        "text/csv"
    )
