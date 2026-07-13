
import streamlit as st
import pandas as pd
import os
from datetime import date
import uuid

def complaint_register():
    st.title("📝 Register Complaint")

    os.makedirs("data", exist_ok=True)
    filename="data/complaints.csv"

    cols=[
        "Complaint ID","Date","Citizen","Mobile","Village","Ward",
        "Category","Priority","Description","Assigned To",
        "Status","Resolved Date","Resolution Remarks"
    ]

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        pd.DataFrame(columns=cols).to_csv(filename,index=False)

    try:
        df=pd.read_csv(filename)
    except Exception:
        df=pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    if list(df.columns)!=cols:
        df=pd.DataFrame(columns=cols)
        df.to_csv(filename,index=False)

    complaint_id="CMP-"+uuid.uuid4().hex[:8].upper()

    with st.form("complaint_form",clear_on_submit=True):
        st.text_input("Complaint ID",value=complaint_id,disabled=True)
        cdate=st.date_input("Complaint Date",value=date.today())
        citizen=st.text_input("Citizen Name")
        mobile=st.text_input("Mobile Number")
        village=st.text_input("Village")
        ward=st.text_input("Ward Number")

        category=st.selectbox("Complaint Category",[
            "Dust Bin Not Cleared",
            "Water Supply Issue",
            "Water Leakage",
            "Street Light Not Working",
            "Drainage Blockage",
            "Road Damage",
            "Garbage Collection",
            "Mosquito Issue",
            "Public Toilet Cleaning",
            "Tree Fallen",
            "Electrical Problem",
            "Other"
        ])

        priority=st.selectbox("Priority",["High","Medium","Low"])
        description=st.text_area("Complaint Description")

        submit=st.form_submit_button("📩 Register Complaint")

    if submit:
        if citizen.strip()=="" or village.strip()=="":
            st.error("Citizen Name and Village are required.")
            return

        new=pd.DataFrame([{
            "Complaint ID":complaint_id,
            "Date":cdate,
            "Citizen":citizen,
            "Mobile":mobile,
            "Village":village,
            "Ward":ward,
            "Category":category,
            "Priority":priority,
            "Description":description,
            "Assigned To":"",
            "Status":"Pending",
            "Resolved Date":"",
            "Resolution Remarks":""
        }])

        df=pd.concat([df,new],ignore_index=True)
        df.to_csv(filename,index=False)

        st.success(f"Complaint {complaint_id} registered successfully.")
        st.balloons()

    st.markdown("---")
    st.subheader("Recent Complaints")

    df=pd.read_csv(filename)

    if df.empty:
        st.info("No complaints registered.")
    else:
        st.dataframe(
            df.sort_values("Date",ascending=False).head(10),
            use_container_width=True
        )
