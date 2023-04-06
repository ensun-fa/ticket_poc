# Import libraries
import streamlit as st
import numpy as np
import pickle

def load_pickle(file_name):
    """
    Helper function to load the trained artifacts from model development
    """
    with open("./files/" + file_name + ".p", "rb") as f:
        return pickle.load(f)


# Load the trained XGBoost model
with open("./files/xgboost3_ticket.p", "rb") as f:
    model = pickle.load(f)

# Load the label encoding artifacts
city_enc = None
market_enc = None
sp_state_enc = None
spec_fixtures_enc = None
zelle_enc = None

encoders = ["city_encoder", "market_encoder", "sp_state_encoder",
            "spec_fixtures_encoder", "zelle_encoder"]
encoder_obj = [city_enc, market_enc, sp_state_enc, spec_fixtures_enc,
               zelle_enc]

for encoder, obj in zip(encoders, encoder_obj):
    obj = load_pickle(encoder)

# Load the mappers
avg_client_cost_dict = None
line_items_dict = None
median_dict = None
mode_dict = None
line_items_list = None

mappers = ["avg_client_cost_dict", "line_items_dict", "median_dict",
           "mode_dict", "line_items_list"]

mapper_obj = [avg_client_cost_dict, line_items_dict, median_dict, 
              mode_dict, line_items_dict]

for mapper, obj in zip(mappers, mapper_obj):
    obj = load_pickle(mapper)

# Create Streamlite sidebar panel
with st.sidebar:
    st.write("Input parameters to the model:")
    trips = st.slider("Trips", min_value="0", max_value="10")
