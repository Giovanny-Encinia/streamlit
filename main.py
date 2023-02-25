from streamlit import session_state as ss
from src.utils import read_load_json, load_keywords
from src.pages_custom.base_page import base

# READ JSON file
if "LABELS" not in ss:
    ss["LABELS"] = read_load_json("src/json/labels.json")

if "load_keywords_list" not in ss:
    ss["load_keywords_dict"] = load_keywords()

if "COLUMNS_FRONTEND" not in ss:
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
