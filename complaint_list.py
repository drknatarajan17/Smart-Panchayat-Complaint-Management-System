
import streamlit as st
import pandas as pd
import os

def complaint_list():

    st.title("📋 Complaint Register")

    filename = "data/complaints.csv"

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        st.info("No complaints available.")
        return

    try:
        df = pd.read_csv(filename)
    except Exception:
        st.error("Unable to read complaints.csv")
        return

    if df.empty:
        st.info("No complaints available.")
        return

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    today = pd.Timestamp.today().normalize()
    df["Pending Days"] = (today - df["Date"]).dt.days.fillna(0).astype(int)

    st.subheader("🔍 Search & Filter")

    c1, c2, c3, c4 = st.columns(4)

    cid = c1.text_input("Complaint ID")
    village = c2.selectbox("Village", ["All"] + sorted(df["Village"].fillna("").unique().tolist()))
    category = c3.selectbox("Category", ["All"] + sorted(df["Category"].fillna("").unique().tolist()))
    status = c4.selectbox("Status", ["All"] + sorted(df["Status"].fillna("").unique().tolist()))

    filtered = df.copy()

    if cid:
        filtered = filtered[filtered["Complaint ID"].astype(str).str.contains(cid, case=False)]

    if village != "All":
        filtered = filtered[filtered["Village"] == village]

    if category != "All":
        filtered = filtered[filtered["Category"] == category]

    if status != "All":
        filtered = filtered[filtered["Status"] == status]

    st.markdown("---")
    st.subheader("📋 Complaint Register")

    def highlight(row):
        if row["Status"] == "Pending" and row["Pending Days"] > 7:
            color = "#ffb3b3"
        elif row["Status"] == "Pending":
            color = "#fff2b3"
        elif row["Status"] == "Resolved":
            color = "#c6efce"
        else:
            color = ""
        return [f"background-color:{color}"] * len(row)

    st.dataframe(
        filtered.style.apply(highlight, axis=1),
        use_container_width=True
    )

    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total", len(filtered))
    c2.metric("Pending", (filtered["Status"]=="Pending").sum())
    c3.metric("Resolved", (filtered["Status"]=="Resolved").sum())
    c4.metric("High Priority", (filtered["Priority"]=="High").sum())

    st.markdown("---")

    csv = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Complaint Register",
        csv,
        file_name="complaint_register.csv",
        mime="text/csv"
    )
