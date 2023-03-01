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

        if mask.sum < ss["dataframemain"].shape[0] / 3:
            result = df[mask]
        else:
            result = df[mask].sample(frac=0.33, random_state=42)

        result_index = list(result.index)
        ss["black_list_index"] += result_index
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

    if ss["submit"]:
        df = df.sort_values(by=["PUR_AMOUNT_USD"], ascending=False)
        # get the sample 33% of the most expensive result
        mask = df["PUR_PO_TEXT"].str.upper().str.contains("|".join(keywords))
        df_keywords = df[mask].sample(frac=0.33, random_state=42)
        index_mask = df_keywords.index

        limit = ss["dataframemain"].shape[0] / 3
        result = df.iloc[:limit, :]

        if "black_list_index" not in ss:
            ss["black_list_index"] = []

        # get the data is not in the other tables, most expensive, threshold etc
        result = result.loc[~result.index.isin(ss["black_list_index"])]
        result_index = list(result.index)
        ss["black_list_index"] += result_index
        ss["submit"] = False

        return result

    return ss["dataframekeywords"]
