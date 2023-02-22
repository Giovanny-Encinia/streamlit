import streamlit as st
from streamlit import session_state as ss

def next():
    """
    Move the counter in the streamlit global state dictionary to the next index.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    ss.counter += 1

    if ss.counter > ss["last_index"]:
        ss.counter = ss["last_index"]

def previous():
    """
    Move the counter in the streamlit global state dictionary to the previous index.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    ss.counter -= 1

    if ss.counter < 0:
        ss.counter = 0