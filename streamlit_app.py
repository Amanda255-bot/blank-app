import streamlit as st

st.title(" GlobalBiz Insights App: Navigating the Business Landscape in 2020")
st.markdown("""
   🌎 **Explore key insights about the largest companies across the globe.**<br><br>
    💡📈🔍📊 **This app allows you to analyze the  Market Value, Geographic Distribution, and Financial Performance of the World’s Top Companies with Historical Data from 2020**!
""", unsafe_allow_html=True)

st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True) # adding some space between the subtitle and the first visualization


import pandas as pd
import numpy as np
import matplotlib.pyplot as pyplot
import plotly.express as px
import pycountry
from geopy.geocoders import Nominatim

df = pd.read_csv("updated_data_v2.csv")


country_data = df.groupby('Country').agg(
    Number_of_companies=('Company', 'count')
).reset_index()


def get_country_code(country_name):
    try:
        country = pycountry.countries.get(name=country_name)
        return country.alpha_3 if country else None
    except:
        return None

country_data['Country_code'] = country_data['Country'].apply(get_country_code)


fig = px.scatter_geo(country_data,
                     locations="Country_code",  # ISO Alpha-3 country codes
                     size="Number_of_companies",  # Bubble size corresponds to the number of companies
                     hover_name="Country",  # Show country name on hover
                     text="Number_of_companies",  # Show the number of companies on the map
                     title="Number of Leading Companies by Country in 2020",
                     projection='natural earth',  # Specify the map projection
                     color="Country",  # Color bubbles by country
                     color_discrete_sequence=px.colors.qualitative.Set1)



fig.update_traces(marker=dict(sizemode='area',  # Set size mode to area for proportional sizes
                             size=country_data['Number_of_companies']*10))  # Increased bubble size


# Adjust layout for centering and zooming
fig.update_layout(
    geo=dict(
        center=dict(lat=0, lon=0),  # Center the map at (0,0) for better alignment
        projection_scale=3.5,  # Adjust the zoom level by changing the scale (higher = zoomed out more)
    ),

)

# Update geo properties for better visual appeal
fig.update_geos(
    showcoastlines=True, 
    coastlinecolor="Black", 
    showland=True, 
    landcolor="lightgray",  # Color for land
    showocean=False,  # Show ocean
    oceancolor="lightblue", 
    showframe = False

)

fig.update_layout(
    geo=dict(
        projection_scale=2.5,  # Zoom level control
        projection_type="mercator",  # Use Mercator projection for the map
    ),
    showlegend = False,
    height=900,  # Set the height of the map
    width=1200,   # Set the width of the map
)


fig.update_traces(
    textfont=dict(
        color='black',  # Set the font color to black
        size=12,  # Adjust the font size as needed
        family='Arial'  # Font family for the numbers
    )
)

# Display the plot in Streamlit
st.plotly_chart(fig)

# Create a barchart

df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

# Sort data by Sales and select the top 20 companies
top_20_sales = df.nlargest(20, 'Sales')

# Create the bar chart
fig = px.bar(
    top_20_sales, 
    x='Company', 
    y='Sales',
    labels={'Sales': 'Total Sales (in billions)'},
    color='Sales',
    color_continuous_scale='Blues'
)

# Rotate x-axis labels for readability
fig.update_layout(xaxis_tickangle=-45)

# Display the chart in Streamlit
st.title("Top 20 Companies by Sales in 2020")
st.plotly_chart(fig)


# Assuming df is your DataFrame with 'Continent' and 'Profits' columns
continent_profits = df.groupby('Continent').agg(Total_Profit=('Profits', 'sum')).reset_index()

# Sort by Total_Profit
continent_profits_sorted = continent_profits.sort_values(by='Total_Profit', ascending=False)

# Identify the smallest slices (combine the last two smallest continents)
smallest_slices = continent_profits_sorted.tail(2)
others_profit = smallest_slices['Total_Profit'].sum()  # Sum the profits of the two smallest
others_label = "Other"  # Name the combined category

