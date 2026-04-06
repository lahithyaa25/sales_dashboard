import pandas as pd
import streamlit as st
import plotly.express as px

# Load data
data = pd.read_csv("C:/Users/lahit/OneDrive/Desktop/sales-dashboard/sales_data.csv")

# Convert date column
data['Sale_Date'] = pd.to_datetime(data['Sale_Date'])

# Calculate Revenue
data['Revenue'] = data['Quantity_Sold'] * data['Unit_Price']

# Sidebar filters
st.sidebar.title("Filters")
products = st.sidebar.multiselect("Select Product", data['Product_ID'].unique(), default=data['Product_ID'].unique())
regions = st.sidebar.multiselect("Select Region", data['Region'].unique(), default=data['Region'].unique())

filtered_data = data[(data['Product_ID'].isin(products)) & (data['Region'].isin(regions))]

# KPIs
total_revenue = filtered_data['Revenue'].sum()
total_units = filtered_data['Quantity_Sold'].sum()
avg_order_value = filtered_data['Revenue'].mean()

st.title("Sales & Revenue Dashboard")
st.metric("Total Revenue", f"${total_revenue:,.2f}")
st.metric("Total Units Sold", total_units)
st.metric("Average Order Value", f"${avg_order_value:,.2f}")

# Revenue trend
revenue_trend = filtered_data.groupby('Sale_Date')['Revenue'].sum().reset_index()
fig_trend = px.line(revenue_trend, x='Sale_Date', y='Revenue', title='Revenue Trend Over Time')
st.plotly_chart(fig_trend)

# Top Products
top_products = filtered_data.groupby('Product_ID')['Revenue'].sum().sort_values(ascending=False).head(5)
fig_top = px.bar(top_products, x=top_products.index, y=top_products.values, title='Top 5 Products')
st.plotly_chart(fig_top)

# Regional Revenue
region_perf = filtered_data.groupby('Region')['Revenue'].sum().reset_index()
fig_region = px.pie(region_perf, names='Region', values='Revenue', title='Revenue by Region')
st.plotly_chart(fig_region)