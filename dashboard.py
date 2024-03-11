import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
sns.set(style='dark')


data = pd.read_csv("all_data.csv")

#membuat header
st.header('e-commerce :sparkles:')

#logo perusahaan 
img = Image.open('ecommerce logo.png')
st.sidebar.image(img)

#convert datatype orders from object to be datetime.
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])

# dataframe date
datetime_columns = ["order_purchase_timestamp", "order_delivered_customer_date"]
data.sort_values(by="order_purchase_timestamp", inplace=True)
data.reset_index(inplace=True)

min_date = data["order_purchase_timestamp"].min()
max_date = data["order_purchase_timestamp"].max()

# Mengambil start_date & end_date dari date_input
with st.sidebar:
        start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
     )

# komponen filter
st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = data.order_id.sum()
    st.metric("freight_value", value=total_orders)
 
with col2:
    total_revenue = data.payment_value.sum()
    st.metric("payment_value", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    data["order_purchase_timestamp"],
    data["order_id"],
    marker='o',
    linewidth=2,
    color="#90CAF9"
 )

ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# #Customer state
def create_bystate_df(data):
    bystate_df = data.groupby(by="customer_state").customer_id.nunique().reset_index()
    return bystate_df 

# # Total orders
def create_sum_order_items_df(data):
    sum_order_items_df = data.groupby("product_id").quantity_x.sum().sort_values(ascending=False).reset_index()
    return sum_order_items_df


# Customer demographic
st.subheader("Customer Demographics")
fig, ax = plt.subplots(figsize=(20,10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count",
    y="state",
    data=bystate_df.sort_values(by="customer_count", ascending=False),
    palette=colors,
    ax=ax
 )
ax.set_title("Number of Customer by States", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)