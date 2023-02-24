import streamlit as st
from streamlit import session_state as ss
import time
from PIL import Image
from src.utils import read_load_json, find_paths, load_data, snowflake_connection
from src.queries.select import DUMMY_QUERY, QUERY_RECORD_INFERENCE, QUERY_RECORD
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

country_list = [
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
    "Mat/Serv Cost",
    "Ad. Cost",
]

doc_type_list = [
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
    "NAN",
    "ZRB1",
    "ZI05",
    "ZI04",
    "ZI03",
    "ZI02",
    "ZI01",
]

with st.sidebar.form(key="formid"):
    country = st.selectbox("PUR_COUNTRY", country_list)
    p_number = st.text_input("PUR_PO_NUM")
    item = st.number_input("PUR_PO_ITEM", min_value=0)
    doc_type = st.selectbox("PUR_PO_DOC_TYPE", doc_type_list)
    matdoc = st.text_input("PUR_PO_MATDOC")
    it_matdoc = st.number_input("PUR_PO_IT_MATDOC", min_value=0)
    cost_type = st.selectbox("PUR_C_COST_TYPE", cost_type_list)
    add_cost_type = st.selectbox("PUR_ADD_COST_TYPE", add_cost_list)
    # Every form must have a submit button.
    submitted = st.form_submit_button("Get data")

    if submitted:
        ss["option"] = option

        if "is_ready" in ss:
            st.write("Succes")
        else:
            ss["is_ready"] = False

        ss["counterid"] = 0
        sql_params = dict(
            sample=ss.samples, start_date=ss.start_date, end_date=ss.end_date
        )
        query = DUMMY_QUERY.format(**sql_params)
        df = load_data(query)
        # df_inference = load_data(QUERY_RECORD_INFERENCE.format(option))
        ss["last_indexid"] = df.shape[0] - 1
        df = df.rename(
            columns={"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"}
        )
        df["LABELED"] = False

        if ss["last_indexid"] > 0:
            ss["dataframemain"] = df
            ss[self.page_name] = True
        else:
            st.warning("No result, there is not data")
            ss[self.dataframe] = pd.DataFrame([], ss.COLUMNS_FRONTEND)
