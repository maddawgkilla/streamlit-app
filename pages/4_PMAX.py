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

st.markdown("### SA Categories this week")

tw_df = pmax_df.query(t_week_q).query("country == 'SA' & category != 'all'")
tw_df = tw_df.groupby('category')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_df['CIR'] = 1/(tw_df['Revenue']/tw_df['Costs'])
tw_df['CPC'] = (tw_df['Costs']/tw_df['Ad_clicks'])
tw_df['CPS'] = (tw_df['Costs']/tw_df['Sessions'])
tw_df['CPM'] = (tw_df['Costs']/tw_df['Ad_impressions'])*1000
tw_df['CTR'] = (tw_df['Ad_clicks']/tw_df['Ad_impressions'])
tw_df['CTS'] = (tw_df['Sessions']/tw_df['Ad_clicks'])
tw_df['CVR'] = (tw_df['Orders']/tw_df['Sessions'])

st.write(tw_df.head(15))

st.markdown("### SA Categories Prior week")

lw_df = pmax_df.query(l_week_q).query("country == 'SA' & category != 'all'")
lw_df = lw_df.groupby('category')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_df['CIR'] = 1/(lw_df['Revenue']/lw_df['Costs'])
lw_df['CPC'] = (lw_df['Costs']/lw_df['Ad_clicks'])
lw_df['CPS'] = (lw_df['Costs']/lw_df['Sessions'])
lw_df['CPM'] = (lw_df['Costs']/lw_df['Ad_impressions'])*1000
lw_df['CTR'] = (lw_df['Ad_clicks']/lw_df['Ad_impressions'])
lw_df['CTS'] = (lw_df['Sessions']/lw_df['Ad_clicks'])
lw_df['CVR'] = (lw_df['Orders']/lw_df['Sessions'])

st.write(lw_df.head(15))

st.markdown("### SA Categories WoW")

dif = ((tw_df - lw_df)/lw_df)
st.write(dif.head(15))

st.markdown("### AE Categories this week")

tw_df = pmax_df.query(t_week_q).query("country == 'AE' & category != 'all'")
tw_df = tw_df.groupby('category')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_df['CIR'] = 1/(tw_df['Revenue']/tw_df['Costs'])
tw_df['CPC'] = (tw_df['Costs']/tw_df['Ad_clicks'])
tw_df['CPS'] = (tw_df['Costs']/tw_df['Sessions'])
tw_df['CPM'] = (tw_df['Costs']/tw_df['Ad_impressions'])*1000
tw_df['CTR'] = (tw_df['Ad_clicks']/tw_df['Ad_impressions'])
tw_df['CTS'] = (tw_df['Sessions']/tw_df['Ad_clicks'])
tw_df['CVR'] = (tw_df['Orders']/tw_df['Sessions'])

st.write(tw_df.head(15))

st.markdown("### SA Categories Prior week")

lw_df = pmax_df.query(l_week_q).query("country == 'AE' & category != 'all'")
lw_df = lw_df.groupby('category')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_df['CIR'] = 1/(lw_df['Revenue']/lw_df['Costs'])
lw_df['CPC'] = (lw_df['Costs']/lw_df['Ad_clicks'])
lw_df['CPS'] = (lw_df['Costs']/lw_df['Sessions'])
lw_df['CPM'] = (lw_df['Costs']/lw_df['Ad_impressions'])*1000
lw_df['CTR'] = (lw_df['Ad_clicks']/lw_df['Ad_impressions'])
lw_df['CTS'] = (lw_df['Sessions']/lw_df['Ad_clicks'])
lw_df['CVR'] = (lw_df['Orders']/lw_df['Sessions'])

st.write(lw_df.head(15))

st.markdown("### AE Categories WoW")

dif = ((tw_df - lw_df)/lw_df)
st.write(dif.head(18))

st.markdown("# Language Analysis")

st.markdown("### SA Language This Week")

tw_df = pmax_df.query(t_week_q).query("country == 'SA'")
tw_df = tw_df.groupby('lang')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_df['CIR'] = 1/(tw_df['Revenue']/tw_df['Costs'])
tw_df['CPC'] = (tw_df['Costs']/tw_df['Ad_clicks'])
tw_df['CPS'] = (tw_df['Costs']/tw_df['Sessions'])
tw_df['CPM'] = (tw_df['Costs']/tw_df['Ad_impressions'])*1000
tw_df['CTR'] = (tw_df['Ad_clicks']/tw_df['Ad_impressions'])
tw_df['CTS'] = (tw_df['Sessions']/tw_df['Ad_clicks'])
tw_df['CVR'] = (tw_df['Orders']/tw_df['Sessions'])

st.write(tw_df.head(7))

st.markdown("### SA Language Prior Week")

lw_df = pmax_df.query(l_week_q).query("country == 'SA'")
lw_df = lw_df.groupby('lang')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_df['CIR'] = 1/(lw_df['Revenue']/lw_df['Costs'])
lw_df['CPC'] = (lw_df['Costs']/lw_df['Ad_clicks'])
lw_df['CPS'] = (lw_df['Costs']/lw_df['Sessions'])
lw_df['CPM'] = (lw_df['Costs']/lw_df['Ad_impressions'])*1000
lw_df['CTR'] = (lw_df['Ad_clicks']/lw_df['Ad_impressions'])
lw_df['CTS'] = (lw_df['Sessions']/lw_df['Ad_clicks'])
lw_df['CVR'] = (lw_df['Orders']/lw_df['Sessions'])

