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

if 'tw_over_df' not in st.session_state:
    st.session_state['tw_over_df'] = 0

if 'lw_over_df' not in st.session_state:
    st.session_state['lw_over_df'] = 0

tw_ovr_df = st.session_state["tw_ovr_df"]
lw_ovr_df = st.session_state["lw_ovr_df"]

st.markdown("### SA Last Week")


tw_chart = tw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple' & country == 'SA'")
tw_chart = tw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_chart['CIR'] = 1/(tw_chart['Revenue']/tw_chart['Costs'])
tw_chart['CPC'] = (tw_chart['Costs']/tw_chart['Ad_clicks'])
tw_chart['CPS'] = (tw_chart['Costs']/tw_chart['Sessions'])
tw_chart['CVR'] = (tw_chart['Orders']/tw_chart['Sessions'])

st.write(tw_chart.head())

st.markdown("### SA Prior Week")

lw_chart = lw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple' & country == 'SA'")
lw_chart = lw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_chart['CIR'] = 1/(lw_chart['Revenue']/lw_chart['Costs'])
lw_chart['CPC'] = (lw_chart['Costs']/lw_chart['Ad_clicks'])
lw_chart['CPS'] = (lw_chart['Costs']/lw_chart['Sessions'])
lw_chart['CVR'] = (lw_chart['Orders']/lw_chart['Sessions'])

st.write(lw_chart.head())

st.markdown("### SA WoW")

dif = ((tw_chart - lw_chart)/lw_chart)
st.write(dif.head())

st.markdown("### AE Last Week")

tw_chart = tw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple' & country == 'AE'")
tw_chart = tw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_chart['CIR'] = 1/(tw_chart['Revenue']/tw_chart['Costs'])
tw_chart['CPC'] = (tw_chart['Costs']/tw_chart['Ad_clicks'])
tw_chart['CPS'] = (tw_chart['Costs']/tw_chart['Sessions'])
tw_chart['CVR'] = (tw_chart['Orders']/tw_chart['Sessions'])

st.write(tw_chart.head())

st.markdown("### AE Prior Week")

lw_chart = lw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple' & country == 'AE'")
lw_chart = lw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_chart['CIR'] = 1/(lw_chart['Revenue']/lw_chart['Costs'])
lw_chart['CPC'] = (lw_chart['Costs']/lw_chart['Ad_clicks'])
lw_chart['CPS'] = (lw_chart['Costs']/lw_chart['Sessions'])
lw_chart['CVR'] = (lw_chart['Orders']/lw_chart['Sessions'])

st.write(lw_chart.head())

st.markdown("### AE WoW")

dif = ((tw_chart - lw_chart)/lw_chart)
st.write(dif.head())

st.markdown("### GCC Last Week")

tw_chart = tw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple' & country != 'AE'").query("country != 'SA'")
tw_chart = tw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_chart['CIR'] = 1/(tw_chart['Revenue']/tw_chart['Costs'])
tw_chart['CPC'] = (tw_chart['Costs']/tw_chart['Ad_clicks'])
tw_chart['CPS'] = (tw_chart['Costs']/tw_chart['Sessions'])
tw_chart['CVR'] = (tw_chart['Orders']/tw_chart['Sessions'])

st.write(tw_chart.head())

st.markdown("### GCC Prior Week")

lw_chart = lw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple' & country != 'AE'").query("country != 'SA'")
lw_chart = lw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_chart['CIR'] = 1/(lw_chart['Revenue']/lw_chart['Costs'])
lw_chart['CPC'] = (lw_chart['Costs']/lw_chart['Ad_clicks'])
lw_chart['CPS'] = (lw_chart['Costs']/lw_chart['Sessions'])
lw_chart['CVR'] = (lw_chart['Orders']/lw_chart['Sessions'])

st.write(lw_chart.head())

st.markdown("### GCC WoW")

dif = ((tw_chart - lw_chart)/lw_chart)
st.write(dif.head())