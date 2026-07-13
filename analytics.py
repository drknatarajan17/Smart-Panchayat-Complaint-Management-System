
import streamlit as st
import pandas as pd
import os

def analytics():
    st.title("📊 Panchayat Analytics")
    filename="data/complaints.csv"
    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        st.info("No complaint data available.")
        return
    try:
        df=pd.read_csv(filename)
    except:
        st.error("Unable to read complaint data.")
        return
    if df.empty:
        st.info("No complaint data available.")
        return
    total=len(df); pending=(df["Status"]=="Pending").sum(); assigned=(df["Status"]=="Assigned").sum(); resolved=(df["Status"]=="Resolved").sum(); high=(df["Priority"]=="High").sum()
    c1,c2,c3,c4,c5=st.columns(5)
    c1.metric("Total",total); c2.metric("Pending",pending); c3.metric("Assigned",assigned); c4.metric("Resolved",resolved); c5.metric("High Priority",high)
    st.subheader("Complaints by Category"); st.bar_chart(df.groupby("Category").size())
    st.subheader("Complaints by Village"); st.bar_chart(df.groupby("Village").size())
    st.subheader("Complaints by Priority"); st.bar_chart(df.groupby("Priority").size())
    st.subheader("Complaint Status"); st.bar_chart(df.groupby("Status").size())
    if "Assigned To" in df.columns:
        w=df[df["Assigned To"].fillna("")!=""]
        if not w.empty:
            st.subheader("Worker Performance"); st.bar_chart(w.groupby("Assigned To").size())
    if "Resolution Days" in df.columns:
        r=df[df["Status"]=="Resolved"].copy()
        if not r.empty:
            r["Resolution Days"]=pd.to_numeric(r["Resolution Days"],errors="coerce").fillna(0)
            st.metric("Average Resolution Days",f"{r['Resolution Days'].mean():.1f}")
    top_cat=df["Category"].mode().iloc[0]
    top_village=df["Village"].mode().iloc[0]
    st.success(f"Most common complaint: {top_cat}")
    st.info(f"Village with highest complaints: {top_village}")
    st.download_button("📥 Download Analytics Data",df.to_csv(index=False).encode(),"analytics_data.csv","text/csv")
