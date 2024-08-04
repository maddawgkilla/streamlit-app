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

meta_df = df.query("channel_group == 'meta'")

st.markdown("### This Week Meta Overall")

tw_meta_df = meta_df.query(t_week_q)

tw_meta_df = tw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_meta_df['CIR'] = 1/(tw_meta_df['Revenue']/tw_meta_df['Costs'])
tw_meta_df['CPC'] = (tw_meta_df['Costs']/tw_meta_df['Ad_clicks'])
tw_meta_df['CPS'] = (tw_meta_df['Costs']/tw_meta_df['Sessions'])
tw_meta_df['CPM'] = (tw_meta_df['Costs']/tw_meta_df['Ad_impressions']) * 1000
tw_meta_df['CTR'] = (tw_meta_df['Ad_clicks']/tw_meta_df['Ad_impressions'])
tw_meta_df['CTS'] = (tw_meta_df['Sessions']/tw_meta_df['Ad_clicks'])
tw_meta_df['CVR'] = (tw_meta_df['Orders']/tw_meta_df['Sessions'])

tw_meta_df = tw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(tw_meta_df.replace([np.inf, np.nan], '-').head())

st.markdown("### Prior Week Meta Overall")

lw_meta_df = meta_df.query(l_week_q)

lw_meta_df = lw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_meta_df['CIR'] = 1/(lw_meta_df['Revenue']/lw_meta_df['Costs'])
lw_meta_df['CPC'] = (lw_meta_df['Costs']/lw_meta_df['Ad_clicks'])
lw_meta_df['CPS'] = (lw_meta_df['Costs']/lw_meta_df['Sessions'])
lw_meta_df['CPM'] = (lw_meta_df['Costs']/lw_meta_df['Ad_impressions']) * 1000
lw_meta_df['CTR'] = (lw_meta_df['Ad_clicks']/lw_meta_df['Ad_impressions'])
lw_meta_df['CTS'] = (lw_meta_df['Sessions']/lw_meta_df['Ad_clicks'])
lw_meta_df['CVR'] = (lw_meta_df['Orders']/lw_meta_df['Sessions'])

lw_meta_df = lw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(lw_meta_df.replace([np.inf, np.nan], '-').head())

st.markdown("### Meta WoW")

dif = ((tw_meta_df - lw_meta_df)/lw_meta_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))

st.markdown("### SA Meta This Week")

tw_meta_df = meta_df.query(t_week_q).query("country == 'SA'")

tw_meta_df = tw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_meta_df['CIR'] = 1/(tw_meta_df['Revenue']/tw_meta_df['Costs'])
tw_meta_df['CPC'] = (tw_meta_df['Costs']/tw_meta_df['Ad_clicks'])
tw_meta_df['CPS'] = (tw_meta_df['Costs']/tw_meta_df['Sessions'])
tw_meta_df['CPM'] = (tw_meta_df['Costs']/tw_meta_df['Ad_impressions']) * 1000
tw_meta_df['CTR'] = (tw_meta_df['Ad_clicks']/tw_meta_df['Ad_impressions'])
tw_meta_df['CTS'] = (tw_meta_df['Sessions']/tw_meta_df['Ad_clicks'])
tw_meta_df['CVR'] = (tw_meta_df['Orders']/tw_meta_df['Sessions'])

tw_meta_df = tw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(tw_meta_df.replace([np.inf, np.nan], '-').head())

st.markdown("### SA Meta Prior Week")

lw_meta_df = meta_df.query(l_week_q).query("country == 'SA'")

lw_meta_df = lw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_meta_df['CIR'] = 1/(lw_meta_df['Revenue']/lw_meta_df['Costs'])
lw_meta_df['CPC'] = (lw_meta_df['Costs']/lw_meta_df['Ad_clicks'])
lw_meta_df['CPS'] = (lw_meta_df['Costs']/lw_meta_df['Sessions'])
lw_meta_df['CPM'] = (lw_meta_df['Costs']/lw_meta_df['Ad_impressions']) * 1000
lw_meta_df['CTR'] = (lw_meta_df['Ad_clicks']/lw_meta_df['Ad_impressions'])
lw_meta_df['CTS'] = (lw_meta_df['Sessions']/lw_meta_df['Ad_clicks'])
lw_meta_df['CVR'] = (lw_meta_df['Orders']/lw_meta_df['Sessions'])

lw_meta_df = lw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(lw_meta_df.replace([np.inf, np.nan], '-').head())

st.markdown("### SA Meta WoW")

dif = ((tw_meta_df - lw_meta_df)/lw_meta_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))

st.markdown("### AE Meta This Week")

