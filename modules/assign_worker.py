
import streamlit as st
import pandas as pd
import os
from datetime import date

def assign_worker():

    st.title("👷 Assign Worker")

    filename = "data/complaints.csv"

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        st.info("No complaints available.")
        return

    df = pd.read_csv(filename)

    if df.empty:
        st.info("No complaints available.")
        return

    pending = df[df["Status"]=="Pending"]

    if pending.empty:
        st.success("All complaints are assigned or resolved.")
        return

    complaint = st.selectbox(
        "Select Complaint",
        pending["Complaint ID"],
        format_func=lambda x: f"{x} | {pending.loc[pending['Complaint ID']==x,'Category'].values[0]}"
    )

    worker = st.text_input("Worker Name")

    department = st.selectbox(
        "Department",
        [
            "Sanitation",
            "Water Supply",
            "Electrical",
            "Road Maintenance",
            "Drainage",
            "Public Health",
            "General"
        ]
    )

    mobile = st.text_input("Worker Mobile Number")

    assign_date = st.date_input("Assignment Date", value=date.today())

    remarks = st.text_area("Assignment Remarks")

    if st.button("👷 Assign Worker"):

        idx = df[df["Complaint ID"]==complaint].index[0]

        df.loc[idx,"Assigned To"] = worker
        df.loc[idx,"Status"] = "Assigned"

        if "Department" not in df.columns:
            df["Department"] = ""

        if "Assignment Date" not in df.columns:
            df["Assignment Date"] = ""

        if "Worker Mobile" not in df.columns:
            df["Worker Mobile"] = ""

        if "Assignment Remarks" not in df.columns:
            df["Assignment Remarks"] = ""

        df.loc[idx,"Department"] = department
        df.loc[idx,"Assignment Date"] = str(assign_date)
        df.loc[idx,"Worker Mobile"] = mobile
        df.loc[idx,"Assignment Remarks"] = remarks

        df.to_csv(filename,index=False)

        st.success("Worker assigned successfully.")
        st.rerun()

    st.markdown("---")

    st.subheader("📋 Assigned Complaints")

    assigned = df[df["Status"]=="Assigned"]

    if assigned.empty:
        st.info("No assigned complaints.")
    else:
        st.dataframe(assigned, use_container_width=True)

        st.metric("Assigned Complaints", len(assigned))

        csv = assigned.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Assigned Complaints",
            csv,
            file_name="assigned_complaints.csv",
            mime="text/csv"
        )
