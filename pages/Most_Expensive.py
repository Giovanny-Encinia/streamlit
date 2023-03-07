from src.pages_custom.base_page import base
from streamlit import session_state as ss
from src.funciones import tree_functions
from src.utils import load_states

load_states()

# query
if "main" not in ss:
    main = base("main")
    main.create_sidebar()
    expensive = base("expensive")
elif "dataframemain" in ss:
    expensive = base("expensive")
    expensive.create_sidebar()

expensive.create_top()

if "dataframemain" in ss and not ss.dataframemain.empty:
    # st.write(ss.dataframemain["PUR_AMOUNT_USD"].dtypes)

    # if ss.dataframemain["PUR_AMOUNT_USD"].dtypes == "object":
    #     ss.dataframemain["PUR_AMOUNT_USD"] = ss.dataframemain["PUR_AMOUNT_USD"].apply(
    #         lambda x: np.random.uniform(low=10, high=10000)
    #     )

    # expensive.get_dataframe(search_maximum_cost(ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"]))
    tree_functions(ss.dataframemain, ss["load_keywords_dict"][ss.option]["KEYWORDS"])
    expensive.main_content()
else:
    pass