# Remove the smallest two rows
continent_profits_sorted = continent_profits_sorted.iloc[:-2]

# Create a new DataFrame for the 'Other' slice
other_df = pd.DataFrame({ 'Continent': [others_label], 'Total_Profit': [others_profit] })

# Concatenate the new 'Other' row with the rest of the data
continent_profits_sorted = pd.concat([continent_profits_sorted, other_df], ignore_index=True)

# Display the title using Markdown with custom HTML styling
st.markdown("<h3 style='font-size: 16px; font-weight: bold;'>Distribution of Profits of the top 2000 companies globally per Continent in 2020</h3>", unsafe_allow_html=True)


# Plot the pie chart using the new DataFrame
fig_pie, ax = pyplot.subplots(figsize=(6, 6))  # Adjust the size of the chart

# Create the pie chart with the new combined slice
wedges, texts, autotexts = ax.pie(continent_profits_sorted['Total_Profit'], 
       labels=None,  
       autopct='%1.1f%%', 
       startangle=90, 
       textprops={'fontsize': 8, 'ha': 'center','fontweight': 'bold'},
       labeldistance=1.7,
       pctdistance=0.8,   # Keep percentages closer to the center of the slices
       wedgeprops={'width': 0.4}  # Set width for the slices
)

# Equal aspect ratio ensures that the pie chart is drawn as a circle
ax.axis('equal')

# Add legend (show continent names outside the chart)
ax.legend(wedges, continent_profits_sorted['Continent'], title="Continents", loc="center left", bbox_to_anchor=(1.2, 0.5))



for autotext in autotexts:
    x, y = autotext.get_position()  # Get current position
    autotext.set_position((x, y)) 

# Display pie chart in Streamlit
st.pyplot(fig_pie)


# Create a bubble chart to illustrate the market values per country

country_market_value = df.groupby('Country').agg(
    Total_Market_Value=(' Market Value', 'sum')  # Sum the market values per country
).reset_index()

country_market_value['Log_Market_Value'] = np.log(country_market_value['Total_Market_Value'])

fig = px.scatter(
    country_market_value, 
    x='Country',  
    y='Total_Market_Value', 
    size='Total_Market_Value',  
    color='Total_Market_Value',  
    color_continuous_scale='Blues',  
    title="Market Value Distribution of Companies by Country in 2020<br>(Market values are in billions USD)",
    hover_name='Country', 
    log_y=True,  
)

# Update layout for better visibility
fig.update_layout(
    height=800,  # Increase the height for better visibility
    width=1500,  # Increase the width for better layout
    showlegend=False  # Disable the legend, since the color scale is enough
)

# Customize the font of the labels
fig.update_traces(
    marker=dict(
        line=dict(width=1, color='DarkSlateGrey')  # Add borders to bubbles for better visibility
    )
)

fig.update_xaxes(showticklabels=False)

for autotext in autotexts:
    autotext.set_color('white') 


# Show the bubble chart in Streamlit
st.plotly_chart(fig)


selected_country = st.selectbox(
    "Pick a country to access country-specific data:",
    df['Country'].unique()  # Use unique values for countries
)

st.markdown("<br>", unsafe_allow_html=True)  # Adds space before the title

# Filter the DataFrame based on the selected country
filtered_data = df[df['Country'] == selected_country]

# Select only the relevant columns
selected_columns = ["Global Rank", "Company", "Sales", "Profits", " Market Value", "Continent"]
filtered_data = filtered_data[selected_columns]

# Display the key data and filtered information
st.markdown(f"<h2 style='font-size: 20px; font-weight: bold;'>Key Data of the Top Companies in {selected_country} in 2020 </h2>", unsafe_allow_html=True)
st.write("(All values are in billion USD)")
st.write(filtered_data)

















