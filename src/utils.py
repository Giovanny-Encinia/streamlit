import json
import streamlit as st
import snowflake.connector
import pandas as pd
from streamlit import session_state as ss


def load_keywords():
    keywords = [
        "DIESEL",
        "BEARINGS AND ACCESORIES",
    ]
    path = "src/json/{}_keywords.json"
    keys = {item: read_load_json(path.format(item.split(" ")[0])) for item in keywords}
    return keys


def read_load_json(path: str) -> dict:
    """
    Read and load a JSON file from a specified path.

    Parameters
    ----------
    path : str
        The path to the JSON file.

    Returns
    -------
    dict
        A dictionary containing the data from the JSON file.

    Notes
    -----
    This function uses the `json` module to load a JSON file from a specified path and return the data
    as a dictionary.

    Examples
    --------
    >>> data = read_load_json('path/to/file.json')
    >>> print(data)
    {'key1': 'value1', 'key2': 'value2', 'key3': 'value3'}
    """

    with open(path, encoding="utf-8") as file_json:
        data_json = json.load(file_json)

    return data_json


def find_paths(tree: dict, node: str, path: list = []) -> list:
    """
    Returns a list of all possible paths from the root to leaf nodes in a given tree.

    Parameters
    ----------
    tree : dict
        The tree to search, represented as a dictionary where each key is a node and
        the corresponding value is a dictionary representing the children of that node.
        Leaf nodes are represented as a value of None.
    node : any hashable type
        The current node being traversed in the search.
    path : list, optional
        A list of nodes representing the current path from the root to the current node.
        Default is an empty list.

    Returns
    -------
    list of lists
        A list of all possible paths from the root to leaf nodes in the tree. Each path is
        represented as a list of nodes.

    Examples
    --------
    >>> tree = {"a": {"b": {"c": {"d": None, "e": None}, "f": {"g": None, "h": None}}}}
    >>> paths = find_paths(tree, "a")
    >>> print(paths)
    [['a', 'b', 'c', 'd'], ['a', 'b', 'c', 'e'], ['a', 'b', 'f', 'g'], ['a', 'b', 'f', 'h']]
    """

    if node not in tree:
        return []

    path = path + [node]

    if tree[node] is None:
        return [path]

    paths = []

    for child in tree[node]:
        child_paths = find_paths(tree[node], child, path)

        for child_path in child_paths:
            paths.append(child_path)

    return paths


@st.experimental_singleton
def snowflake_connection(prod: bool = False) -> snowflake.connector:
    """
    Initialize a connection to Snowflake using the specified credentials.

    Parameters
    ----------
    prod : bool
        This is for to make the correct connection to prod database or dev databas

    Returns
    -------
    snowflake.connector.connection.SnowflakeConnection
        A Snowflake connection object.

    Notes
    -----
    This function uses the credentials stored in the `secrets` object of a Streamlit app to connect to Snowflake
    using the `snowflake.connector` library. Once the connection is established, it is stored in the session state
    of the app for reuse in subsequent requests.

    Examples
    --------
    >>> conn = snowflake_connection()
    >>> cur = conn.cursor()
    >>> cur.execute('SELECT COUNT(*) FROM mytable')
    >>> result = cur.fetchone()[0]
    >>> print(result)
    42
    """
    if prod:
        ctx = snowflake.connector.connect(
            **st.secrets["snowflake_prod"], client_session_keep_alive=True
        )
        st.session_state["is_ready"] = True
    else:
        ctx = snowflake.connector.connect(
            **st.secrets["snowflake"], client_session_keep_alive=True
        )
        st.session_state["is_ready"] = True
    return ctx


@st.experimental_memo(ttl=600)
def load_data(query: str, prod: bool = False) -> pd.DataFrame:
    """
    Load data from a Snowflake database using the specified SQL query and save a status connection in a streamlit
    sesion_state like False

    Parameters
    ----------
    query : str
        The SQL query to execute to retrieve the data.
    prod : bool
        This is for to make the correct connection to prod database or dev database

    Returns
    -------
    pd.DataFrame
        A Pandas DataFrame containing the results of the SQL query.

    Notes
    -----
    This function uses the `snowflake_connection` function to establish a connection to the Snowflake database and
    execute the specified SQL query. The results are returned as a Pandas DataFrame, which can be used for data
    analysis and visualization. This function is memoized using the `@st.experimental_memo` decorator to improve
    performance by caching the results of the function for a set amount of time (in this case, 600 seconds or 10
    minutes).

    Examples
    --------
    >>> data = load_data('SELECT * FROM mytable WHERE column1 > 100')
    >>> print(data.head())
           column1  column2  column3
    0         101       10       20
    1         102       20       30
    2         103       30       40
    ...       ...      ...      ...
    """
    if prod:
        conn = snowflake_connection(True)
    else:
        conn = snowflake_connection()

    cur = conn.cursor().execute(query)
    df_headers = pd.DataFrame(cur.description)
    data = cur.fetchall()
    st.session_state["is_ready"] = False
    return pd.DataFrame(data, columns=df_headers["name"])
