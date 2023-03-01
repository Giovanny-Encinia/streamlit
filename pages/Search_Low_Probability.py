from src.pages_custom.base_page import base
import streamlit as st
from streamlit import session_state as ss
from src.funciones import search_keywords, threshold
from src.utils import (
    read_load_json,
    find_paths,
    load_data,
    snowflake_connection,
    load_keywords,
)

if "LABELS" not in ss:
    ss["LABELS"] = read_load_json("src/json/labels.json")

if "load_keywords_list" not in ss:
    ss["load_keywords_dict"] = load_keywords()

if "COLUMNS_FRONTEND" not in ss:
    ss["COLUMNS_FRONTEND"] = [
        "PUR_PO_TEXT",
        "PUR_COUNTRY",
        "PUR_PO_NUM",
        "PUR_PO_DOC_TYPE",
        "PUR_PO_MATDOC",
        "PUR_C_COST_TYPE",
        "PUR_VENDOR_NAME",
        "PUR_AMOUNT_USD",
        "PUR_PO_UOM",
        "PUR_LINE_DESC_PREDICTED",
        "PUR_LINE_DESC_PROBABILITY",
        "NIVEL1_PREDICTED",
        "NIVEL1_PROBABILITY",
        "NIVEL2_PREDICTED",
        "NIVEL2_PROBABILITY",
        "NIVEL3_PREDICTED",
        "NIVEL3_PROBABILITY",
        "NIVEL4_PREDICTED",
        "NIVEL4_PROBABILITY",
    ]

if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    low = base("low")
elif "dataframemain" in ss:
    low = base("low")
    low.create_sidebar()

low.create_top()

if "dataframemain" in ss and not ss.dataframemain.empty:
    low.get_dataframe(threshold(ss.dataframemain))
    low.main_content()
else:
    pass
