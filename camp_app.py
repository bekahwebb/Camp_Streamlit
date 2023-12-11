#dashboard code
import streamlit as st
import pandas as pd
import plotly.express as px

st.cache_data.clear()
# Read the CSV file into a DataFrame
camp_data = pd.read_csv('nps_camp.csv')
# Display top regions by average cost
top_regions = camp_data.groupby('City')['Cost'].mean().nlargest(5).reset_index()
st.title("National Park Costs for Camping:")
st.subheader("Module 1:")
st.write("Top US Cities by Average Cost of Nearby National Park Campgrounds")
st.dataframe(top_regions)
# Create an input for selecting a city
st.subheader("Average Cost of Nearby National Park Campgrounds") 
selected_city = st.selectbox('Select a US City', camp_data['City'].unique())


# Filter data for the selected city and plot the cost
city_data = camp_data[camp_data['City'] == selected_city]
if not city_data.empty:
    fig = px.scatter(city_data, x='Park Code', y='Cost', color='City',
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     labels={'Cost': 'Cost'})
    st.plotly_chart(fig)
else:
    st.write(f'No data found for {selected_city}')

# Display top costs by zip code count
top_costs = camp_data.groupby('Cost')['Zip'].count().nlargest(5).reset_index()
st.subheader("Module 2:")
st.write("Number of Zipcodes with a Campground of a Certain 'Cost'")
st.dataframe(top_costs)
# Create an input for selecting a cost
selected_cost = st.selectbox('Select a Campground Cost', camp_data['Cost'].unique())
# Filter data for the selected cost and display it
cost_data = camp_data[camp_data['Cost'] == selected_cost]
if not cost_data.empty:
    st.write(f'Data for Cost {selected_cost}')
    st.dataframe(cost_data)
else:
    st.write(f'No data found for Cost {selected_cost}')

# Sidebar with filter options
st.sidebar.header('Filter Options')
# Multi-select widget for selecting 'Park Codes'
selected_park_codes = st.sidebar.multiselect('Select Park Codes to view Lat, Long, and Cost', camp_data['Park Code'].unique())
# Filter data based on selected 'Park Codes'
selected_columns = ["Latitude", "Longitude", "Park Code", "Cost"]
filtered_data = camp_data[selected_columns]
filtered_data = filtered_data.dropna()
filtered_data = filtered_data[filtered_data['Park Code'].isin(selected_park_codes)]
# Display the filtered data in a table
st.subheader("Module 3:")
st.write("Filtered Data for Parks: Latitude, Longitude, Park Codes, and Cost (See left drop down window):")
st.table(filtered_data)
# Display the map with all markers (not filtered)
#st.cache_data.clear()
#st.map.clear()
st.subheader("Module 4:")
st.subheader("Map with all the National Park Campsites:")
st.map(camp_data.dropna(), latitude='Latitude', longitude='Longitude', size = "Cost")

