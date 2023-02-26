# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com
from src.pages_custom.base_page import base
import streamlit as st
from streamlit import session_state as ss
from src.funciones import search_keywords
from src.utils import read_load_json, load_keywords

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

if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    keywords = base("keywords")
elif "dataframemain" in ss:
    keywords = base("keywords")
    keywords.create_sidebar()

keywords.create_top()

if (
    "dataframemain" in ss
    and (ss.option == "DIESEL" or ss.option == "BEARINGS AND ACCESORIES")
    and not ss.dataframemain.empty
):
    keywords.get_dataframe(
        search_keywords(
            ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"]
        )
    )
    keywords.main_content()
else:
    pass
