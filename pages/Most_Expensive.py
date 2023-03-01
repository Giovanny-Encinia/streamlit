from src.pages_custom.base_page import base
import streamlit as st
import numpy as np
from streamlit import session_state as ss
from src.funciones import search_maximum_cost, tree_functions
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
# query
if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    expensive = base("expensive")
elif "dataframemain" in ss:
    expensive = base("expensive")
    expensive.create_sidebar()

expensive.create_top()

if "dataframemain" in ss and not ss.dataframemain.empty:
    st.write(ss.dataframemain["PUR_AMOUNT_USD"].dtypes)

    # if ss.dataframemain["PUR_AMOUNT_USD"].dtypes == "object":
    #     ss.dataframemain["PUR_AMOUNT_USD"] = ss.dataframemain["PUR_AMOUNT_USD"].apply(
    #         lambda x: np.random.uniform(low=10, high=10000)
    #     )

    # expensive.get_dataframe(search_maximum_cost(ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"]))
    tree_functions(ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"])
    expensive.main_content()
else:
    pass
