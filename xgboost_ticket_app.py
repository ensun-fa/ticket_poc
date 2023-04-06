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
spec_VCT_enc = load_pickle("spec_VCT_encoder")
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
    bid_date = st.date_input("Job bid date")
    serv_date = st.date_input("Job servicing date")
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

# Convert numerical inputs as floats
trips = float(trips)
cleans = float(cleans)
cr_min = float(cr_min)
cr_max = float(cr_max)
sqft = float(sqft)
sqft_price = float(sqft_price)
crew_best = float(crew_best)

# Process the inputs
mean_crew = (cr_max + cr_min) / 2
avg_client_cost_per_tix = avg_client_cost_dict[client]
bid_conversion_dur = (serv_date - bid_date).days

spec_fixtures_encoded = spec_fixtures_enc.transform([spec_fixtures])
spec_VCT_encoded = spec_VCT_enc.transform([spec_vct])
zelle_encoded = zelle_enc.transform([zelle])
sp_city_encoded = city_enc.transform([sp_city])
sp_state_encoded = sp_state_enc.transform([sp_state])
market_encoded = market_enc.transform([job_market])

quote_items = [q1, q2, q3, q4, q5, q6, q7, q8]
count_quote_items = len([x for x in quote_items if x != "None"])
line_items = [x for x in quote_items if x != "None"]
line_items = sorted(line_items)
line_items = '_'.join([i for i in line_items])
line_items_encoded = line_items_dict.get(line_items, np.median(list(line_items_dict.values())))


with col4:
    st.write("Predicted job cost")
    st.write(":green[$1,227.49]")
    st.write("Mean crew: ", f"{mean_crew}")
    st.write("Avg Client Cost Per Tix: ", f"${avg_client_cost_per_tix:,.2f}")
    st.write("Encoded fixtures specification: ", f"{spec_fixtures_encoded[0]}")
    st.write("Quote items count: ", f"{count_quote_items}")
    st.write("Encoded VCT specification: ", f"{spec_VCT_encoded[0]}")
    st.write("Encoded eligible for Zelle: ", f"{zelle_encoded[0]}")
    st.write("Encoded SP city of operations: ", f"{sp_city_encoded[0]}")
    st.write("Encoded SP state of operations: ", f"{sp_state_encoded[0]}")
    st.write("Encoded job market: ", f"{market_encoded[0]}")
    st.write("Bid conversion duration: ", f"{bid_conversion_dur}")
    st.write("Encoded line items: ", f"{line_items_encoded:,.2f}")
