import pandas as pd
import streamlit as st


# Main function para llamar a las demas
def mainDf(dataframe, column):
    d1 = azar(dataframe)
    d2 = threshold(dataframe, column)
    # d3 = keywords(dataframe,column)
    result = pd.concat(d1, d2)
    return result


# Funcion random
def azar(dt, col):
    df = dt[dt[col] > 0.8].sample(frac=0.4, replace=False, random_state=1)
    return df


# Funcion para % de confianza
def threshold(dataframe):
    return dataframe.query("CONFIDENCE < 0.8").reset_index()


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

    mask = df["PUR_PO_TEXT"].str.contains("|".join(keywords))
    return df[mask].reset_index()


def search_maximum_cost(
    df: pd.DataFrame, columns: str = "PUR_AMOUNT_USD", n: int = 15
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
    return df.nlargest(n, "PUR_AMOUNT_USD").reset_index()
