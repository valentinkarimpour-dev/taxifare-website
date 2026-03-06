import streamlit as st
import datetime
import requests
import pydeck as pdk
import time

###########################################
url = 'https://taxifare.lewagon.ai/predict'
###########################################

# Light/dark mode toggle
if "light_mode" not in st.session_state:
    st.session_state.light_mode = False

def toggle_mode():
    st.session_state.light_mode = not st.session_state.light_mode

st.button(
    "☀️ Switch to Light Mode" if not st.session_state.light_mode else "🌙 Switch to Dark Mode",
    on_click=toggle_mode
)

bg_color = "#ffffff" if st.session_state.light_mode else "#000000"
text_color = "#000000" if st.session_state.light_mode else "#ffffff"

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{ background-color: {bg_color}; }}
[data-testid="stHeader"] {{ background-color: {bg_color}; }}
[data-testid="stMain"] {{ background-color: {bg_color}; }}
p, label, div {{ color: {text_color}; }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h3 style='color: #F7C948;'>🚕 When is your ride?</h3>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Row 1 — Inputs
col1, col2, col3 = st.columns(3)

with col1:
    datetime_input = st.datetime_input(
        "Select date and time:"
        )
with col2:
    pass_count = st.number_input("How many passengers?", min_value=1, step=1)
with col3:
    st.write("")
    st.write("")
    st.write("🙆‍♂️" * pass_count)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
    <h3 style='color: #F7C948;'>🌍 Where do you want to go?</h3>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)


# Row 1 — Longitudes
col1, col2, col3, col4 = st.columns(4)

with col1:
    pickup_long_input = st.number_input("Pickup longitude", min_value=-74.2591, max_value=-73.7004, value=-73.9855, step=0.0001, format="%.4f")
    pickup_long_input = st.slider("", min_value=-74.2591, max_value=-73.7004, value=pickup_long_input, step=0.0001, format="%.4f", key="pu_lon_slider")

with col2:
    pickup_lat_input = st.number_input("Pickup latitude", min_value=40.4774, max_value=40.9176, value=40.7580, step=0.0001, format="%.4f")
    pickup_lat_input = st.slider("", min_value=40.4774, max_value=40.9176, value=pickup_lat_input, step=0.0001, format="%.4f", key="pu_lat_slider")

with col3:
    dropoff_long_input = st.number_input("Dropoff longitude", min_value=-74.2591, max_value=-73.7004, value=-73.9822, step=0.0001, format="%.4f")
    dropoff_long_input = st.slider("", min_value=-74.2591, max_value=-73.7004, value=dropoff_long_input, step=0.0001, format="%.4f", key="do_lon_slider")

with col4:
    dropoff_lat_input = st.number_input("Dropoff latitude", min_value=40.4774, max_value=40.9176, value=40.7636, step=0.0001, format="%.4f")
    dropoff_lat_input = st.slider("", min_value=40.4774, max_value=40.9176, value=dropoff_lat_input, step=0.0001, format="%.4f", key="do_lat_slider")

params = {"pickup_datetime": str(datetime_input),
          "pickup_longitude": str(pickup_long_input),
          "pickup_latitude": str(pickup_lat_input),
          "dropoff_longitude": str(dropoff_long_input),
          "dropoff_latitude": str(dropoff_lat_input),
          "passenger_count": int(pass_count)
}

prediction = requests.get(url=url, params=params)
# prediction is a Response object — it has .status_code, .text, .json() etc.
fare = prediction.json()["fare"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&display=swap');

div.stButton > button {{
    width: 220%;
    background-color: #e6b800;
    color: {text_color};
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: 0.1rem;
    border: none;
    border-radius: 12px;
    padding: 0.85rem;
    cursor: pointer;
    transition: background-color 0.2s ease;
}}
div.stButton:nth-of-type(2) > button:hover {{
    background-color: #fff4b3;
    color: #000000;
}}
</style>
""", unsafe_allow_html=True)


if st.button("⚡⚡ CALCULATE FARE PRICE ⚡⚡", key="calculate_btn"):
    placeholder = st.empty()
    for i in range(4):
        placeholder.markdown("""
            <div style="text-align: center; font-size: 1.3rem; color: {text_color};">
                🏃 Calculating...
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.3)
        placeholder.markdown("""
            <div style="text-align: center; font-size: 1.3rem; color: {text_color};">
                &nbsp;&nbsp;&nbsp;&nbsp;Calculating... 🏃
            </div>
        """, unsafe_allow_html=True)
        time.sleep(0.1)
    placeholder.empty()
    st.markdown(f"""
        <p style="text-align: center; font-size: 2rem; color: {text_color}; font-weight: bold;">
            🚕 ${fare:.1f}
        </p>
    """, unsafe_allow_html=True)

# Map
midpoint_lat = (pickup_lat_input + dropoff_lat_input) / 2
midpoint_lon = (pickup_long_input + dropoff_long_input) / 2

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=midpoint_lat,
        longitude=midpoint_lon,
        zoom=11
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=[{"position": [pickup_long_input, pickup_lat_input]}],
            get_position="position",
            get_color=[0, 200, 0],
            get_radius=150,
        ),
        pdk.Layer(
            "ScatterplotLayer",
            data=[{"position": [dropoff_long_input, dropoff_lat_input]}],
            get_position="position",
            get_color=[200, 0, 0],
            get_radius=150,
        ),
    ]
), height=400)  # 👈 adjust this value