tw_meta_df = meta_df.query(t_week_q).query("country == 'AE'")

tw_meta_df = tw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_meta_df['CIR'] = 1/(tw_meta_df['Revenue']/tw_meta_df['Costs'])
tw_meta_df['CPC'] = (tw_meta_df['Costs']/tw_meta_df['Ad_clicks'])
tw_meta_df['CPS'] = (tw_meta_df['Costs']/tw_meta_df['Sessions'])
tw_meta_df['CPM'] = (tw_meta_df['Costs']/tw_meta_df['Ad_impressions']) * 1000
tw_meta_df['CTR'] = (tw_meta_df['Ad_clicks']/tw_meta_df['Ad_impressions'])
tw_meta_df['CTS'] = (tw_meta_df['Sessions']/tw_meta_df['Ad_clicks'])
tw_meta_df['CVR'] = (tw_meta_df['Orders']/tw_meta_df['Sessions'])

tw_meta_df = tw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(tw_meta_df.replace([np.inf, np.nan], '-').head())

st.markdown("### AE Meta Prior Week")

lw_meta_df = meta_df.query(l_week_q).query("country == 'AE'")

lw_meta_df = lw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_meta_df['CIR'] = 1/(lw_meta_df['Revenue']/lw_meta_df['Costs'])
lw_meta_df['CPC'] = (lw_meta_df['Costs']/lw_meta_df['Ad_clicks'])
lw_meta_df['CPS'] = (lw_meta_df['Costs']/lw_meta_df['Sessions'])
lw_meta_df['CPM'] = (lw_meta_df['Costs']/lw_meta_df['Ad_impressions']) * 1000
lw_meta_df['CTR'] = (lw_meta_df['Ad_clicks']/lw_meta_df['Ad_impressions'])
lw_meta_df['CTS'] = (lw_meta_df['Sessions']/lw_meta_df['Ad_clicks'])
lw_meta_df['CVR'] = (lw_meta_df['Orders']/lw_meta_df['Sessions'])

lw_meta_df = lw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(lw_meta_df.replace([np.inf, np.nan], '-').head())

st.markdown("### AE Meta WoW")

dif = ((tw_meta_df - lw_meta_df)/lw_meta_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))

st.markdown("### GCC Meta This Week")

tw_meta_df = meta_df.query(t_week_q).query("country != 'AE' & country != 'SA'")

tw_meta_df = tw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_meta_df['CIR'] = 1/(tw_meta_df['Revenue']/tw_meta_df['Costs'])
tw_meta_df['CPC'] = (tw_meta_df['Costs']/tw_meta_df['Ad_clicks'])
tw_meta_df['CPS'] = (tw_meta_df['Costs']/tw_meta_df['Sessions'])
tw_meta_df['CPM'] = (tw_meta_df['Costs']/tw_meta_df['Ad_impressions']) * 1000
tw_meta_df['CTR'] = (tw_meta_df['Ad_clicks']/tw_meta_df['Ad_impressions'])
tw_meta_df['CTS'] = (tw_meta_df['Sessions']/tw_meta_df['Ad_clicks'])
tw_meta_df['CVR'] = (tw_meta_df['Orders']/tw_meta_df['Sessions'])

tw_meta_df = tw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(tw_meta_df.head())

st.markdown("### GCC Meta Prior Week")

lw_meta_df = meta_df.query(l_week_q).query("country != 'AE' & country != 'SA'")

lw_meta_df = lw_meta_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_meta_df['CIR'] = 1/(lw_meta_df['Revenue']/lw_meta_df['Costs'])
lw_meta_df['CPC'] = (lw_meta_df['Costs']/lw_meta_df['Ad_clicks'])
lw_meta_df['CPS'] = (lw_meta_df['Costs']/lw_meta_df['Sessions'])
lw_meta_df['CPM'] = (lw_meta_df['Costs']/lw_meta_df['Ad_impressions']) * 1000
lw_meta_df['CTR'] = (lw_meta_df['Ad_clicks']/lw_meta_df['Ad_impressions'])
lw_meta_df['CTS'] = (lw_meta_df['Sessions']/lw_meta_df['Ad_clicks'])
lw_meta_df['CVR'] = (lw_meta_df['Orders']/lw_meta_df['Sessions'])

lw_meta_df = lw_meta_df.query("channel == 'api' | channel == 'asc' | channel == 'traffic'  | channel == 'webtraffic'")

st.write(lw_meta_df.head())

st.markdown("### GCC Meta WoW")

dif = ((tw_meta_df - lw_meta_df)/lw_meta_df)
st.write(dif.head(6))