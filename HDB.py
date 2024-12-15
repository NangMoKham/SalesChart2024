import pandas as pd
import streamlit as st
import plotly.express as px
st.set_page_config(page_title = "My Home Dashboard",page_icon=':bar_chart:',layout='wide')
df = pd.read_csv('HDBclean.csv')
st.sidebar.header('Please Filter Here: ')
month = st.sidebar.multiselect(
    "Select Month: ",
    options = df['month'].unique(),
    default = df['month'].unique()[:5])
town = st.sidebar.multiselect(
    "Select Town: ",
    options = df['town'].unique(),
    default = df['town'].unique()[:5])
flat_type = st.sidebar.multiselect(
    "Select Flat Type: ",
    options = df['flat_type'].unique(),
    default = df['flat_type'].unique()[:5])
st.title(':bar_chart: Home Dashborad for 2010')
st.markdown('##')
tsum = df['resale_price'].sum()
flat_model = df['flat_model'].nunique()
left_col, right_col = st.columns(2)
with left_col:
    st.subheader('Total Resale Price')
    st.subheader(f'US $ {tsum}')
with right_col:
    st.subheader('Number of Flat Model')
    st.subheader(f' {flat_model}')
df_select = df.query('month == @month and town == @town and flat_type == @flat_type')
sales_by_resale = df_select.groupby('flat_type')['resale_price'].sum()
fig_sales_by_resale = px.bar(
    sales_by_resale,
    x = sales_by_resale.values,
    y = sales_by_resale.index,
    orientation = 'h',
    title = 'sales_by_resale')
a, b, c = st.columns(3)
a.plotly_chart(fig_sales_by_resale, use_container_width = True)

fig_sales_by_town = px.pie(df_select, values='resale_price', names='town', title='Resale by Town')
b.plotly_chart(fig_sales_by_town, use_container_width = True)

sales_by_month = df_select.groupby('month')['resale_price'].sum().sort_values()
fig_sales_by_month = px.bar(
    sales_by_month,
    x = sales_by_month.values,
    y = sales_by_month.index,
    orientation = 'h',
    title = 'sales_by_month')
c.plotly_chart(fig_sales_by_month, use_container_width = True)

d, e = st.columns(2)
fig_line_sales_by_month = px.line(
    df_select,
    x = sales_by_month.values,
    y = sales_by_month.index,
    title = 'Resale by Month')
d.plotly_chart(fig_line_sales_by_month, use_container_width = True)

fig_total_flat_model = px.scatter(
    df,
    x = 'resale_price',
    y = 'flat_model',
    title = 'Resale total amount')
e.plotly_chart(fig_total_flat_model, use_container_width = True)
    