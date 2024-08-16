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

st.markdown("### BTS Overall")

bts = df[df['campaign'].str.contains('bts')]

# st.write(bts.head())

ovr = bts.groupby(["country", "channel_group", "channel"])[["Sessions", "Costs", "gmv", "Orders", "Ad_clicks", "Ad_impressions"]].sum()
ovr = ovr.query("channel == 'sd' | channel == 'shp' | channel == 'asc' | channel == 'webtraffic' | channel == 'traffic'").query("country  == 'SA' | country == 'AE'")
ovr = ovr[ovr["Costs"] != 0]
ovr['CIR'] = 1/(ovr['Revenue']/ovr['Costs'])
ovr['CPC'] = (ovr['Costs']/ovr['Ad_clicks'])
ovr['CPS'] = (ovr['Costs']/ovr['Sessions'])
ovr['CPM'] = (ovr['Costs']/ovr['Ad_impressions'])*1000
ovr['CTR'] = (ovr['Ad_clicks']/ovr['Ad_impressions'])
ovr['CTS'] = (ovr['Sessions']/ovr['Ad_clicks'])
ovr['CVR'] = (ovr['Orders']/ovr['Sessions'])

st.write(ovr.head(40))


st.markdown("## Google Shopping")

def extract_cat(text):
    parts = text.split('_')
    if len(parts) >= 10:
        return parts[9]
    else:
        return None

st.markdown("### AE")

shp = bts.query("channel == 'shp'")
shp['category'] = shp['campaign'].apply(extract_cat)
# st.write(shp.head(10))

ae = shp.query("country == 'AE'")
ae = ae.groupby("category")[["Sessions", "Costs", "gmv", "Orders", "Ad_clicks", "Ad_impressions"]].sum()
ae['CIR'] = 1/(ae['Revenue']/ae['Costs'])
ae['CPC'] = (ae['Costs']/ae['Ad_clicks'])
ae['CPS'] = (ae['Costs']/ae['Sessions'])
ae['CPM'] = (ae['Costs']/ae['Ad_impressions'])*1000
ae['CTR'] = (ae['Ad_clicks']/ae['Ad_impressions'])
ae['CTS'] = (ae['Sessions']/ae['Ad_clicks'])
ae['CVR'] = (ae['Orders']/ae['Sessions'])
ae = ae.query("Costs > 0")

st.write(ae.head(40))

st.markdown("### SA")

sa = shp.query("country == 'SA'")
sa = sa.groupby("category")[["Sessions", "Costs", "gmv", "Orders", "Ad_clicks", "Ad_impressions"]].sum()
sa['CIR'] = 1/(sa['Revenue']/sa['Costs'])
sa['CPC'] = (sa['Costs']/sa['Ad_clicks'])
sa['CPS'] = (sa['Costs']/sa['Sessions'])
sa['CPM'] = (sa['Costs']/sa['Ad_impressions'])*1000
sa['CTR'] = (sa['Ad_clicks']/sa['Ad_impressions'])
sa['CTS'] = (sa['Sessions']/sa['Ad_clicks'])
sa['CVR'] = (sa['Orders']/sa['Sessions'])
sa = sa.query("Costs > 0")


st.write(sa.head(40))

st.markdown("## SD Report")

sd = bts.query("channel == 'sd'")

sd = sd.groupby(["country", "lang"])[["Sessions", "Costs", "gmv", "Orders", "Ad_clicks", "Ad_impressions"]].sum()

sd = sd[sd["Costs"] != 0]

st.write(sd.head(10))

st.markdown("## Overall spends by Day")

spends = bts.query("channel == 'asc' | channel == 'sd' | channel == 'shp' | channel == 'traffic' | channel == 'webtraffic'").query("country == 'SA' | country == 'AE'")
pivot_table = spends.pivot_table(index=['country', 'channel'], columns='date', values=['Costs'], aggfunc='sum')

st.write(pivot_table.head(30))


st.markdown("## Shopping spends by date")

st.markdown("### AE SHP by date")

spends = shp.query("country == 'AE'")
pivot_table = spends.pivot_table(index=['category'], columns='date', values=['Costs'], aggfunc='sum')
pivot_table.fillna('-', inplace=True)
# filtered_pivot = pivot_table.query('Costs.sum(axis=1) != 0')
# wsum = pivot_table.sum(axis=1)
# st.write(type(wsum))
# pivot_table = pivot_table[wsum != 0]
st.write(pivot_table.head(100))

st.markdown("### SA SHP by date")

spends = shp.query("country == 'SA'")
pivot_table = spends.pivot_table(index=['category'], columns='date', values=['Costs'], aggfunc='sum')
pivot_table.fillna('-', inplace=True)
st.write(pivot_table.head(100))