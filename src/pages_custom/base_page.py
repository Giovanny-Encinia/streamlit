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

class base:
    def __init__(self, page_name:str="main"):
        self.page_name = page_name
        self.last_index = "last_index"+page_name
        self.counter = "counter"+page_name
        self.dataframe = "dataframe"+page_name
        pass
    
    def create_top(self):
        col1, col2, col3 = st.columns([2, 2, 5])

        with col1:
            image = Image.open("src/images/logo.png")
            st.image(image)

        with col3:
            imagen = Image.open("src/images/MicrosoftTeams-image.png")
            st.image(imagen)

        st.title("Procurement Labeling Tool Cemex")

        if self.last_index not in ss:
            ss[self.last_index] = 0

        if self.counter not in ss:
            ss[self.counter] = 0
    
    def create_sidebar(self):
        with st.sidebar.form("Input"):
            now = datetime.datetime.now()
            two_weeks_ago= now - datetime.timedelta(weeks=2)
            label_option = set(ss.LABELS.keys()).union(ss.LABELS["SERVICIOS"].keys())
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
                
                ss[self.counter] = 0
                sql_params = dict(sample=ss.samples, start_date=ss.start_date, end_date=ss.end_date)
                query = DUMMY_QUERY.format(**sql_params)
                df = load_data(query)
                # df_inference = load_data(QUERY_RECORD_INFERENCE.format(option))
                ss[self.last_index] = df.shape[0] - 1
                df = df.rename(columns = {"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"})
                df["LABELED"] = False
                
                if ss[self.last_index]  > 0:
                    ss[self.datafrane] = df
                else:
                    st.warning("No result, there is not data")

    def get_dataframe(self, df:pd.DataFrame):
        ss[self.dataframe] = df

    def main_content(self):
        selectbox_label = "What type of filter do you want to apply"
        type_filter = ["Keywords", "Max Cost", "Threshold", "All data"]
        select_box_option = st.selectbox(selectbox_label, type_filter, key=self.page_name)  
        col1, col2, col3 = st.columns(3)

        # there exist the posibility that the query is void
        if self.dataframe not in ss or ss[self.last_index] <= 0:
            ss[self.dataframe] = pd.DataFrame([], ss.COLUMNS_FRONTEND)
            st.dataframe(ss[self.dataframe],  use_container_width=True)
        elif self.dataframe in ss:
            ss[self.last_index] = ss[self.dataframe].shape[0] - 1

            if ss[self.counter] < ss[self.last_index]:
                col3.button("Next", on_click=next)
            
            if ss.counter > 0:
                col1.button("Previous", on_click=previous) 

            st.dataframe(ss[self.dataframe].iloc[ss[self.counter]].loc[ss.COLUMNS_FRONTEND],  use_container_width=True)
            check = st.radio("Label:", ('Correct', 'Incorrect'))
            st.write("No entiendo")
            if check == "Incorrect":
                tree = ss.LABELS

                if ss.option not in  ["BEARINGS AND ACCESORIES", "DIESEL"]:
                    tree = ss.LABELS["SERVICIOS"]
                
                paths =  find_paths(tree, ss.option)
                level_labels = [">".join(path) for path in paths]
                op = st.selectbox("Label correcto: ", level_labels)
                correccion = st.button("Corregir")

                if correccion:
                    ss[self.dataframe].iloc[ss[self.counter]]["LABEL"] = op

                if ss.counter == ss[self.last_index]:
                    update = st.button("Update")

                show_df = st.checkbox('Show raw data')

                # show dataframe is checkbox selected
                if show_df:
                    st.dataframe(ss[self.dataframe], use_container_width=True)