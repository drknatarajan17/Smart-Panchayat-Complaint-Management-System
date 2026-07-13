
import streamlit as st
from modules.dashboard import dashboard
from modules.complaint_register import complaint_register
from modules.complaint_list import complaint_list
from modules.assign_worker import assign_worker
from modules.resolve_complaint import resolve_complaint
from modules.analytics import analytics
from modules.reports import reports
from modules.ai_advisor import ai_advisor

st.set_page_config(page_title="Smart Panchayat Complaint Management System",page_icon="🏛️",layout="wide")
st.sidebar.title("🏛️ Smart Panchayat")

menu=st.sidebar.radio("Navigation",[
"🏠 Dashboard",
"📝 Register Complaint",
"📋 Complaint Register",
"👷 Assign Worker",
"✅ Resolve Complaint",
"📊 Analytics",
"📑 Reports",
"🤖 AI Advisor",
"ℹ️ About"
])

if menu=="🏠 Dashboard":
    dashboard()
elif menu=="📝 Register Complaint":
    complaint_register()
elif menu=="📋 Complaint Register":
    complaint_list()
elif menu=="👷 Assign Worker":
    assign_worker()
elif menu=="✅ Resolve Complaint":
    resolve_complaint()
elif menu=="📊 Analytics":
    analytics()
elif menu=="📑 Reports":
    reports()
elif menu=="🤖 AI Advisor":
    ai_advisor()
else:
    st.title("ℹ️ About")
    st.write("Smart Panchayat Complaint Management System")
    st.write("Author: Dr. K. Natarajan")
