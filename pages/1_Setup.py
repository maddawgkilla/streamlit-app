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

if "df" not in st.session_state:
    st.session_state.df = None

file = st.file_uploader("Upload CSV", type=["csv"])

if file is not None:
    df = pd.read_csv(file, thousands = ',')
    st.session_state.df = df
    st.success("CSV uploaded successfully!")

if st.session_state.df is not None:
        # st.subheader("Data Preview")
        # st.dataframe(st.session_state.df.head())
        df = st.session_state.df

# st.write("df =", st.session_state.df)

# if 'file' not in st.session_state:
#     st.file_uploader("Please choose a file", key='file')
# else:
#     file = st.session_state['file']

# st.file_uploader("Please choose a file", key='file')

# st.write(st.session_state['file'])
# if 'file' not in st.session_state:
#     file = st.file_uploader("Please choose a file", key='file')
# else:
#     st.write("Else Statement")

# file = st.file_uploader("Please choose a file", key='file')
# st.write(st.session_state.file)

# if 'df' not in st.session_state:
#     df = pd.read_csv(file, thousands = ',')
# else:


# df = pd.read_csv(st.session_state.file, thousands = ',')

df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

df['Sessions'] = pd.to_numeric(df['Sessions'])
df['Costs'] = pd.to_numeric(df['Costs'])
df['Revenue'] = pd.to_numeric(df['gmv'])
df['Orders'] = pd.to_numeric(df['Orders'])
df['Installs'] = pd.to_numeric(df['Installs'])
df['Ad_clicks'] = pd.to_numeric(df['Ad_clicks'])
df['Ad_impressions'] = pd.to_numeric(df['Ad_impressions'])
df['campaign'] = df['campaign'].astype(str)

def extract_lang(text):
    parts = text.split('_')
    if len(parts) >= 4:
        return parts[3]
    else:
        return None

def extract_cat(text):
    parts = text.split('_')
    if len(parts) >= 9:
        return parts[8]
    else:
        return None

df.loc[df['id'].isin(['d1347', 'd1348', 'd1428', 'd1429', 'd1666', 'd1617', 'd1641', 'd1642', 'd1579', 'd1578', 'd1731', 'd1766', 'd1765', 'd1811']), 'channel'] = 'webtraffic'

df['category'] = df['campaign'].apply(extract_cat)
df['lang'] = df['campaign'].apply(extract_lang)

df = df.query("channel_group != 'onsite'")

st.write(df.head())

st.markdown("### Select start and end dates for first period")

if "t_sd" not in st.session_state:
    st.session_state.t_sd = None
if "t_ed" not in st.session_state:
    st.session_state.t_ed = None

if "l_sd" not in st.session_state:
    st.session_state.l_sd = None
if "l_ed" not in st.session_state:
    st.session_state.l_ed = None

st.session_state.t_sd = st.date_input("Starting Date of this period", st.session_state.t_sd)
st.session_state.t_ed = st.date_input("End Date of this period", st.session_state.t_ed)

# st.write(t_sd, t_ed)

st.markdown("### Select start and end dates for previous period")

st.session_state.l_sd = st.date_input("Starting Date of previous period", st.session_state.l_sd)
st.session_state.l_ed = st.date_input("End Date of previous period", st.session_state.l_ed)

t_sd = str(st.session_state.t_sd)
l_sd = str(st.session_state.l_sd)
t_ed = str(st.session_state.t_ed)
l_ed = str(st.session_state.l_ed)

# st.write(t_sd, t_ed, l_ed, l_sd)

t_week_q = "date <= '" + t_ed + "' & date >= '" + t_sd + "'"
l_week_q = "date <= '" + l_ed + "' & date >= '" + l_sd + "'"
# l_week_q = "date <= {l_ed} & date >= {l_sd}"

st.session_state.t_week_q = t_week_q
st.session_state.l_week_q = l_week_q

tw_ovr_df = df.query(t_week_q)
lw_ovr_df = df.query(l_week_q)

tw_chart = tw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple'")
tw_chart = tw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
# tw_chart.set_index('channel_group', inplace=True)
tw_chart['CIR'] = 1/(tw_chart['Revenue']/tw_chart['Costs'])
tw_chart['CPC'] = (tw_chart['Costs']/tw_chart['Ad_clicks'])
tw_chart['CPS'] = (tw_chart['Costs']/tw_chart['Sessions'])
tw_chart['CVR'] = (tw_chart['Orders']/tw_chart['Sessions'])

st.markdown("### This period Overview")

st.write(tw_chart.head())

st.markdown("### Previous period Overview")

lw_chart = lw_ovr_df.query("channel_group != 'rtb' & channel_group != 'prog' & channel_group != 'apple'")
lw_chart = lw_chart.groupby('channel_group')[['Sessions', 'Costs', 'Revenue', 'Orders', 'Ad_clicks', 'Ad_impressions']].sum()
# lw_chart.set_index('channel_group', inplace=True)
lw_chart['CIR'] = 1/(lw_chart['Revenue']/lw_chart['Costs'])
lw_chart['CPC'] = (lw_chart['Costs']/lw_chart['Ad_clicks'])
lw_chart['CPS'] = (lw_chart['Costs']/lw_chart['Sessions'])
lw_chart['CVR'] = (lw_chart['Orders']/lw_chart['Sessions'])

st.write(lw_chart.head())

st.markdown("### WoW Change / Delta between period 1 and 2")

dif = ((tw_chart - lw_chart)/lw_chart)
st.write(dif.head())

st.session_state['tw_ovr_df'] = tw_ovr_df
st.session_state['lw_ovr_df'] = lw_ovr_df
