import streamlit as st
from streamlit import session_state as ss
from PIL import Image
from src.funciones import search_keywords, search_maximum_cost
from src.utils import (
    read_load_json,
    find_paths,
    load_data,
    snowflake_connection,
    load_keywords,
)
from src.queries.select import DUMMY_QUERY
from src.on_click_functions.buttons import next, previous
import datetime
import pandas as pd
from src.pages_custom.base_page import base

# READ JSON file
ss["LABELS"] = read_load_json("src/json/labels.json")
ss["keywords"] = load_keywords()
ss["COLUMNS_FRONTEND"] = [
    "PUR_PO_TEXT",
    "LABEL",
    "CONFIDENCE",
    "PUR_COUNTRY",
    "PUR_VENDOR_NAME",
    "PUR_PO_UOM",
]
main = base("main")
main.create_sidebar()
main.create_top()
main.main_content()
