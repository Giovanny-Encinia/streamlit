import pandas as pd
from streamlit import session_state as ss
import streamlit as st


# Funcion para % de confianza, WIP
def threshold(dataframe):
    return dataframe.query("PUR_LINE_DESC < 0.75").reset_index()


def search_keywords(df: pd.DataFrame, keywords: list) -> pd.DataFrame:
    """
    Filter the input DataFrame to only include rows where the 'PUR_PO_TEXT' column
    contains at least one of the keywords in the input list.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to filter.
    keywords : list
        A list of keywords to search for in the 'PUR_PO_TEXT' column.

    Returns
    -------
    pandas.DataFrame
        The filtered DataFrame containing only the rows where the 'PUR_PO_TEXT'
        column contains at least one of the keywords.
    """

    # get all the data with keywords from main dataframe
    if ss["submit"]:
        # this is the first time that the user select a filter
        if "black_list_index" not in ss:
            ss["black_list_index"] = []

        mask = df["PUR_PO_TEXT"].str.upper().str.contains("|".join(keywords))

        # there exist the posibility that the keywords will be less than all the sample
        if mask.sum() < ss["dataframemain"].shape[0] / 3:
            result = df[mask]
        else:
            # if the keywods represent more than 30% of the sample
            result = df[mask].sample(frac=0.33, random_state=42)

        result_index = list(result.index)
        ss["black_list_index"] += result_index
        # this is very important because the function will not be execute again since
        # the user submit another query
        ss["submit"] = False

        return result

    return ss["dataframekeywords"]


def search_maximum_cost(
    df: pd.DataFrame,
    keywords: list,
    columns: str = "PUR_AMOUNT_USD",
    n: int = 15,
) -> pd.DataFrame:
    """
    Return the first `top` rows ordered by `columns` in descending order.
    Return the first `top` rows with the largest values in `columns`, in
    descending order. The columns that are not specified are returned as
    well, but not used for ordering.
    This method is equivalent to
    ``df.sort_values(columns, ascending=False).head(n)``, but more
    performant.

    Parameters
    ----------
    n : int
        Number of rows to return.
    columns : label or list of labels
        Column label(s) to order by.
    Returns
    -------
    DataFrame
        The first `n` rows ordered by the given columns in descending
        order.
    """

    # is a new submit over this function
    if ss["submit"]:
        # 
        # get the sample 33% of the most expensive result
        # the keywords always are variant, they can have diferent size
        mask = df["PUR_PO_TEXT"].str.upper().str.contains("|".join(keywords))
        df_keywords = df[mask].sample(frac=0.33, random_state=42)
        index_mask = df_keywords.index
        result = df.loc[~df.index.isin(list(index_mask))]

        new_size = result.shape[0] / 2
        result = result.sort_values(by=["PUR_AMOUNT_USD"], ascending=False)
        result = df.iloc[:int(new_size), :]

        if "black_list_index" not in ss:
            ss["black_list_index"] = []

        # get the data is not in the other tables, most expensive, threshold etc
        ss["black_list_index"] += result_index
        ss["submit"] = False

        return result
    # another function has been selectioned by the user
    # therefore it exists elements in the black list    
    else:
        ss["dataframekeywords"].index

    return ss["dataframekeywords"]

def tree_functions(df: pd.DataFrame, keywords: list, type_filter: str="expensive") -> pd.DataFrame:
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
    st.write(ss["submit"])
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

        
        keywords_index = list(ss["dataframekeywords"].index)
        lowproba_maxcost = df.loc[~df.index.isin(list(keywords_index))]
        limit = len(keywords_index)
        st.write(keywords_index)

        if type_filter == 'low_probability':
            lowproba = lowproba_maxcost.query("PUR_LINE_DESC_PREDICTED < 0.9")
            lowproba = lowproba[:limit, :]
            st.write(lowproba.index)
            maxcost = lowproba_maxcost.loc[~lowproba_maxcost.index.isin(lowproba.index)]  
        # most expensive or main
        else:
           maxcost = lowproba_maxcost.sort_values(by=["PUR_AMOUNT_USD"], ascending=False)
           maxcost = maxcost.iloc[:limit, :]
           st.write(~lowproba_maxcost.index.isin(maxcost.index))
           lowproba = lowproba_maxcost.loc[~lowproba_maxcost.index.isin(maxcost.index)]


        ss["dataframeexpensive"] = maxcost.sort_values(by=["PUR_AMOUNT_USD"], ascending=False)
        ss["dataframelow"] = lowproba
        
        # this is very important because the function will not be execute again since
        # the user submit another query
        ss["submit"] = False
    else:
        pass