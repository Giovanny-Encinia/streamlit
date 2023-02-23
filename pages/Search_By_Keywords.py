from src.pages_custom.base_page import base
import streamlit as st
from streamlit import session_state as ss
from src.funciones import search_keywords
from src.utils import (
    read_load_json,
    find_paths,
    load_data,
    snowflake_connection,
    load_keywords,
)

ss["LABELS"] = read_load_json("src/json/labels.json")
load_keywords_dict = load_keywords()
ss["COLUMNS_FRONTEND"] = [
    "PUR_PO_TEXT",
    "LABEL",
    "CONFIDENCE",
    "PUR_COUNTRY",
    "PUR_VENDOR_NAME",
    "PUR_PO_UOM",
]

if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    keywords = base("keywords")
elif "dataframemain" in ss:
    keywords = base("keywords")
    keywords.create_sidebar()

keywords.create_top()
if (
    ss.option == "DIESEL" or ss.option == "BEARINGS AND ACCESORIES"
) and not ss.dataframemain.empty:
    keywords.get_dataframe(
        search_keywords(ss.dataframemain, load_keywords_dict[ss.option]["KEYWORDS"])
    )
    keywords.main_content()
else:
    pass
