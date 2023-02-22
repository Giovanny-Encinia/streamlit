# import streamlit as st
# import time
# from PIL import Image
# import src.funciones as fn
# from src.utils import read_load_json, find_paths, load_data
# from src.queries import DUMMY_QUERY, GET_LABEL_RECORD
  
# # READ JSON file
# LABELS = read_load_json('src/labels.json')

# #Validation signs, whether it was successfully or not.

# c, cc, ccc = st.columns([2, 2, 5])

# with ccc:
#     imagen = Image.open("MicrosoftTeams-image.png")
#     st.image(imagen)

# st.title("Procurement Labeling Tool Cemex")

# if "counter" not in st.session_state:
#     st.session_state["counter"] = 0



# columns_uniqueid = [
#     "PUR_COUNTRY",
#     "PUR_PO_NUM",
#     "PUR_PO_ITEM",
#     "PUR_PO_DOC_TYPE",
#     "PUR_PO_MATDOC",
#     "PUR_PO_IT_MATDOC",
#     "PUR_C_COST_TYPE",
#     "PUR_ADD_COST_TYPE",
# ]

# COLUMNS_FRONTEND = ["PUR_PO_TEXT", "LABEL", "CONFIDENCE", "PUR_COUNTRY", "PUR_VENDOR_NAME", "PUR_PO_UOM"]

# #Sidebar
# with st.sidebar:
#     image = Image.open("logo.png")
#     st.image(image)
#     label_option = set(LABELS.keys()).union(LABELS["SERVICIOS"].keys())
#     option = st.selectbox("Which database do you want to validate?", label_option)
#     samples = st.text_input("How many samples do you want?: ", 10)

#     if "is_ready" not in st.session_state:        
#         st.session_state["is_ready"] = False 

#     if st.session_state["is_ready"]:
#         st.success("Successfully connected to Snowflake")


# #NIVEL_PROBA, columna con el % de confianza de clasificacion
# query = GET_LABEL_RECORD.format("2023-02-12", "2023=03-21")

# df_historic = load_data(query)
# df_last_index = df_historic.shape[0] - 1
# # df_historic = df_historic.rename(columns = {"NIVEL_PREDICTED": "LABEL", "NIVEL_PROBA": "CONFIDENCE"})
# df_historic["LABELED"] = False
# final = df_historic.copy()



# with st.container():  
#     #Functions
#     def next():
#         st.session_state.counter += 1

#         if st.session_state.counter > df_last_index:
#             st.session_state.counter = df_last_index


#     def previous():
#         st.session_state.counter -= 1

#         if st.session_state.counter < 0:
#             st.session_state.counter = 0
        


#     col1, col2, col3 = st.columns(3)

#     if st.session_state.counter < df_last_index:
#         col3.button("Next", on_click=next)
#     else:
#         col3.write("") 

#     if st.session_state.counter > 0:
#         col1.button("Previous", on_click=previous)
#     else:
#         col1.write("") 

#     # if you click very quickly the next or previous button appear bug
#     st.dataframe(df_historic.iloc[st.session_state.counter].loc[COLUMNS_FRONTEND],  use_container_width=True)
    
        

# with st.container():
#     check = st.radio("Label:", ('Correct', 'Incorrect'))

#     if check == "Incorrect":
#         tree = LABELS

#         if option not in  ["BEARINGS AND ACCESORIES", "DIESEL"]:
#             tree = LABELS["SERVICIOS"]
        
#         paths =  find_paths(tree, option)
#         level_labels = [">".join(path) for path in paths]
#         op = st.selectbox("Label correcto: ", level_labels)
#         correccion = st.button("Corregir")

#         if correccion:
#             final.iloc[st.session_state.counter]["LABEL"] = op

# if st.session_state.counter == df_last_index:
#     update = st.button("Update")
#     # st.dataframe(final, use_container_width= True)

# # st.checkbox value defaults to Falses
# show_df = st.checkbox('Show raw data')

# # show dataframe is checkbox selected
# if show_df:
#     st.dataframe(df_historic, use_container_width=True)
