from src.pages_custom.base_page import base
from streamlit import session_state as ss
from src.funciones import tree_functions
from src.utils import load_states

load_states()

if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    low = base("low")
elif "dataframemain" in ss:
    low = base("low")
    low.create_sidebar()

low.create_top()

if "dataframemain" in ss and not ss.dataframemain.empty:
    # low.get_dataframe(threshold(ss.dataframemain))
    tree_functions(ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"])
    low.main_content()
else:
    pass
