import streamlit as st
import datetime
import requests
import pydeck as pdk
###########################################
url = 'https://taxifare.lewagon.ai/predict'
###########################################

st.markdown("""
    <style>
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)


'''
### When is your ride?
'''

# Row 1 — Inputs
col1, col2 = st.columns(2)

with col1:
    datetime_input = st.datetime_input(
        "Select date and time:"
        )
with col2:
    pass_count = st.number_input("How many passengers?", min_value=1, step=1)


'''
### Where do you want to go?
'''


# Row 1 — Longitudes
col1, col2 = st.columns(2)

with col1:
    pickup_long_input = st.number_input("Pickup longitude", min_value=-74.2591, max_value=-73.7004, value=-73.9855, step=0.0001, format="%.4f")

with col2:
    dropoff_long_input = st.number_input("Dropoff longitude", min_value=-74.2591, max_value=-73.7004, value=-73.9822, step=0.0001, format="%.4f")

# Row 2 — Latitudes
col1, col2 = st.columns(2)

with col1:
    pickup_lat_input = st.number_input("Pickup latitude", min_value=40.4774, max_value=40.9176, value=40.7580, step=0.0001, format="%.4f")

with col2:
    dropoff_lat_input = st.number_input("Dropoff latitude", min_value=40.4774, max_value=40.9176, value=40.7636, step=0.0001, format="%.4f")

params = {"pickup_datetime": str(datetime_input),
          "pickup_longitude": str(pickup_long_input),
          "pickup_latitude": str(pickup_lat_input),
          "dropoff_longitude": str(dropoff_long_input),
          "dropoff_latitude": str(dropoff_lat_input),
          "passenger_count": str(pass_count)
}

prediction = requests.get(url=url, params=params)
# prediction is a Response object — it has .status_code, .text, .json() etc.

'''
### The estimated price will be:
'''
fare = prediction.json()["fare"]

st.markdown(f"""
    <p style="font-size: 2rem; color: white; font-weight: bold;">
        🚕 ${fare:.1f}
    </p>
""", unsafe_allow_html=True)# this parses the response body into a Python dictionary e.g. {"fare": 12.5}
