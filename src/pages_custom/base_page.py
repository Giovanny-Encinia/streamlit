# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com
import streamlit as st
from streamlit import session_state as ss
import time
from PIL import Image
from src.utils import read_load_json, find_paths, load_data, snowflake_connection
from src.queries.select import DUMMY_QUERY, QUERY_SPEND, QUERY_RECORD
import datetime
import pandas as pd
from src.funciones import search_keywords, search_maximum_cost


class base:
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.last_index = "last_index" + page_name
        self.counter = "counter" + page_name
        self.dataframe = "dataframe" + page_name
        pass

    def next(self):
        """
        Move the counter in the streamlit global state dictionary to the next index.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """

        if ss[self.counter] > ss[self.last_index] - 1:
            ss[self.counter] = ss[self.last_index]
        else:
            ss[self.counter] += 1

    def previous(self):
        """
        Move the counter in the streamlit global state dictionary to the previous index.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        ss[self.counter] -= 1

        if ss[self.counter] < 0:
            ss[self.counter] = 0

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
        with st.sidebar.form(key=self.page_name + "form"):
            # initialize the sidebar options
            if "option" not in ss:
                ss["option"] = "MAQUINARIA Y EQUIPO"

            if "samples" not in ss:
                ss["samples"] = 10

            if "start_date" not in ss:
                ss["start_date"] = datetime.datetime.now() - datetime.timedelta(weeks=2)

            if "end_date" not in ss:
                ss["end_date"] = datetime.datetime.now()

            # remember exist servicios servicios, so this can be repeated, this is the reason wich need the union
            label_option = set(ss.LABELS.keys()).union(ss.LABELS["SERVICIOS"].keys())
            # save in a list labels, this is, each time user selections a new label, save labels for a good visualization
            label_option_list = list(label_option)
            label_option_list.insert(0, ss["option"])
            option = st.selectbox(
                "Which database do you want to validate?", label_option_list
            )
            start_date = st.date_input("Select begin date", value=ss["start_date"])
            end_date = st.date_input("Select end date", value=ss["end_date"])
            samples = st.number_input(
                "How many samples do you want?: ",
                min_value=10,
                max_value=10000,
                value=ss["samples"],
            )
            # Every form must have a submit button.
            submitted = st.form_submit_button("Get data")

            if submitted:
                ss["samples"] = samples
                ss["option"] = option
                ss["start_date"] = start_date
                ss["end_date"] = end_date

                # each time it exits a request all the counter have to be 0
                for key in ss:
                    if "counter" in key:
                        ss[key] = 0

                if "is_ready" in ss:
                    st.write("Succes")
                else:
                    ss["is_ready"] = False

                ss[self.counter] = 0

                if ss.option in ss["load_keywords_dict"]:
                    keywords_search = ss["load_keywords_dict"][ss.option]["KEYWORDS"]
                    keywords_search = (
                        "(UPPER(PUR_PO_TEXT) LIKE '%"
                        + "%' OR UPPER(PUR_PO_TEXT) LIKE '%".join(keywords_search)
                        + "%')"
                    )
                else:
                    # This is  always FALSE then the return value is only the predicted like the option
                    keywords_search = "1 = 2 "

                sql_params = dict(
                    sample=ss.samples,
                    start_date=ss.start_date.strftime("%Y-%m-%d"),
                    end_date=ss.end_date.strftime("%Y-%m-%d"),
                    pur_line_desc=ss.option.replace(" ", ""),
                    keywords_search=keywords_search,
                )
                # for test use dummy data
                query = QUERY_SPEND.format(**sql_params)
                # True is for prod connection
                df = load_data(query, True)
                df = df.drop(columns="PUR_PO_TEXT")
                df_inference = load_data(QUERY_RECORD)
                df_merged = pd.merge(
                    df,
                    df_inference,
                    on=[
                        "PUR_COUNTRY",
                        "PUR_PO_NUM",
                        "PUR_PO_ITEM",
                        "PUR_PO_DOC_TYPE",
                        "PUR_PO_MATDOC",
                        "PUR_PO_IT_MATDOC",
                        "PUR_C_COST_TYPE",
                        "PUR_ADD_COST_TYPE",
                    ],
                )
                ss[self.last_index] = df_merged.shape[0] - 1
                st.write("submit sidebar")
                st.write(ss[self.last_index])
                # df = df.rename(
                #     columns={"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"}
                # )
                df["LABELED"] = False

                if ss[self.last_index] >= 0:
                    ss["dataframemain"] = df_merged
                    ss[self.page_name] = True
                    ss["submit"] = True
                    ss["black_list_index"] = []
                    st.write(self.page_name)
                else:
                    st.warning("No result, there is not datajajajaj")
                    ss["dataframemain"] = pd.DataFrame([], ss.COLUMNS_FRONTEND)
                    ss[self.dataframe] = pd.DataFrame([], ss.COLUMNS_FRONTEND)

    def get_dataframe(self, df: pd.DataFrame):
        ss[self.last_index] = df.shape[0] - 1
        ss[self.dataframe] = df

    def main_content(self):
        col1, col2, col3 = st.columns(3)

        # in main self.dataframe is 'dataframemain' and each selkect option independent of the page
        # is saved in this state
        if (
            self.dataframe in ss
            and not ss[self.dataframe].empty
            and not ss["dataframemain"].empty
        ):
            if ss[self.counter] < ss[self.last_index]:
                col3.button("Next", on_click=self.next, key=self.page_name + "next")

            if ss[self.counter] > 0:
                col1.button(
                    "Previous", on_click=self.previous, key=self.page_name + "prev"
                )

            st.write(ss[self.dataframe].shape)
            end = ss[self.dataframe].shape[0]
            actual = ss[self.counter]
            st.write(f"{actual + 1}/{end}")
            st.dataframe(
                ss[self.dataframe]
                .reset_index()
                .iloc[ss[self.counter]]
                .loc[ss.COLUMNS_FRONTEND],
                use_container_width=True,
            )
            check = st.radio(
                "Label:", ("Correct", "Incorrect"), key=self.page_name + "radio"
            )

            if check == "Incorrect":
                tree = ss.LABELS

                if ss.option not in ["BEARINGS AND ACCESORIES", "DIESEL"]:
                    tree = ss.LABELS["SERVICIOS"]

                paths = find_paths(tree, ss.option)
                level_labels = [">".join(path) for path in paths]
                op = st.selectbox("Label correcto: ", level_labels)
                correccion = st.button("Corregir", key=self.page_name + "correct")

                if correccion:
                    # ss[self.dataframe].iloc[ss[self.counter]]["LABEL"] = op
                    pass

                if ss[self.counter] == ss[self.last_index]:
                    update = st.button("Update", key=self.page_name + "update")

                show_df = st.checkbox("Show raw data")

                # show dataframe is checkbox selected
                if show_df:
                    st.dataframe(ss[self.dataframe], use_container_width=True)
