import pytest
from src.utils import read_load_json
import json

def test_json_labels():
    
    data_json = read_load_json("src/labels.json")
    labels = ["DIESEL", "BEARINGS AND ACCESORIES", "SERVICIOS"]
    keys = data_json.keys()
    is_true_list = [label in keys for label in labels]
    assert sum(is_true_list), "Value Error"