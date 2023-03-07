# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com
import streamlit as st
from streamlit import session_state as ss
import time
from PIL import Image
from src.utils import read_load_json, find_paths, load_data, snowflake_connection
from src.queries.select import QUERY_SPEND, QUERY_RECORD
from src.queries.create import INSERT_RECORD
import datetime
import pandas as pd
import re


class base:
    def __init__(self, page_name: str):
        self.page_name = page_name
        self.last_index = "last_index" + page_name
        self.counter = "counter" + page_name
        self.dataframe = "dataframe" + page_name
        pass

    def delete_label_keys(self):
        _ = [
            ss.pop(name + self.page_name)
            for name in ("deeplevel", "level1", "correctness")
            if name + self.page_name in ss
        ]

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
            self.delete_label_keys()

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
        self.delete_label_keys()

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

        st.title("Smart Categorization Feedback Tool")

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

                if "BEARINGS AND ACCESORIES" == ss.option or "DIESEL" == ss.option:
                    condition_pred = f"PUR_LINE_DESC_PREDICTED = '{ss.option}'"
                else:
                    ss.option = ss.option.replace(" ", "")
                    condition_pred = f"NIVEL1_PREDICTED = '{ss.option}'"

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
                    condition_pred=condition_pred,
                    keywords_search=keywords_search,
                )
                # Get data dev database
                query = QUERY_SPEND.format(**sql_params)
                # True is for prod connection
                df = load_data(query, True)

                df = df.drop(columns="PUR_PO_TEXT")
                # get data from inference record table
                df_inference = load_data(QUERY_RECORD.format(**sql_params))
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
                df_merged["Labeled"] = False
                ss["indexlabel" + self.page_name] = [
                    False for _ in range(df_merged.shape[0])
                ]
                df_merged["Label"] = " "
                ss["indexlabel_temp" + self.page_name] = [
                    " " for _ in range(df_merged.shape[0])
                ]
                ss[self.last_index] = df_merged.shape[0] - 1

                if ss[self.last_index] >= 0:
                    ss["submit"] = True
                    ss["dataframemain"] = df_merged
                    ss[self.page_name] = True
                    ss["black_list_index"] = []
                    ss["datadictionary"] = {
                        fk_id: [] for fk_id in ss["dataframemain"]["FK_ID"]
                    }
                else:
                    st.warning("No result, there is not data")
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

            end = ss[self.dataframe].shape[0]
            actual = ss[self.counter]

            with col2:
                st.progress((actual + 1) / end)
                st.markdown(
                    f'<div style="text-align: center; font-size: 20px;">{actual + 1}/{end}</div>',
                    unsafe_allow_html=True,
                )

            st.dataframe(
                ss[self.dataframe].iloc[ss[self.counter]].loc[ss.COLUMNS_FRONTEND],
                use_container_width=True,
            )

            # initialize because the others rows
            if "correctness" + self.page_name not in ss:
                ss["correctness" + self.page_name] = " "

            # Chosse Correct or Incorrect
            with st.form("correct_label" + self.page_name, clear_on_submit=True):
                st.write("Is it correct?")
                correctness = st.selectbox(
                    "",
                    [" ", "Correct", "Incorrect"],
                    index=0,
                )
                # Every form must have a submit button.
                submitted = st.form_submit_button("Select and continue")

                if submitted:
                    ss["correctness" + self.page_name] = correctness

            # check option
            if ss["correctness" + self.page_name] == "Incorrect":
                tree = ss.LABELS

                with st.form("insidecorrect_label" + self.page_name):
                    label_option_correct = set(ss.LABELS.keys()).union(
                        ss.LABELS["SERVICIOS"].keys()
                    )
                    # save in a list labels, this is, each time user selections a new label, save labels for a good visualization
                    label_optioncorrect_list = list(label_option_correct)

                    if "level1" + self.page_name not in ss:
                        ss["level1" + self.page_name] = " "

                    optioncorrect = st.selectbox(
                        "Choose a category", label_optioncorrect_list
                    )
                    insidesubmitted = st.form_submit_button("Select and continue")

                    if insidesubmitted:
                        ss["level1" + self.page_name] = optioncorrect

                if ss["level1" + self.page_name] != " ":
                    if ss["level1" + self.page_name] not in [
                        "BEARINGS AND ACCESORIES",
                        "DIESEL",
                    ]:
                        tree = ss.LABELS["SERVICIOS"]

                    paths = find_paths(tree, optioncorrect)
                    level_labels = [">".join(path) for path in paths]

                    with st.form("deep_level" + self.page_name):
                        if "deeplevel" + self.page_name not in ss:
                            ss["deeplevel" + self.page_name] = " "

                        op = st.selectbox("Label correcto: ", level_labels)

                        deeplevelsubmitted = st.form_submit_button("Label")

                        if deeplevelsubmitted:
                            ss["deeplevel" + self.page_name] = op

                    if ss["deeplevel" + self.page_name] != " ":
                        list_levels = op.replace(" ", "").split(">")
                        # ss["datadictionary"]
                        fk_id = ss[self.dataframe].iloc[ss[self.counter]].loc["FK_ID"]
                        list_columns_actualrow = list(
                            ss[self.dataframe]
                            .iloc[ss[self.counter]]
                            .loc[ss["columns_record"]]
                        )
                        list_columns_actualrow[1] = datetime.datetime.utcnow()
                        list_columns_actualrow[3] = "HUMAN_LABELED"
                        list_columns_actualrow[8] = int(
                            re.search(r"\d+", str(list_columns_actualrow[8])).group()
                        )
                        list_columns_actualrow[11] = int(
                            re.search(r"\d+", str(list_columns_actualrow[11])).group()
                        )
                        list_columns_actualrow[14] = "BASE_DATOS"
                        list_columns_actualrow[15] = 1.0
                        list_columns_actualrow[17] = 1.0
                        list_columns_actualrow[19] = 1.0
                        list_columns_actualrow[21] = 1.0
                        list_columns_actualrow[23] = 1.0
                        list_columns_actualrow[25] = 1.0

                        if list_levels[0] == "OTROS":
                            list_columns_actualrow[14] = "OTROS_COD"
                            list_columns_actualrow[16] = "OTROS"
                            list_columns_actualrow[18] = "OTROS"
                        elif list_levels[0] == "BEARINGSANDACCESORIES":
                            list_columns_actualrow[16] = "BEARINGS AND ACCESORIES"
                            list_columns_actualrow[18] = list_levels[1]
                        elif list_levels[0] == "DIESEL":
                            list_columns_actualrow[16] = "DIESEL"
                            list_columns_actualrow[18] = "DIESEL"
                        else:
                            list_columns_actualrow[16] = "SERVICIOS"
                            list_columns_actualrow[18] = list_levels[0]
                            list_columns_actualrow[20] = list_levels[1]
                            list_columns_actualrow[22] = list_levels[2]
                            list_columns_actualrow[24] = list_levels[3]

                        ss["indexlabel_temp" + self.page_name][
                            ss[self.counter]
                        ] = list_levels
                        ss[self.dataframe]["Label"] = ss[
                            "indexlabel_temp" + self.page_name
                        ]

                        ss["datadictionary"][fk_id] = list_columns_actualrow

                        ss["indexlabel" + self.page_name][ss[self.counter]] = True
                        ss[self.dataframe]["Labeled"] = ss[
                            "indexlabel" + self.page_name
                        ]
                        st.write("SUCCESS")
            elif ss["correctness" + self.page_name] == "Correct":
                ss["indexlabel" + self.page_name][ss[self.counter]] = True
                ss[self.dataframe]["Labeled"] = ss["indexlabel" + self.page_name]

            if ss[self.counter] == ss[self.last_index]:
                update = st.button("Update", key=self.page_name + "update")

                if update:
                    items = [
                        (id, row)
                        for id, row in ss["datadictionary"].items()
                        if row != []
                    ]
                    params = []

                    for key, item in items:
                        params.append(item)
                        del ss["datadictionary"][key]

                    cnx = snowflake_connection()
                    cs = cnx.cursor()
                    cs.executemany(INSERT_RECORD, params)

                    pass

            show_df = st.checkbox("Show raw data")

            # show dataframe is checkbox selected
            if show_df:
                st.dataframe(ss[self.dataframe], use_container_width=True)
