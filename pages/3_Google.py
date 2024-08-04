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

ggl_df = df.query("channel_group == 'google'")
pmax_df = ggl_df.query("channel == 'pmax'")

st.markdown("### This Week's Google Overall")

tw_ggl_df = ggl_df.query(t_week_q)

tw_ggl_df = tw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_ggl_df['CIR'] = 1/(tw_ggl_df['Revenue']/tw_ggl_df['Costs'])
tw_ggl_df['CPC'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CPS'] = (tw_ggl_df['Costs']/tw_ggl_df['Sessions'])
tw_ggl_df['CPM'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_impressions'])*1000
tw_ggl_df['CTR'] = (tw_ggl_df['Ad_clicks']/tw_ggl_df['Ad_impressions'])
tw_ggl_df['CTS'] = (tw_ggl_df['Sessions']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CVR'] = (tw_ggl_df['Orders']/tw_ggl_df['Sessions'])

tw_ggl_df = tw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(tw_ggl_df.head(10))

st.markdown("### Prior Week's Google Overall")

lw_ggl_df = ggl_df.query(l_week_q)

lw_ggl_df = lw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_ggl_df['CIR'] = 1/(lw_ggl_df['Revenue']/lw_ggl_df['Costs'])
lw_ggl_df['CPC'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CPS'] = (lw_ggl_df['Costs']/lw_ggl_df['Sessions'])
lw_ggl_df['CPM'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_impressions'])*1000
lw_ggl_df['CTR'] = (lw_ggl_df['Ad_clicks']/lw_ggl_df['Ad_impressions'])
lw_ggl_df['CTS'] = (lw_ggl_df['Sessions']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CVR'] = (lw_ggl_df['Orders']/lw_ggl_df['Sessions'])

lw_ggl_df = lw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(lw_ggl_df.head(10))

st.markdown("### WoW Google")

dif = ((tw_ggl_df - lw_ggl_df)/lw_ggl_df)
st.write(dif.head(6))

st.markdown("### SA Google This Week")

tw_ggl_df = ggl_df.query(t_week_q).query("country == 'SA'")

tw_ggl_df = tw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_ggl_df['CIR'] = 1/(tw_ggl_df['Revenue']/tw_ggl_df['Costs'])
tw_ggl_df['CPC'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CPS'] = (tw_ggl_df['Costs']/tw_ggl_df['Sessions'])
tw_ggl_df['CPM'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_impressions'])*1000
tw_ggl_df['CTR'] = (tw_ggl_df['Ad_clicks']/tw_ggl_df['Ad_impressions'])
tw_ggl_df['CTS'] = (tw_ggl_df['Sessions']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CVR'] = (tw_ggl_df['Orders']/tw_ggl_df['Sessions'])

tw_ggl_df = tw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(tw_ggl_df.head(10))

st.markdown("### SA Google Prior Week")


lw_ggl_df = ggl_df.query(l_week_q).query("country == 'SA'")

lw_ggl_df = lw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_ggl_df['CIR'] = 1/(lw_ggl_df['Revenue']/lw_ggl_df['Costs'])
lw_ggl_df['CPC'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CPS'] = (lw_ggl_df['Costs']/lw_ggl_df['Sessions'])
lw_ggl_df['CPM'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_impressions'])*1000
lw_ggl_df['CTR'] = (lw_ggl_df['Ad_clicks']/lw_ggl_df['Ad_impressions'])
lw_ggl_df['CTS'] = (lw_ggl_df['Sessions']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CVR'] = (lw_ggl_df['Orders']/lw_ggl_df['Sessions'])

lw_ggl_df = lw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(lw_ggl_df.head(10))


st.markdown("### SA Google WoW")

dif = ((tw_ggl_df - lw_ggl_df)/lw_ggl_df)
st.write(dif.head(6))

st.markdown("### AE Google This Week")

tw_ggl_df = ggl_df.query(t_week_q).query("country == 'AE'")

tw_ggl_df = tw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_ggl_df['CIR'] = 1/(tw_ggl_df['Revenue']/tw_ggl_df['Costs'])
tw_ggl_df['CPC'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CPS'] = (tw_ggl_df['Costs']/tw_ggl_df['Sessions'])
tw_ggl_df['CPM'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_impressions'])*1000
tw_ggl_df['CTR'] = (tw_ggl_df['Ad_clicks']/tw_ggl_df['Ad_impressions'])
tw_ggl_df['CTS'] = (tw_ggl_df['Sessions']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CVR'] = (tw_ggl_df['Orders']/tw_ggl_df['Sessions'])

tw_ggl_df = tw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(tw_ggl_df.head(10))

st.markdown("### AE Google Prior Week")

lw_ggl_df = ggl_df.query(l_week_q).query("country == 'AE'")

lw_ggl_df = lw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_ggl_df['CIR'] = 1/(lw_ggl_df['Revenue']/lw_ggl_df['Costs'])
lw_ggl_df['CPC'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CPS'] = (lw_ggl_df['Costs']/lw_ggl_df['Sessions'])
lw_ggl_df['CPM'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_impressions'])*1000
lw_ggl_df['CTR'] = (lw_ggl_df['Ad_clicks']/lw_ggl_df['Ad_impressions'])
lw_ggl_df['CTS'] = (lw_ggl_df['Sessions']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CVR'] = (lw_ggl_df['Orders']/lw_ggl_df['Sessions'])

lw_ggl_df = lw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(lw_ggl_df.head(10))

st.markdown("### AE Google WoW")

dif = ((tw_ggl_df - lw_ggl_df)/lw_ggl_df)
st.write(dif.head(6))


st.markdown("### GCC Google This Week")

tw_ggl_df = ggl_df.query(t_week_q).query("country != 'AE' & country != 'SA'")

tw_ggl_df = tw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_ggl_df['CIR'] = 1/(tw_ggl_df['Revenue']/tw_ggl_df['Costs'])
tw_ggl_df['CPC'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CPS'] = (tw_ggl_df['Costs']/tw_ggl_df['Sessions'])
tw_ggl_df['CPM'] = (tw_ggl_df['Costs']/tw_ggl_df['Ad_impressions'])*1000
tw_ggl_df['CTR'] = (tw_ggl_df['Ad_clicks']/tw_ggl_df['Ad_impressions'])
tw_ggl_df['CTS'] = (tw_ggl_df['Sessions']/tw_ggl_df['Ad_clicks'])
tw_ggl_df['CVR'] = (tw_ggl_df['Orders']/tw_ggl_df['Sessions'])

tw_ggl_df = tw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(tw_ggl_df.head(10))

st.markdown("### GCC Google Prior Week")

lw_ggl_df = ggl_df.query(l_week_q).query("country != 'AE' & country != 'SA'")

lw_ggl_df = lw_ggl_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_ggl_df['CIR'] = 1/(lw_ggl_df['Revenue']/lw_ggl_df['Costs'])
lw_ggl_df['CPC'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CPS'] = (lw_ggl_df['Costs']/lw_ggl_df['Sessions'])
lw_ggl_df['CPM'] = (lw_ggl_df['Costs']/lw_ggl_df['Ad_impressions'])*1000
lw_ggl_df['CTR'] = (lw_ggl_df['Ad_clicks']/lw_ggl_df['Ad_impressions'])
lw_ggl_df['CTS'] = (lw_ggl_df['Sessions']/lw_ggl_df['Ad_clicks'])
lw_ggl_df['CVR'] = (lw_ggl_df['Orders']/lw_ggl_df['Sessions'])

lw_ggl_df = lw_ggl_df.query("channel == 'sb' | channel == 'pmax' | channel == 'uac' | channel == 'sd' | channel == 'shp'")

st.write(lw_ggl_df.head(10))

st.markdown("### GCC Google WoW")

dif = ((tw_ggl_df - lw_ggl_df)/lw_ggl_df)
st.write(dif.head(6))