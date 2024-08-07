import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)

import hmac

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

if 'df' not in st.session_state:
    st.session_state['df'] = 0
else:
    df = st.session_state.df

st.markdown("### With W/O Overlay - Traffic SA")

wwo = df.query("channel == 'traffic' | channel == 'webtraffic'")
wwo = wwo[wwo['campaign'].str.contains('with')]

wwo['type'] = 'with'

wwo.loc[wwo['campaign'].str.contains('without'), 'type'] = 'without'
wwo = wwo.groupby("type")[["Sessions", "Costs", "gmv", "Orders", "Ad_clicks", "Ad_impressions", "Revenue"]].sum()
wwo['CIR'] = 1/(wwo['Revenue']/wwo['Costs'])
wwo['CPC'] = (wwo['Costs']/wwo['Ad_clicks'])
wwo['CPS'] = (wwo['Costs']/wwo['Sessions'])
wwo['CPM'] = (wwo['Costs']/wwo['Ad_impressions'])*1000
wwo['CTR'] = (wwo['Ad_clicks']/wwo['Ad_impressions'])
wwo['CTS'] = (wwo['Sessions']/wwo['Ad_clicks'])
wwo['CVR'] = (wwo['Orders']/wwo['Sessions'])
st.write(wwo.head(10))

# st.markdown("### VC vs Purchase - Traffic SA")
