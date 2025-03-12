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


snap_df = df.query("channel_group == 'snap'")
snap_df.loc[snap_df['campaign'].str.contains('dpa_rmk', case=False, na=False), 'channel'] = 'dpa-rmk'
snap_df.loc[snap_df['campaign'].str.contains('dpa_acq', case=False, na=False), 'channel'] = 'dpa-acq'
snap_df.loc[snap_df['campaign'].str.contains('dpa_open_webtraffic', case=False, na=False), 'channel'] = 'webtraffic'
snap_df.loc[snap_df['campaign'].str.contains('dpa_open_apptraffic', case=False, na=False), 'channel'] = 'apptraffic'

snap_df = snap_df.groupby(['channel', 'date'])[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
snap_df.reset_index()
tw_snap_df = snap_df.query(t_week_q)
lw_snap_df = snap_df.query(l_week_q)

st.markdown("### This week's Snapchat overview")

tw_snap_df = tw_snap_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_snap_df = lw_snap_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_snap_df['CIR'] = 1/(tw_snap_df['Revenue']/tw_snap_df['Costs'])
lw_snap_df['CIR'] = 1/(lw_snap_df['Revenue']/lw_snap_df['Costs'])
tw_snap_df['CPC'] = (tw_snap_df['Costs']/tw_snap_df['Ad_clicks'])
lw_snap_df['CPC'] = (lw_snap_df['Costs']/lw_snap_df['Ad_clicks'])
tw_snap_df['CPS'] = (tw_snap_df['Costs']/tw_snap_df['Sessions'])
lw_snap_df['CPS'] = (lw_snap_df['Costs']/lw_snap_df['Sessions'])
tw_snap_df['CPM'] = (tw_snap_df['Costs']/tw_snap_df['Ad_impressions']) * 1000
lw_snap_df['CPM'] = (lw_snap_df['Costs']/lw_snap_df['Ad_impressions']) * 1000
tw_snap_df['CTR'] = (tw_snap_df['Ad_clicks']/tw_snap_df['Ad_impressions'])
lw_snap_df['CTR'] = (lw_snap_df['Ad_clicks']/lw_snap_df['Ad_impressions'])
tw_snap_df['CTS'] = (tw_snap_df['Sessions']/tw_snap_df['Ad_clicks'])
lw_snap_df['CTS'] = (lw_snap_df['Sessions']/lw_snap_df['Ad_clicks'])
tw_snap_df['CVR'] = (tw_snap_df['Orders']/tw_snap_df['Sessions'])
lw_snap_df['CVR'] = (lw_snap_df['Orders']/lw_snap_df['Sessions'])
tw_snap_df = tw_snap_df.reset_index()
lw_snap_df = lw_snap_df.reset_index()

tw_snap_df.set_index('channel', inplace=True)
lw_snap_df.set_index('channel', inplace=True)

tw_snap_df = tw_snap_df.query("channel == 'appconv' | channel == 'appengage' | channel == 'dpa-rmk' | channel == 'webconv' | channel == 'api' | channel == 'webtraffic' | channel == 'apptraffic' | channel == 'dpa-acq'")
lw_snap_df = lw_snap_df.query("channel == 'appconv' | channel == 'appengage' | channel == 'dpa-rmk' | channel == 'webconv' | channel == 'api' | channel == 'webtraffic' | channel == 'apptraffic' | channel == 'dpa-acq'")


st.write(tw_snap_df.head(10))


## Reinit of the main snap df

snap_df = df.query("channel_group == 'snap'")
snap_df.loc[snap_df['campaign'].str.contains('dpa_rmk', case=False, na=False), 'channel'] = 'dpa-rmk'
snap_df.loc[snap_df['campaign'].str.contains('dpa_acq', case=False, na=False), 'channel'] = 'dpa-acq'
snap_df.loc[snap_df['campaign'].str.contains('dpa_open_webtraffic', case=False, na=False), 'channel'] = 'webtraffic'
snap_df.loc[snap_df['campaign'].str.contains('dpa_open_apptraffic', case=False, na=False), 'channel'] = 'apptraffic'

st.markdown("### SA Snapchat This Week")

tw_snap_df = snap_df.query(t_week_q).query("country == 'SA'")

tw_snap_df = tw_snap_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_snap_df['CIR'] = 1/(tw_snap_df['Revenue']/tw_snap_df['Costs'])
tw_snap_df['CPC'] = (tw_snap_df['Costs']/tw_snap_df['Ad_clicks'])
tw_snap_df['CPS'] = (tw_snap_df['Costs']/tw_snap_df['Sessions'])
tw_snap_df['CPM'] = (tw_snap_df['Costs']/tw_snap_df['Ad_impressions']) * 1000
tw_snap_df['CTR'] = (tw_snap_df['Ad_clicks']/tw_snap_df['Ad_impressions'])
tw_snap_df['CTS'] = (tw_snap_df['Sessions']/tw_snap_df['Ad_clicks'])
tw_snap_df['CVR'] = (tw_snap_df['Orders']/tw_snap_df['Sessions'])

tw_snap_df = tw_snap_df.query("channel == 'api' | channel == 'dpa-rmk' | channel == 'dpa-acq' | channel == 'webtraffic' | channel == 'apptraffic'")

st.write(tw_snap_df.replace([np.inf, np.nan], '-').head())

st.markdown("### SA Snapchat Prior Week")

lw_snap_df = snap_df.query(l_week_q).query("country == 'SA'")

lw_snap_df = lw_snap_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_snap_df['CIR'] = 1/(lw_snap_df['Revenue']/lw_snap_df['Costs'])
lw_snap_df['CPC'] = (lw_snap_df['Costs']/lw_snap_df['Ad_clicks'])
lw_snap_df['CPS'] = (lw_snap_df['Costs']/lw_snap_df['Sessions'])
lw_snap_df['CPM'] = (lw_snap_df['Costs']/lw_snap_df['Ad_impressions']) * 1000
lw_snap_df['CTR'] = (lw_snap_df['Ad_clicks']/lw_snap_df['Ad_impressions'])
lw_snap_df['CTS'] = (lw_snap_df['Sessions']/lw_snap_df['Ad_clicks'])
lw_snap_df['CVR'] = (lw_snap_df['Orders']/lw_snap_df['Sessions'])

lw_snap_df = lw_snap_df.query("channel == 'api' | channel == 'dpa-rmk' | channel == 'dpa-acq' | channel == 'webtraffic' | channel == 'apptraffic'")

st.write(lw_snap_df.replace([np.inf, np.nan], '-').head())

st.markdown("### SA Snapchat WoW")

dif = ((tw_snap_df - lw_snap_df)/lw_snap_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))



