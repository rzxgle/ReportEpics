import streamlit as st

def render_epics(epics):

    for _, epic in epics.iterrows():

        progress = epic["progress"] / 100

        st.write(
            f"Epic {epic['epic']} "
            f"({epic['completed_items']}/{epic['total_items']})"
        )

        st.progress(progress)