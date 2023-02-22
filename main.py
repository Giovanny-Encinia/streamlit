import streamlit as st
from streamlit import session_state as ss
import time
from PIL import Image
from src.funciones import search_keywords
from src.utils import read_load_json, find_paths, load_data, snowflake_connection
from src.queries.select import DUMMY_QUERY, QUERY_RECORD_INFERENCE, QUERY_RECORD
from src.on_click_functions.buttons import next, previous
import datetime
import pandas as pd

# READ JSON file
LABELS = read_load_json('src/json/labels.json')
bearings_keywords = read_load_json("src/json/bearings_keywords.json")
# st.write(load_data(QUERY_RECORD).columns)
c, cc, ccc = st.columns([2, 2, 5])

with c:
    image = Image.open("src/images/logo.png")
    st.image(image)

with ccc:
    imagen = Image.open("src/images/MicrosoftTeams-image.png")
    st.image(imagen)

st.title("Procurement Labeling Tool Cemex")
COLUMNS_FRONTEND = ["PUR_PO_TEXT", "LABEL", "CONFIDENCE", "PUR_COUNTRY", "PUR_VENDOR_NAME", "PUR_PO_UOM"]

if "last_index" not in ss:
    ss["last_index"] = 0

if "counter" not in ss:
    ss["counter"] = 0

#Sidebar
with st.sidebar.form("Input"):
    now = datetime.datetime.now()
    two_weeks_ago= now - datetime.timedelta(weeks=2)
    label_option = set(LABELS.keys()).union(LABELS["SERVICIOS"].keys())
    ss["option"] = st.selectbox("Which database do you want to validate?", label_option)
    ss["start_date"] = st.date_input("Select begin date", two_weeks_ago)
    ss["start_date"] = ss.start_date.strftime("%Y-%m-%d")
    ss["end_date"] = st.date_input("Select end date", now)
    ss["end_date"] = ss.end_date.strftime("%Y-%m-%d")
    ss["samples"] = st.number_input("How many samples do you want?: ", min_value=10, max_value=10000)
    # Every form must have a submit button.
    submitted = st.form_submit_button("Get data")
    

    if submitted:
        
        if "is_ready" in ss:
            st.write("Succes")
        else: 
            ss["is_ready"] = False
        
        ss["counter"] = 0
        sql_params = dict(sample=ss.samples, start_date=ss.start_date, end_date=ss.end_date)
        query = DUMMY_QUERY.format(**sql_params)
        df = load_data(query)
        # df_inference = load_data(QUERY_RECORD_INFERENCE.format(option))
        ss["last_index"] = df.shape[0] - 1
        df = df.rename(columns = {"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"})
        df["LABELED"] = False
        
        if ss["last_index"]  > 0:
            ss["dataframe"] = df
        else:
            st.warning("No result, there is not data")


with st.container():   
    col1, col2, col3 = st.columns(3)

    # there exist the posibility that the query is void
    if "dataframe" not in ss or ss["last_index"] <= 0:
        ss["dataframe"] = pd.DataFrame([], COLUMNS_FRONTEND)
        st.dataframe(ss.dataframe,  use_container_width=True)
    elif "dataframe" in ss:
        ss["last_index"] = ss.dataframe.shape[0] - 1

        if ss.counter < ss["last_index"]:
            col3.button("Next", on_click=next)
        
        if ss.counter > 0:
            col1.button("Previous", on_click=previous) 

        st.dataframe(ss.dataframe.iloc[ss.counter].loc[COLUMNS_FRONTEND],  use_container_width=True)
        check = st.radio("Label:", ('Correct', 'Incorrect'))

        if check == "Incorrect":
            tree = LABELS

            if ss.option not in  ["BEARINGS AND ACCESORIES", "DIESEL"]:
                tree = LABELS["SERVICIOS"]
            
            paths =  find_paths(tree, ss.option)
            level_labels = [">".join(path) for path in paths]
            op = st.selectbox("Label correcto: ", level_labels)
            correccion = st.button("Corregir")

            if correccion:
                ss.dataframe.iloc[ss.counter]["LABEL"] = op

            if ss.counter == ss["last_index"]:
                update = st.button("Update")

            show_df = st.checkbox('Show raw data')

            # show dataframe is checkbox selected
            if show_df:
                st.dataframe(ss.dataframe, use_container_width=True)


# st.write(fn.azar(ss.dataframe, "CONFIDENCE"))
        st.write(bearings_keywords["KEYWORDS"])
        st.write(search_keywords(ss.dataframe, bearings_keywords["KEYWORDS"]))