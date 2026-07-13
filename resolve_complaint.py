
import streamlit as st
import pandas as pd
import os
from datetime import date

def resolve_complaint():

    st.title("✅ Resolve Complaint")

    filename = "data/complaints.csv"

    if (not os.path.exists(filename)) or os.path.getsize(filename) == 0:
        st.info("No complaints available.")
        return

    try:
        df = pd.read_csv(filename)
    except Exception:
        st.error("Unable to read complaints file.")
        return

    if df.empty:
        st.info("No complaints available.")
        return

    assigned = df[df["Status"] == "Assigned"]

    if assigned.empty:
        st.info("No assigned complaints are available for resolution.")
        return

    complaint_id = st.selectbox(
        "Select Assigned Complaint",
        assigned["Complaint ID"],
        format_func=lambda x: f"{x} | {assigned.loc[assigned['Complaint ID']==x,'Category'].values[0]}"
    )

    resolved_by = st.text_input("Resolved By")

    resolution_date = st.date_input(
        "Resolution Date",
        value=date.today()
    )

    remarks = st.text_area("Resolution Remarks")

    if st.button("✅ Mark as Resolved"):

        idx = df[df["Complaint ID"] == complaint_id].index[0]

        df.loc[idx, "Status"] = "Resolved"
        df.loc[idx, "Resolved Date"] = str(resolution_date)
        df.loc[idx, "Resolution Remarks"] = remarks

        if "Resolved By" not in df.columns:
            df["Resolved By"] = ""

        if "Resolution Days" not in df.columns:
            df["Resolution Days"] = ""

        df.loc[idx, "Resolved By"] = resolved_by

        try:
            complaint_date = pd.to_datetime(df.loc[idx, "Date"])
            days = (pd.to_datetime(str(resolution_date)) - complaint_date).days
        except Exception:
            days = 0

        df.loc[idx, "Resolution Days"] = days

        df.to_csv(filename, index=False)

        st.success("Complaint resolved successfully.")
        st.balloons()
        st.rerun()

    st.markdown("---")

    st.subheader("🟢 Resolved Complaints")

    resolved = df[df["Status"] == "Resolved"]

    if resolved.empty:
        st.info("No resolved complaints.")
    else:

        st.dataframe(
            resolved,
            use_container_width=True
        )

        c1, c2 = st.columns(2)

        c1.metric(
            "Resolved Complaints",
            len(resolved)
        )

        avg_days = resolved["Resolution Days"].fillna(0).astype(float).mean()

        c2.metric(
            "Average Resolution Time",
            f"{avg_days:.1f} Days"
        )

        csv = resolved.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download Resolved Complaints",
            csv,
            file_name="resolved_complaints.csv",
            mime="text/csv"
        )
