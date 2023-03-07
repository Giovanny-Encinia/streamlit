from streamlit import session_state as ss
from src.utils import load_states
from src.pages_custom.base_page import base
import streamlit as st

# READ JSON file
load_states()

# query = QUERY_RECORD
# df = load_data(query)
# st.dataframe(df)
main = base("main")
main.create_sidebar()
main.create_top()

if "dataframemain" in ss and not ss["dataframemain"].empty:
    st.dataframe(ss["dataframemain"][ss.COLUMNS_FRONTEND])
