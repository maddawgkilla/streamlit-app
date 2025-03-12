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

if 'l_week_q' not in st.session_state:
    st.session_state['l_week_q'] = 0
else:
    l_week_q = st.session_state.l_week_q

tiktok_df = df.query("channel_group == 'tiktok'")
tiktok_df = tiktok_df.groupby(['channel', 'date'])[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tiktok_df.reset_index()

st.markdown("### This week's Tiktok Overview")

tw_tiktok_df = tiktok_df.query(t_week_q)
lw_tiktok_df = tiktok_df.query(l_week_q)


tw_tiktok_df = tw_tiktok_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_tiktok_df = lw_tiktok_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_tiktok_df['CIR'] = 1/(tw_tiktok_df['Revenue']/tw_tiktok_df['Costs'])
lw_tiktok_df['CIR'] = 1/(lw_tiktok_df['Revenue']/lw_tiktok_df['Costs'])
tw_tiktok_df['CPC'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Ad_clicks'])
lw_tiktok_df['CPC'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Ad_clicks'])
tw_tiktok_df['CPS'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Sessions'])
lw_tiktok_df['CPS'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Sessions'])
tw_tiktok_df['CPM'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Ad_impressions']) * 1000
lw_tiktok_df['CPM'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Ad_impressions']) * 1000
tw_tiktok_df['CTR'] = (tw_tiktok_df['Ad_clicks']/tw_tiktok_df['Ad_impressions'])
lw_tiktok_df['CTR'] = (lw_tiktok_df['Ad_clicks']/lw_tiktok_df['Ad_impressions'])
tw_tiktok_df['CTS'] = (tw_tiktok_df['Sessions']/tw_tiktok_df['Ad_clicks'])
lw_tiktok_df['CTS'] = (lw_tiktok_df['Sessions']/lw_tiktok_df['Ad_clicks'])
tw_tiktok_df['CVR'] = (tw_tiktok_df['Orders']/tw_tiktok_df['Sessions'])
lw_tiktok_df['CVR'] = (lw_tiktok_df['Orders']/lw_tiktok_df['Sessions'])
tw_tiktok_df = tw_tiktok_df.reset_index()
lw_tiktok_df = lw_tiktok_df.reset_index()

tw_tiktok_df.set_index('channel', inplace=True)
lw_tiktok_df.set_index('channel', inplace=True)

tw_tiktok_df = tw_tiktok_df.query("channel == 'apppromo' | channel == 'vsa2'")
lw_tiktok_df = lw_tiktok_df.query("channel == 'apppromo' | channel == 'vsa2'")

st.write(tw_tiktok_df.head(10))

## Reinit of the main tiktok df

tiktok_df = df.query("channel_group == 'tiktok'")

st.markdown("### SA Tiktok This Week")

tw_tiktok_df = tiktok_df.query(t_week_q).query("country == 'SA'")

tw_tiktok_df = tw_tiktok_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_tiktok_df['CIR'] = 1/(tw_tiktok_df['Revenue']/tw_tiktok_df['Costs'])
tw_tiktok_df['CPC'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Ad_clicks'])
tw_tiktok_df['CPS'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Sessions'])
tw_tiktok_df['CPM'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Ad_impressions']) * 1000
tw_tiktok_df['CTR'] = (tw_tiktok_df['Ad_clicks']/tw_tiktok_df['Ad_impressions'])
tw_tiktok_df['CTS'] = (tw_tiktok_df['Sessions']/tw_tiktok_df['Ad_clicks'])
tw_tiktok_df['CVR'] = (tw_tiktok_df['Orders']/tw_tiktok_df['Sessions'])

tw_tiktok_df = tw_tiktok_df.query("channel == 'apppromo' | channel == 'vsa2'")

st.write(tw_tiktok_df.replace([np.inf, np.nan], '-').head())

st.markdown("### SA Tiktok Prior Week")

lw_tiktok_df = tiktok_df.query(l_week_q).query("country == 'SA'")

lw_tiktok_df = lw_tiktok_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_tiktok_df['CIR'] = 1/(lw_tiktok_df['Revenue']/lw_tiktok_df['Costs'])
lw_tiktok_df['CPC'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Ad_clicks'])
lw_tiktok_df['CPS'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Sessions'])
lw_tiktok_df['CPM'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Ad_impressions']) * 1000
lw_tiktok_df['CTR'] = (lw_tiktok_df['Ad_clicks']/lw_tiktok_df['Ad_impressions'])
lw_tiktok_df['CTS'] = (lw_tiktok_df['Sessions']/lw_tiktok_df['Ad_clicks'])
lw_tiktok_df['CVR'] = (lw_tiktok_df['Orders']/lw_tiktok_df['Sessions'])

lw_tiktok_df = lw_tiktok_df.query("channel == 'apppromo' | channel == 'vsa2'")

st.write(lw_tiktok_df.replace([np.inf, np.nan], '-').head())

st.markdown("### SA Tiktok WoW")

dif = ((tw_tiktok_df - lw_tiktok_df)/lw_tiktok_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))



st.markdown("### AE Tiktok This Week")

tw_tiktok_df = tiktok_df.query(t_week_q).query("country == 'AE'")

tw_tiktok_df = tw_tiktok_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_tiktok_df['CIR'] = 1/(tw_tiktok_df['Revenue']/tw_tiktok_df['Costs'])
tw_tiktok_df['CPC'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Ad_clicks'])
tw_tiktok_df['CPS'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Sessions'])
tw_tiktok_df['CPM'] = (tw_tiktok_df['Costs']/tw_tiktok_df['Ad_impressions']) * 1000
tw_tiktok_df['CTR'] = (tw_tiktok_df['Ad_clicks']/tw_tiktok_df['Ad_impressions'])
tw_tiktok_df['CTS'] = (tw_tiktok_df['Sessions']/tw_tiktok_df['Ad_clicks'])
tw_tiktok_df['CVR'] = (tw_tiktok_df['Orders']/tw_tiktok_df['Sessions'])

tw_tiktok_df = tw_tiktok_df.query("channel == 'apppromo' | channel == 'vsa2'")

st.write(tw_tiktok_df.replace([np.inf, np.nan], '-').head())

st.markdown("### AE Tiktok Prior Week")

lw_tiktok_df = tiktok_df.query(l_week_q).query("country == 'AE'")

lw_tiktok_df = lw_tiktok_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_tiktok_df['CIR'] = 1/(lw_tiktok_df['Revenue']/lw_tiktok_df['Costs'])
lw_tiktok_df['CPC'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Ad_clicks'])
lw_tiktok_df['CPS'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Sessions'])
lw_tiktok_df['CPM'] = (lw_tiktok_df['Costs']/lw_tiktok_df['Ad_impressions']) * 1000
lw_tiktok_df['CTR'] = (lw_tiktok_df['Ad_clicks']/lw_tiktok_df['Ad_impressions'])
lw_tiktok_df['CTS'] = (lw_tiktok_df['Sessions']/lw_tiktok_df['Ad_clicks'])
lw_tiktok_df['CVR'] = (lw_tiktok_df['Orders']/lw_tiktok_df['Sessions'])

lw_tiktok_df = lw_tiktok_df.query("channel == 'apppromo' | channel == 'vsa2'")

st.write(lw_tiktok_df.replace([np.inf, np.nan], '-').head())

st.markdown("### AE Tiktok WoW")

dif = ((tw_tiktok_df - lw_tiktok_df)/lw_tiktok_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))