st.markdown("### AE Snapchat This Week")

tw_snap_df = snap_df.query(t_week_q).query("country == 'AE'")

tw_snap_df = tw_snap_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_snap_df['CIR'] = 1/(tw_snap_df['Revenue']/tw_snap_df['Costs'])
tw_snap_df['CPC'] = (tw_snap_df['Costs']/tw_snap_df['Ad_clicks'])
tw_snap_df['CPS'] = (tw_snap_df['Costs']/tw_snap_df['Sessions'])
tw_snap_df['CPM'] = (tw_snap_df['Costs']/tw_snap_df['Ad_impressions']) * 1000
tw_snap_df['CTR'] = (tw_snap_df['Ad_clicks']/tw_snap_df['Ad_impressions'])
tw_snap_df['CTS'] = (tw_snap_df['Sessions']/tw_snap_df['Ad_clicks'])
tw_snap_df['CVR'] = (tw_snap_df['Orders']/tw_snap_df['Sessions'])

tw_snap_df = tw_snap_df.query("channel == 'api' | channel == 'dpa-rmk' | channel == 'dpa-acq' | channel == 'webtraffic' | channel == 'apptraffic'")

st.write(tw_snap_df.replace([np.inf, np.nan], '-').head())

st.markdown("### AE Snapchat Prior Week")

lw_snap_df = snap_df.query(l_week_q).query("country == 'AE'")

lw_snap_df = lw_snap_df.groupby('channel')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_snap_df['CIR'] = 1/(lw_snap_df['Revenue']/lw_snap_df['Costs'])
lw_snap_df['CPC'] = (lw_snap_df['Costs']/lw_snap_df['Ad_clicks'])
lw_snap_df['CPS'] = (lw_snap_df['Costs']/lw_snap_df['Sessions'])
lw_snap_df['CPM'] = (lw_snap_df['Costs']/lw_snap_df['Ad_impressions']) * 1000
lw_snap_df['CTR'] = (lw_snap_df['Ad_clicks']/lw_snap_df['Ad_impressions'])
lw_snap_df['CTS'] = (lw_snap_df['Sessions']/lw_snap_df['Ad_clicks'])
lw_snap_df['CVR'] = (lw_snap_df['Orders']/lw_snap_df['Sessions'])

lw_snap_df = lw_snap_df.query("channel == 'api' | channel == 'dpa-rmk' | channel == 'dpa-acq' | channel == 'webtraffic' | channel == 'apptraffic'")

st.write(lw_snap_df.replace([np.inf, np.nan], '-').head())

st.markdown("### AE Snapchat WoW")

dif = ((tw_snap_df - lw_snap_df)/lw_snap_df)
st.write(dif.replace([np.inf, np.nan], '-').head(6))