
import pandas as pd


#Main function para llamar a las demas
def mainDf(dataframe, column):
    d1 = azar(dataframe)
    d2 = threshold(dataframe,column)
    #d3 = keywords(dataframe,column)
    result = pd.concat(d1,d2)
    return result

#Funcion random
def azar(dt, col):
    df = dt[dt[col] > 0.8].sample(frac=0.4, replace=False, random_state=1)
    return df

#Funcion para % de confianza
def threshold(dataframe):
    df = dataframe[dataframe["CONFIDENCE"] < 0.8].sample(frac=0.3, random_state=1)
    return df

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
    mask = df['PUR_PO_TEXT'].str.contains('|'.join(keywords))
    return df[mask]

