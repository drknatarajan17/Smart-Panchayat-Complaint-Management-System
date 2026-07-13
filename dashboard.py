
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def dashboard():
    st.title("🏛️ Smart Panchayat Dashboard")

    os.makedirs("data", exist_ok=True)
    filename = "data/complaints.csv"

    cols = [
        "Complaint ID","Date","Citizen","Mobile","Village","Ward",
        "Category","Priority","Description","Assigned To",
        "Status","Resolved Date","Resolution Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=cols).to_csv(filename,index=False)

    try:
        df = pd.read_csv(filename)
    except Exception:
        df = pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    if list(df.columns)!=cols:
        df = pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    if df.empty:
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Total Complaints",0)
        c2.metric("Pending",0)
        c3.metric("Resolved",0)
        c4.metric("High Priority",0)
        st.info("No complaints registered yet.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    today = pd.Timestamp.today().normalize()

    total = len(df)
    pending = len(df[df["Status"]=="Pending"])
    resolved = len(df[df["Status"]=="Resolved"])
    high = len(df[df["Priority"]=="High"])

    overdue = df[
        (df["Status"]=="Pending") &
        ((today - df["Date"]).dt.days > 7)
    ]

    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("Total", total)
    c2.metric("🔴 Pending", pending)
    c3.metric("🟢 Resolved", resolved)
    c4.metric("🟠 High Priority", high)
    c5.metric("🚨 Overdue", len(overdue))

    st.markdown("---")

    st.subheader("📊 Complaints by Category")
    st.bar_chart(df.groupby("Category").size())

    st.subheader("🏘️ Complaints by Village")
    st.bar_chart(df.groupby("Village").size())

    st.markdown("---")

    st.subheader("🚨 Pending Complaints")

    pending_df = df[df["Status"]=="Pending"].copy()

    if pending_df.empty:
        st.success("No pending complaints.")
    else:
        pending_df["Pending Days"] = (
            today - pending_df["Date"]
        ).dt.days

        def highlight(row):
            color = "#ffcccc" if row["Pending Days"]>7 else "#fff4cc"
            return [f"background-color:{color}"]*len(row)

        st.dataframe(
            pending_df.style.apply(highlight, axis=1),
            use_container_width=True
        )

    st.markdown("---")

    st.subheader("🟢 Recently Resolved")

    solved = df[df["Status"]=="Resolved"]

    if solved.empty:
        st.info("No resolved complaints.")
    else:
        st.dataframe(
            solved.sort_values("Resolved Date", ascending=False),
            use_container_width=True
        )
