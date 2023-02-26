from streamlit import session_state as ss
from src.utils import read_load_json, load_keywords, load_data
from src.pages_custom.base_page import base
from src.queries.select import QUERY_RECORD
import streamlit as st

# READ JSON file
if "LABELS" not in ss:
    ss["LABELS"] = read_load_json("src/json/labels.json")

if "load_keywords_list" not in ss:
    ss["load_keywords_dict"] = load_keywords()

if "COLUMNS_FRONTEND" not in ss:
    ss["COLUMNS_FRONTEND"] = [
        "PUR_PO_TEXT",
        "PUR_COUNTRY",
        "PUR_PO_NUM",
        "PUR_PO_ITEM",
        "PUR_PO_DOC_TYPE",
        "PUR_PO_MATDOC",
        "PUR_PO_IT_MATDOC",
        "PUR_C_COST_TYPE",
        "PUR_VENDOR_NAME",
        "PUR_AMOUNT_USD",
        "PUR_PO_UOM",
    ]
# query = QUERY_RECORD
# df = load_data(query)
# st.dataframe(df)
main = base("main")
main.create_sidebar()
main.create_top()
main.main_content()
