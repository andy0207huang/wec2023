# ---WEBAPP---
import pandas as pd
import plotly.express as px
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="WEC 2023 - CO2 Emission",
    page_icon=":bar_chart:",
    layout="centered"
)

# read data
df = pd.read_excel(
    io='WEC 2023-result.xlsx',
    engine='openpyxl',
    usecols='A:P',
    nrows=20
)

dfcsv = pd.read_csv("WEC 2023-result.csv")

# DASHBOARD
st.title(":bar_chart: CO2 Emission Dashboard")
st.markdown("##")
# Metrics
# Row 
st.markdown('### CO2 Emissions Metrics')
col1, col2, col3, col4 = st.columns(4)

total = round(dfcsv['Total CO2 Emissions'].sum(), 2)
newyr = round(dfcsv['New Year Predicted Emissions'].sum(), 2)
avgd = round(dfcsv['Total CO2 Emissions'].mean(),2)

col1.metric("Current", total)
col2.metric("New Year Predicted", newyr, round((newyr-total)/newyr, 2))
col3.metric("Average Director", avgd)
col4.metric("Average Canadian", "1685.49", round((1685.49-avgd)/1685.49, 2))
st.text('**All data is in kg')

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
e = round(dfcsv['Electronic CO2 Emissions'].sum(), 2)
f = round(dfcsv['Food CO2 Emissions'].sum(), 2)
t = round(dfcsv['Transportation CO2 Emissions'].sum(), 2)

labels = 'Transportation Total ' + str(t) + ' kg', 'Food Total ' + str(f) + ' kg', 'Electronics Total ' + str(e) + ' kg'
sizes = [t, f, e]
explode = (0, 0, 0.2)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

# in-dept pie (FOOD)
rm = round(dfcsv['Red Meat'].sum(), 2)
g = round(dfcsv['Grains'].sum(), 2)
d = round(dfcsv['Dairy'].sum(), 2)
labels_food = 'Food (Red Meat) ' + str(rm) + ' kg', 'Food (Grains)' + str(g) + ' kg', 'Food (Dairy)' + str(d) + ' kg'
sizes2 = [rm, g, d]
explode2 = (0.2, 0, 0)
colors2 = ['#FF7F50', '#FF4500', '#FFD700']

fig2, ax2 = plt.subplots()
ax2.pie(sizes2, explode=explode2, labels=labels_food, autopct='%1.1f%%',
        shadow=True, startangle=90, colors = colors2)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig2)

# in-dept pie (TRANSPORTATION)
car = round(dfcsv['Car'].sum(), 2)
w = round(dfcsv['Walking'].sum(), 2)
public = round(dfcsv['Public Transport'].sum(), 2)
labels_trans = 'Transportation (Car) ' + str(car) + ' kg', 'Transportation (Walking) ' + str(w) + ' kg', 'Transportation (Public Transportation) ' + str(public) + ' kg'
sizes3 = [car, w, public]
explode3 = (0.2, 0, 0)
colors3 = ['#797EF6', '#1AA7EC', '#1E2F97']

fig3, ax3 = plt.subplots()
ax3.pie(sizes3, explode=explode3, labels=labels_trans, autopct='%1.1f%%',
        shadow=True, startangle=90, colors=colors3)
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig3)

# in-dept pie (ELECTRONICS)
c = round(dfcsv['Cellphone'].sum(), 2)
tv = round(dfcsv['TV'].sum(), 2)
pc = round(dfcsv['Computer'].sum(), 2)
labels_elec = 'Electronics (Cellphone) ' + str(c) + ' kg', 'Electronic (TV) ' + str(tv) + ' kg', 'Electronics (Computer) ' + str(pc) + ' kg'
sizes4 = [c, tv, pc]
explode4 = (0, 0.2, 0)
colors4 = ['#00FF7F', '#00FF00', '#ADFF2F']

fig4, ax4 = plt.subplots()
ax4.pie(sizes4, explode=explode4, labels=labels_elec, autopct='%1.1f%%',
        shadow=True, startangle=90, colors=colors4)
ax4.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig4)




# FILTER
st.sidebar.header("Please Filter Here:")

username = st.sidebar.multiselect(
    "Select the Username:",
    options=dfcsv["username"].unique(),
    default=dfcsv["username"].unique()
)

df_selection = dfcsv.query(
    "username == @username"
)


# --static--
# CHART 1
st.header("Stacked Bar")
# bar_chart = alt.Chart(df).mark_bar().encode(
#     x = 'username',
#     y= {'rm', 'g', 'd', 'c', 'tv', 'pc', 'car', 'w', 'pt'},
#     color = 'username'
# )
# st.altair_chart(bar_chart, use_container_width=True)

fig, ax = plt.subplots()
dfcsv.plot.bar(x='username',
    y = ['Red Meat', 'Grains', 'Dairy', 'Cellphone', 'TV', 'Computer', 'Car', 'Walking', 'Public Transport'],
    stacked = True,
    ax=ax
)
st.pyplot(fig)

# --dynamic--
# CHART 2


# TABLE
st.header("Scraped Data")
st.dataframe(df_selection)