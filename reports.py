
import streamlit as st
import pandas as pd
import os

def reports():
    st.title("📑 Panchayat Reports")

    filename="data/complaints.csv"

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        st.info("No complaint records available.")
        return

    try:
        df=pd.read_csv(filename)
    except:
        st.error("Unable to read complaints file.")
        return

    if df.empty:
        st.info("No complaint records available.")
        return

    total=len(df)
    pending=df[df["Status"]=="Pending"]
    assigned=df[df["Status"]=="Assigned"]
    resolved=df[df["Status"]=="Resolved"]
    high=df[df["Priority"]=="High"]

    c1,c2,c3,c4=st.columns(4)
    c1.metric("Total",total)
    c2.metric("Pending",len(pending))
    c3.metric("Assigned",len(assigned))
    c4.metric("Resolved",len(resolved))

    st.markdown("---")

    summary=pd.DataFrame({
        "Report":["Total Complaints","Pending","Assigned","Resolved","High Priority"],
        "Count":[total,len(pending),len(assigned),len(resolved),len(high)]
    })

    st.subheader("📊 Summary")
    st.dataframe(summary,use_container_width=True)

    st.bar_chart(summary.set_index("Report"))

    st.markdown("---")

    tabs=st.tabs([
        "Pending",
        "Assigned",
        "Resolved",
        "High Priority",
        "All Complaints"
    ])

    with tabs[0]:
        st.dataframe(pending,use_container_width=True)

    with tabs[1]:
        st.dataframe(assigned,use_container_width=True)

    with tabs[2]:
        st.dataframe(resolved,use_container_width=True)

    with tabs[3]:
        st.dataframe(high,use_container_width=True)

    with tabs[4]:
        st.dataframe(df,use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Download Reports")

    reports=[
        ("Pending Complaints",pending,"pending_complaints.csv"),
        ("Assigned Complaints",assigned,"assigned_complaints.csv"),
        ("Resolved Complaints",resolved,"resolved_complaints.csv"),
        ("High Priority Complaints",high,"high_priority_complaints.csv"),
        ("All Complaints",df,"all_complaints.csv"),
        ("Summary Report",summary,"summary_report.csv")
    ]

    for title,data,file in reports:
        st.download_button(
            f"📄 {title}",
            data.to_csv(index=False).encode("utf-8"),
            file_name=file,
            mime="text/csv"
        )