st.write(lw_df.head(7))

st.markdown("### SA Language WoW")

dif = ((tw_df - lw_df)/lw_df)
st.write(dif.head(6))

st.markdown("### AE Language This Week")

tw_df = pmax_df.query(t_week_q).query("country == 'AE'")
tw_df = tw_df.groupby('lang')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_df['CIR'] = 1/(tw_df['Revenue']/tw_df['Costs'])
tw_df['CPC'] = (tw_df['Costs']/tw_df['Ad_clicks'])
tw_df['CPS'] = (tw_df['Costs']/tw_df['Sessions'])
tw_df['CPM'] = (tw_df['Costs']/tw_df['Ad_impressions'])*1000
tw_df['CTR'] = (tw_df['Ad_clicks']/tw_df['Ad_impressions'])
tw_df['CTS'] = (tw_df['Sessions']/tw_df['Ad_clicks'])
tw_df['CVR'] = (tw_df['Orders']/tw_df['Sessions'])

st.write(tw_df.head(7))

st.markdown("### AE Language Prior Week")

lw_df = pmax_df.query(l_week_q).query("country == 'AE'")
lw_df = lw_df.groupby('lang')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
lw_df['CIR'] = 1/(lw_df['Revenue']/lw_df['Costs'])
lw_df['CPC'] = (lw_df['Costs']/lw_df['Ad_clicks'])
lw_df['CPS'] = (lw_df['Costs']/lw_df['Sessions'])
lw_df['CPM'] = (lw_df['Costs']/lw_df['Ad_impressions'])*1000
lw_df['CTR'] = (lw_df['Ad_clicks']/lw_df['Ad_impressions'])
lw_df['CTS'] = (lw_df['Sessions']/lw_df['Ad_clicks'])
lw_df['CVR'] = (lw_df['Orders']/lw_df['Sessions'])

st.write(lw_df.head(7))

st.markdown("### AE Language WoW")

dif = ((tw_df - lw_df)/lw_df)
st.write(dif.head(6))

st.markdown("# Language + Category Analysis")

st.markdown("### SA PMAX")

tw_df = pmax_df.query(t_week_q).query("country == 'SA' & category != 'all'")
tw_df = tw_df.groupby(['category', 'lang'])[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_df['CIR'] = 1/(tw_df['Revenue']/tw_df['Costs'])
tw_df['CPC'] = (tw_df['Costs']/tw_df['Ad_clicks'])
tw_df['CPS'] = (tw_df['Costs']/tw_df['Sessions'])
tw_df['CPM'] = (tw_df['Costs']/tw_df['Ad_impressions'])*1000
tw_df['CTR'] = (tw_df['Ad_clicks']/tw_df['Ad_impressions'])
tw_df['CTS'] = (tw_df['Sessions']/tw_df['Ad_clicks'])
tw_df['CVR'] = (tw_df['Orders']/tw_df['Sessions'])

tw_df.reset_index(inplace=True)
st.write(tw_df.head(30))

st.markdown("### AE PMAX")

tw_df = pmax_df.query(t_week_q).query("country == 'AE' & category != 'all'")
tw_df = tw_df.groupby(['category', 'lang'])[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
tw_df['CIR'] = 1/(tw_df['Revenue']/tw_df['Costs'])
tw_df['CPC'] = (tw_df['Costs']/tw_df['Ad_clicks'])
tw_df['CPS'] = (tw_df['Costs']/tw_df['Sessions'])
tw_df['CPM'] = (tw_df['Costs']/tw_df['Ad_impressions'])*1000
tw_df['CTR'] = (tw_df['Ad_clicks']/tw_df['Ad_impressions'])
tw_df['CTS'] = (tw_df['Sessions']/tw_df['Ad_clicks'])
tw_df['CVR'] = (tw_df['Orders']/tw_df['Sessions'])

tw_df.reset_index(inplace=True)
st.write(tw_df.head(30))

st.markdown("# Top vs Remaining")

ggl_df = df.query("channel_group == 'google'")
ggl_df = ggl_df.query(t_week_q)
ggl_df = ggl_df.query("channel == 'pmax'")
ggl_df['ptype'] = ggl_df['campaign'].apply(lambda x: 'remaining' if 'remaining' in x else 'other')
# ggl_df.head()

sa_df = ggl_df.query('country == "SA" & lang == "ar"')
ae_df = ggl_df.query('country == "AE" & lang == "en"')

st.markdown("### SA")

sa_df = sa_df.groupby(['category', 'ptype'])[['Sessions', 'Costs', 'Orders', 'Ad_clicks', 'Revenue']].sum()
sa_df['CPS'] = sa_df['Costs']/sa_df['Sessions']
sa_df['CPA'] = sa_df['Costs']/sa_df['Orders']
sa_df['CPC'] = sa_df['Costs']/sa_df['Ad_clicks']
sa_df['CIR'] = 1/(sa_df['Revenue']/sa_df['Costs'])
st.write(sa_df.head(25))

st.markdown("### AE")

ae_df = ae_df.groupby(['category', 'ptype'])[['Sessions', 'Costs', 'Orders', 'Ad_clicks', 'Revenue']].sum()
ae_df['CPS'] = ae_df['Costs']/ae_df['Sessions']
ae_df['CPA'] = ae_df['Costs']/ae_df['Orders']
ae_df['CPC'] = ae_df['Costs']/ae_df['Ad_clicks']
ae_df['CIR'] = 1/(ae_df['Revenue']/ae_df['Costs'])
st.write(ae_df.head(15))