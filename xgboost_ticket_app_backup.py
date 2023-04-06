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
city_enc = load_pickle("city_encoder")
market_enc = load_pickle("market_encoder")
sp_state_enc = load_pickle("sp_state_encoder")
spec_fixtures_enc = load_pickle("spec_fixtures_encoder")
zelle_enc = load_pickle("zelle_encoder")

# Load the mappers
avg_client_cost_dict = load_pickle("avg_client_cost_dict")
line_items_dict = load_pickle("line_items_dict")
median_dict = load_pickle("median_dict")
mode_dict = load_pickle("mode_dict")
line_items_list = load_pickle("line_items_list")

# Generate options for select boxes
client_list = avg_client_cost_dict.keys()
client_list = list(client_list)
client_list = client_list[:-1]
client_list.append("No client")

spec_fixtures_list = ["SALES FLOOR", "BACK OF HOUSE", "MINIMAL", "NONE", "YES",
                     "MINIMAL - BOH", "NO", "INCLUDED - STANDARD",
                     "INCLUDED - EXTENSIVE", "SEE NOTES", "STANDARD FIXTURES"]
spec_fixtures_list = sorted(spec_fixtures_list)
spec_vct_list = ["No Strip & Wax", "Strip & Wax", "Yes",  "Scrub & Wax",
                 "Not Applicable"]
spec_vct_list = sorted(spec_vct_list)
zelle_list = ["Eligible", "Not Eligible", "Unknown"]
sp_city_list = load_pickle("sp_city")
sp_state_list = load_pickle("sp_state")
job_market_list = load_pickle("job_market")
line_items_list.insert(0, "None")

st.set_page_config(layout="wide")
st.header("Purple Key - Ticket SP Cost Model POC App")

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    # st.write("## Input parameters to the model:")
    st.write(":orange[Job details]")
    job_market = st.selectbox("Job market", job_market_list)
    trips = st.slider("Trips", 0, 10, 5)
    cleans = st.slider("Number of cleans", 0, 10, 5)
    cr_min = st.slider("Crew Min", 0, 15, 5)
    cr_max = st.slider("Crew Max", 0, 15, 5)
    sqft = st.text_input("Job sqft", value=0)
    sqft_price = st.text_input("Sqft Price", value=0)
    client = st.selectbox("Client", client_list)
    crew_best = st.text_input("Crew Best (Labor hours)", value=0)
    spec_fixtures = st.selectbox("Specs - Fixtures", spec_fixtures_list)
    spec_vct = st.selectbox("Specs - VCT", spec_vct_list)

with col2:
    st.write(":orange[Assigned SP details]")
    zelle = st.selectbox("Is SP Eligible for Zelle?", zelle_list)
    sp_city = st.selectbox("SP's base city", sp_city_list)
    sp_state = st.selectbox("SP's base state", sp_state_list)

with col3:
    st.write(":orange[Quotation details (line items only)]")
    q1 = st.selectbox("Quote item #1", line_items_list)
    q2 = st.selectbox("Quote item #2", line_items_list)
    q3 = st.selectbox("Quote item #3", line_items_list)
    q4 = st.selectbox("Quote item #4", line_items_list)
    q5 = st.selectbox("Quote item #5", line_items_list)
    q6 = st.selectbox("Quote item #6", line_items_list)
    q7 = st.selectbox("Quote item #7", line_items_list)
    q8 = st.selectbox("Quote item #8", line_items_list)

with col4:
    st.write("Predicted job cost")
    st.write(":green[$1227.49]")
# Create Streamlite sidebar panel
# with st.sidebar:
#     st.write("## Input parameters to the model:")
#     st.write("Job details")
#     job_market = st.selectbox("Job market", job_market_list)
#     trips = st.slider("Trips", 0, 10, 5)
#     cleans = st.slider("Number of cleans", 0, 10, 5)
#     cr_min = st.slider("Crew Min", 0, 15, 5)
#     cr_max = st.slider("Crew Max", 0, 15, 5)
#     sqft = st.text_input("Job sqft")
#     sqft_price = st.text_input("Sqft Price")
#     client = st.selectbox("Client", client_list)
#     crew_best = st.text_input("Crew Best (Labor hours)")
#     spec_fixtures = st.selectbox("Specs - Fixtures", spec_fixtures_list)
#     spec_vct = st.selectbox("Specs - VCT", spec_vct_list)

#     st.write("Assigned SP details")
#     zelle = st.selectbox("Is SP Eligible for Zelle?", zelle_list)
#     sp_city = st.selectbox("SP's base city", sp_city_list)
#     sp_state = st.selectbox("SP's base state", sp_state_list)
    
#     st.write("Quotation details (line items only)")
#     q1 = st.selectbox("Quote item #1", line_items_list)
#     q2 = st.selectbox("Quote item #2", line_items_list)
#     q3 = st.selectbox("Quote item #3", line_items_list)
#     q4 = st.selectbox("Quote item #4", line_items_list)
#     q5 = st.selectbox("Quote item #5", line_items_list)
#     q6 = st.selectbox("Quote item #6", line_items_list)
#     q7 = st.selectbox("Quote item #7", line_items_list)
#     q8 = st.selectbox("Quote item #8", line_items_list)

