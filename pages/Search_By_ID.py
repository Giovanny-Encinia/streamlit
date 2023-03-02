# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com
import streamlit as st
from streamlit import session_state as ss
from PIL import Image
from src.utils import load_data, find_paths
from src.queries.select import QUERY_SEARCH_UNIQUE, QUERY_SEARCH_UNIQUE_INFERENCE
import pandas as pd

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

if "COLUMNS_FRONTEND" not in ss:
    ss["COLUMNS_FRONTEND"] = [
        "PUR_PO_TEXT",
        "PUR_COUNTRY",
        "PUR_PO_NUM",
        "PUR_PO_ITEM",
        "PUR_PO_DOC_TYPE",
        "PUR_PO_MATDOC",
        "PUR_PO_IT_MATDOC",
        "PUR_C_COST_TYPE",
        "PUR_VENDOR_NAME",
        "PUR_AMOUNT_USD",
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
    "ZFR",
    "NB",
]
add_cost_list = [
    ss["add_cost_type"],
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
        query_inference = QUERY_SEARCH_UNIQUE_INFERENCE.format(**sql_params)
        df_inference = load_data(query_inference).drop(columns="PUR_PO_TEXT")
        # df_inference = load_data(QUERY_RECORD_INFERENCE.format(option))
        ss["last_indexid"] = df.shape[0] - 1
        # df = df.rename(
        #     columns={"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"}
        # )
        df["LABELED"] = False

        if ss["last_indexid"] > 0:
            ss["dataframeid"] = df
            ss["dataframeinferenceid"] = df_inference
            ss["id"] = True
        else:
            st.warning("No result, there is not data")
            ss["dataframeid"] = pd.DataFrame([], ss.COLUMNS_FRONTEND)
            ss["dataframeinferenceid"] = pd.DataFrame([], ss.COLUMNS_FRONTEND)

col1, col2, col3 = st.columns(3)

if "dataframeid" in ss and not ss["dataframeid"].empty:
    ss["dataframeid"] = ss["dataframeid"].query(
        "PUR_PO_ITEM == @ss['item'] and PUR_PO_IT_MATDOC == @ss['it_matdoc']"
    )
    ss["last_indexid"] = ss["dataframeid"].shape[0] - 1
    df_merged = pd.merge(
        ss["dataframeid"],
        ss["dataframeinferenceid"],
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
    ss["dataframemergedid"] = df_merged
    st.dataframe(
        ss["dataframemergedid"].iloc[0].loc[ss["COLUMNS_FRONTEND"]],
        use_container_width=True,
    )
    check = st.radio("Label:", ("Correct", "Incorrect"), key="id" + "radio")

    if check == "Incorrect":
        label_option_correct = set(ss.LABELS.keys()).union(
            ss.LABELS["SERVICIOS"].keys()
        )
        # save in a list labels, this is, each time user selections a new label, save labels for a good visualization
        label_optioncorrect_list = list(label_option_correct)
        ss["optioncorrect"] = st.selectbox(
            "Choose a category", label_optioncorrect_list
        )

        tree = ss.LABELS

        if ss.optioncorrect not in ["BEARINGS AND ACCESORIES", "DIESEL"]:
            tree = ss.LABELS["SERVICIOS"]

        paths = find_paths(tree, ss.optioncorrect)
        level_labels = [">".join(path) for path in paths]
        op = st.selectbox("Label correcto: ", level_labels)
        correccion = st.button("Corregir", key="id" + "correct")

        if correccion:
            # ss[self.dataframe].iloc[ss[self.counter]]["LABEL"] = op
            pass
