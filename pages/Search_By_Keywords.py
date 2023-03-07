# Carlos Giovanny Encinia Gonzalez
# carlos.encinia@ext.cemex.com
from src.pages_custom.base_page import base
from streamlit import session_state as ss
from src.funciones import tree_functions
from src.utils import load_states

load_states()

if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    keywords = base("keywords")
elif "dataframemain" in ss:
    keywords = base("keywords")
    keywords.create_sidebar()

keywords.create_top()

if "dataframemain" in ss and ss.option != "OTROS" and not ss.dataframemain.empty:
    # st.write("ACCEDE A LA FUNCION CREATE")
    # keywords.get_dataframe(
    #     search_keywords(
    #         ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"]
    #     )
    # )
    tree_functions(ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"])
    keywords.main_content()
else:
    pass
