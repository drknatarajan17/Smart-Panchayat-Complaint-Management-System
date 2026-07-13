
import streamlit as st
import pandas as pd
import os

def ai_advisor():

    st.title("🤖 AI Panchayat Advisor")

    filename = "data/complaints.csv"

    if (not os.path.exists(filename)) or os.path.getsize(filename)==0:
        st.info("No complaint data available.")
        return

    try:
        df = pd.read_csv(filename)
    except Exception:
        st.error("Unable to read complaint data.")
        return

    if df.empty:
        st.info("No complaint data available.")
        return

    total = len(df)
    pending = len(df[df["Status"]=="Pending"])
    assigned = len(df[df["Status"]=="Assigned"])
    resolved = len(df[df["Status"]=="Resolved"])
    high = len(df[df["Priority"]=="High"])

    pending_ratio = (pending/total)*100 if total else 0
    resolved_ratio = (resolved/total)*100 if total else 0

    st.subheader("📊 Panchayat Performance")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Complaints", total)
    c2.metric("Pending %", f"{pending_ratio:.1f}%")
    c3.metric("Resolved %", f"{resolved_ratio:.1f}%")
    c4.metric("High Priority", high)

    st.markdown("---")
    st.subheader("🧠 AI Recommendations")

    tips = []

    if pending > resolved:
        tips.append("🔴 Pending complaints are higher than resolved complaints. Increase workforce allocation.")

    if high > 5:
        tips.append("🚨 High priority complaints are increasing. Address them immediately.")

    if "Category" in df.columns and not df.empty:
        top_category = df["Category"].mode().iloc[0]
        tips.append(f"📌 Most frequent complaint: **{top_category}**. Plan preventive maintenance.")

    if "Village" in df.columns and not df.empty:
        top_village = df["Village"].mode().iloc[0]
        tips.append(f"🏘️ Village with the highest complaints: **{top_village}**. Schedule a field inspection.")

    if "Resolution Days" in df.columns:
        res = df[df["Status"]=="Resolved"].copy()
        if not res.empty:
            res["Resolution Days"] = pd.to_numeric(res["Resolution Days"], errors="coerce").fillna(0)
            avg_days = res["Resolution Days"].mean()

            if avg_days > 7:
                tips.append(f"⏳ Average resolution time is {avg_days:.1f} days. Improve response times.")
            else:
                tips.append(f"✅ Average resolution time is {avg_days:.1f} days. Good performance.")

    if assigned > pending:
        tips.append("👷 Most complaints have been assigned to workers. Continue monitoring progress.")

    if not tips:
        tips.append("🎉 Complaint management is running smoothly.")

    for tip in tips:
        st.write(tip)

    st.markdown("---")

    st.subheader("⭐ Panchayat Performance Score")

    score = 100

    if pending_ratio > 50:
        score -= 30
    elif pending_ratio > 30:
        score -= 15

    if high > 10:
        score -= 20
    elif high > 5:
        score -= 10

    if "Resolution Days" in df.columns:
        res = df[df["Status"]=="Resolved"].copy()
        if not res.empty:
            avg = pd.to_numeric(res["Resolution Days"], errors="coerce").fillna(0).mean()
            if avg > 7:
                score -= 15

    score = max(score, 0)

    st.metric("Performance Score", f"{score}/100")
    st.progress(score/100)

    if score >= 85:
        st.success("🟢 Excellent Panchayat Service")
    elif score >= 70:
        st.info("🟡 Good Performance")
    elif score >= 50:
        st.warning("🟠 Average Performance")
    else:
        st.error("🔴 Needs Immediate Improvement")

    st.markdown("---")

    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download AI Analysis Data",
        csv,
        file_name="ai_analysis.csv",
        mime="text/csv"
    )
