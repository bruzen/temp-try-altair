import streamlit as st
import altair as alt
from vega_datasets import data

# Load the iris dataset
source = data.iris()

# Set up the Streamlit app
st.title('Interactive Faceted Scatter Plot with Marginal Histograms')

# Define the scales
xscale = alt.Scale(domain=(4.0, 8.0))
yscale = alt.Scale(domain=(1.9, 4.55))

# Define the bar arguments
bar_args = {'opacity': 0.3, 'binSpacing': 0}

# Create a slider to select the range of data
data_range = st.slider('Data Range', 0, len(source), (0, len(source)), key='data_range')

# Filter the data based on the selected range
filtered_data = source[data_range[0]:data_range[1]]

# Create the scatter plot
points = alt.Chart(filtered_data).mark_circle().encode(
    alt.X('sepalLength:Q', scale=xscale),
    alt.Y('sepalWidth:Q', scale=yscale),
    color='species:N'
)

# Create the top histogram
top_hist = alt.Chart(filtered_data).mark_bar(**bar_args).encode(
    alt.X('sepalLength:Q', bin=alt.Bin(maxbins=20, extent=xscale.domain), stack=None, title=''),
    alt.Y('count()', stack=None, title=''),
    alt.Color('species:N')
).properties(height=60)

# Create the right histogram
right_hist = alt.Chart(filtered_data).mark_bar(**bar_args).encode(
    alt.Y('sepalWidth:Q', bin=alt.Bin(maxbins=20, extent=yscale.domain), stack=None, title=''),
    alt.X('count()', stack=None, title=''),
    alt.Color('species:N')
).properties(width=60)

# Combine the plots using facet
plot = top_hist & (points | right_hist)

# Display the plot
st.altair_chart(plot, use_container_width=True)
