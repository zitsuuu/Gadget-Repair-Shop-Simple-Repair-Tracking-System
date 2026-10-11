import streamlit as st
import sqlite3
from pathlib import Path

# Page settings
st.set_page_config(
    page_title="GadgetFix | Repair Tracking",
    page_icon="🔧",
    layout="centered"
)

# Always use the database beside this file
DB_PATH = Path(__file__).resolve().parent / "gadgetfix.db"

st.title("🔧 GadgetFix")
st.subheader("Gadget Repair Tracking")
st.write("Check the progress of your gadget repair.")

st.divider()

receipt_no = st.text_input(
    "Enter your receipt number",
    placeholder="e.g. 1"
)

if st.button("Check Repair Status", use_container_width=True):
    if not receipt_no.strip():
        st.warning("Please enter your receipt number.")

    elif not receipt_no.strip().isdigit() or int(receipt_no) <= 0:
        st.error("Please enter a valid receipt number.")

    elif not DB_PATH.exists():
        st.error("Repair database not found.")

    else:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT receipt_no, name, gadget, problem,
                   cost, status, date_time, completed_time
            FROM repairs
            WHERE receipt_no = ?
        """, (int(receipt_no),))

        repair = cursor.fetchone()
        conn.close()

        if repair is None:
            st.error("No repair found with that receipt number.")

        else:
            st.success("Repair record found!")

            st.markdown("### Repair Details")
            st.write("**Receipt Number:**", repair[0])
            st.write("**Customer Name:**", repair[1])
            st.write("**Gadget:**", repair[2])

            st.markdown("### Repair Problems")
            st.text(repair[3])

            st.write("**Total Cost:** ₱", repair[4])
            st.write("**Date Received:**", repair[6])

            st.markdown("### Current Status")

            if repair[5] == "Waiting for repair":
                st.info("🕒 Waiting for repair")

            elif repair[5] == "Being repaired":
                st.warning("🔧 Being repaired")

            elif repair[5] == "Completed":
                st.success("✅ Repair completed")

            else:
                st.write(repair[5])

            if repair[7]:
                st.write("**Completed On:**", repair[7])

st.divider()
st.caption("GadgetFix — Simple Gadget Repair Tracking System") 