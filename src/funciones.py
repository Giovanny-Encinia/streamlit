import pandas as pd
from streamlit import session_state as ss
import streamlit as st


def tree_functions(
    df: pd.DataFrame, keywords: list, type_filter: str = "expensive"
) -> pd.DataFrame:
    """
    Filter the input DataFrame to only include rows where the 'PUR_PO_TEXT' column
    contains at least one of the keywords in the input list.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to filter.
    keywords : list
        A list of keywords to search for in the 'PUR_PO_TEXT' column.
    type_filter : str
        the filter of the function this can be, filter by low probability
        or by expensive AMOUNT USD

    Returns
    -------
    pandas.DataFrame
        The filtered DataFrame containing only the rows where the 'PUR_PO_TEXT'
        column contains at least one of the keywords.
    """
    # get all the data with keywords from main dataframe
    if ss["submit"]:
        # this is the first time that the user select a filter
        mask = df["PUR_PO_TEXT"].str.upper().str.contains("|".join(keywords))
        # there exist the posibility that the keywords will be less than all the sample
        if mask.sum() < ss["dataframemain"].shape[0] / 3:
            ss["dataframekeywords"] = df[mask]
        else:
            # if the keywods represent more than 30% of the sample
            ss["dataframekeywords"] = df[mask].sample(frac=0.33, random_state=42)

        # st.dataframe(ss.dataframekeywords)
        ss["last_indexkeywords"] = ss["dataframekeywords"].shape[0]

        keywords_index = list(ss["dataframekeywords"].index)
        lowproba_maxcost = df.loc[~df.index.isin(list(keywords_index))]
        limit = len(keywords_index)

        if type_filter == "low_probability":
            lowproba = lowproba_maxcost.query("PUR_LINE_DESC_PREDICTED < 0.9")
            lowproba = lowproba[:limit, :]
            maxcost = lowproba_maxcost.loc[~lowproba_maxcost.index.isin(lowproba.index)]
        # most expensive or main
        else:
            maxcost = lowproba_maxcost.sort_values(
                by=["PUR_AMOUNT_USD"], ascending=False
            )
            maxcost = maxcost.iloc[:limit, :]
            lowproba = lowproba_maxcost.loc[~lowproba_maxcost.index.isin(maxcost.index)]

        ss["dataframeexpensive"] = maxcost.sort_values(
            by=["PUR_AMOUNT_USD"], ascending=False
        )
        ss["last_indexexpensive"] = ss["dataframeexpensive"].shape[0] - 1
        ss["dataframelow"] = lowproba
        ss["last_indexlow"] = ss["dataframelow"].shape[0] - 1

        # this is very important because the function will not be execute again since
        # the user submit another query
        ss["submit"] = False
    else:
        pass
