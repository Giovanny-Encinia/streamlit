from src.pages_custom.base_page import base
import streamlit as st
import numpy as np
from streamlit import session_state as ss
from src.funciones import search_maximum_cost
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
    "PUR_AMOUNT_USD",
]

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

    if ss.dataframemain["PUR_AMOUNT_USD"].dtypes == "object":
        ss.dataframemain["PUR_AMOUNT_USD"] = ss.dataframemain["PUR_AMOUNT_USD"].apply(
            lambda x: np.random.uniform(low=10, high=10000)
        )

    expensive.get_dataframe(search_maximum_cost(ss.dataframemain))
    expensive.main_content()
else:
    pass
