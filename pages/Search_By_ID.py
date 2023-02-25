# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com
import streamlit as st
from streamlit import session_state as ss
import time
from PIL import Image
from src.utils import read_load_json, find_paths, load_data, snowflake_connection
from src.queries.select import (
    DUMMY_QUERY,
    QUERY_RECORD_INFERENCE,
    QUERY_RECORD,
    QUERY_SEARCH_UNIQUE,
)
import datetime
import pandas as pd
from src.funciones import search_keywords, search_maximum_cost

col1, col2, col3 = st.columns([2, 2, 5])

with col1:
    image = Image.open("src/images/logo.png")
    st.image(image)

with col3:
    imagen = Image.open("src/images/MicrosoftTeams-image.png")
    st.image(imagen)

st.title("Procurement Labeling Tool Cemex")

if "last_indexid" not in ss:
    ss["last_indexid"] = 0

if "counterid" not in ss:
    ss["counterid"] = 0

if "country" not in ss:
    ss["country"] = "MX"

if "number" not in ss:
    ss["number"] = ""

if "item" not in ss:
    ss["item"] = 0

if "doc" not in ss:
    ss["doc"] = "ZIPO"

if "matdoc" not in ss:
    ss["matdoc"] = ""

if "it_matdoc" not in ss:
    ss["it_matdoc"] = 0

if "cost_type" not in ss:
    ss["cost_type"] = "Mat/Serv Cost"

if "add_cost_type" not in ss:
    ss["add_cost_type"] = "NAN"

ss["COLUMNS_FRONTEND"] = [
    "PUR_PO_TEXT",
    "LABEL",
    "CONFIDENCE",
    "PUR_COUNTRY",
    "PUR_VENDOR_NAME",
    "PUR_PO_UOM",
]
country_list = [
    ss["country"],
    "MX",
    "GT",
    "CR",
    "JM",
    "PA",
    "PE",
    "DO",
    "HT",
    "NI",
    "CO",
    "PR",
    "BS",
    "SV",
]
cost_type_list = [
    ss["cost_type"],
    "Mat/Serv Cost",
    "Ad. Cost",
]

doc_type_list = [
    ss["doc"],
    "ZIPO",
    "ZEUP",
    "ZICP",
    "LP",
    "FO",
    "CON",
    "ZNB",
    "ZFRC",
    "NB",
]
add_cost_list = [
    ss["add_cost_type"],
    "ZRB1",
    "ZI05",
    "ZI04",
    "ZI03",
    "ZI02",
    "ZI01",
]

with st.sidebar.form(key="formid"):
    country = st.selectbox("PUR_COUNTRY", country_list)
    number = st.text_input("PUR_PO_NUM", value=ss["number"], max_chars=10)
    item = st.number_input("PUR_PO_ITEM", min_value=0, value=ss["item"])
    doc = st.selectbox("PUR_PO_DOC_TYPE", doc_type_list)
    matdoc = st.text_input("PUR_PO_MATDOC", value=ss["matdoc"], max_chars=10)
    it_matdoc = st.number_input("PUR_PO_IT_MATDOC", min_value=0, value=ss["it_matdoc"])
    cost_type = st.selectbox("PUR_C_COST_TYPE", cost_type_list)
    add_cost_type = st.selectbox("PUR_ADD_COST_TYPE", add_cost_list)
    # Every form must have a submit button.
    submitted = st.form_submit_button("Get data")

    if submitted:
        if "is_ready" in ss:
            st.write("Succes")
        else:
            ss["is_ready"] = False

        ss["country"] = country
        ss["number"] = number
        ss["item"] = item
        ss["doc"] = doc
        ss["matdoc"] = matdoc
        ss["it_matdoc"] = it_matdoc
        ss["cost_type"] = cost_type
        ss["add_cost_type"] = add_cost_type

        ss["counterid"] = 0
        sql_params = dict(
            country=ss["country"],
            number=ss["number"],
            doc=ss["doc"],
            matdoc=ss["matdoc"],
            cost_type=ss["cost_type"],
        )
        query = QUERY_SEARCH_UNIQUE.format(**sql_params)
        df = load_data(query, True)
        # df_inference = load_data(QUERY_RECORD_INFERENCE.format(option))
        ss["last_indexid"] = df.shape[0] - 1
        df = df.rename(
            columns={"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"}
        )
        df["LABELED"] = False

        if ss["last_indexid"] > 0:
            ss["dataframeid"] = df
            ss["id"] = True
        else:
            st.warning("No result, there is not data")
            ss["dataframeid"] = pd.DataFrame([], ss.COLUMNS_FRONTEND)


col1, col2, col3 = st.columns(3)

if "dataframeid" in ss and not ss["dataframeid"].empty:
    ss["dataframeid"] = ss["dataframeid"].query(
        "PUR_PO_ITEM == @ss['item'] and PUR_PO_IT_MATDOC == @ss['it_matdoc']"
    )
    ss["last_indexid"] = ss["dataframeid"].shape[0] - 1
    st.dataframe(
        ss["dataframeid"],
        use_container_width=True,
    )
