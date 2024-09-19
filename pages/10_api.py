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

if 't_week_q' not in st.session_state:
    st.session_state['t_week_q'] = 0
else:
    t_week_q = st.session_state.t_week_q


def extract_os(text):
    parts = text.split('_')
    if len(parts) >= 3:
        return parts[2]
    else:
        return None

def extract_market(text):
    parts = text.split('_')
    if len(parts) >= 2:
        return parts[1]
    else:
        return None
    
df['os'] = df['campaign'].apply(extract_os)
df['market'] = df['campaign'].apply(extract_market)

st.markdown("# API Tables")


install = df.query("channel == 'uac' | channel == 'api' | channel == 'apppromo'").query(t_week_q)
sa = install.query("market == 'sa'")
ae = install.query("market == 'ae'")

sa = sa.groupby(['os', 'channel_group', 'channel'])[['Sessions', 'Costs', 'Ad_clicks', 'Ad_impressions', 'Installs', 'SK_Installs', 'Orders', 'Revenue']].sum()
ae = ae.groupby(['os', 'channel_group', 'channel'])[['Sessions', 'Costs', 'Ad_clicks', 'Ad_impressions', 'Installs', 'SK_Installs', 'Orders', 'Revenue']].sum()

st.markdown("### SA")

st.write(sa.head(20))

st.markdown("### AE")

st.write(ae.head(20))

