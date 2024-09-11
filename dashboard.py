import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="User and Content Analysis of TV Series Streaming Company", layout="wide")

### READ DATA ###

shows = pd.read_csv('data/shows.csv') 
air_dates = pd.read_csv('data/air_dates.csv') 
production_countries = pd.read_csv('data/production_countries.csv') 
production_companies = pd.read_csv('data/production_companies.csv')
genres = pd.read_csv('data/genres.csv')  
languages = pd.read_csv('data/languages.csv') 
networks = pd.read_csv('data/networks.csv') 
show_votes = pd.read_csv('data/show_votes.csv')  
created_by = pd.read_csv('data/created_by.csv')
created_by_types = pd.read_csv('data/created_by_types.csv')
genre_types = pd.read_csv('data/genre_types.csv')
language_types = pd.read_csv('data/language_types.csv')
links = pd.read_csv('data/links.csv')
link_types = pd.read_csv('data/link_types.csv')
network_types = pd.read_csv('data/network_types.csv')
origin_country_types = pd.read_csv('data/origin_country_types.csv')
production_company_types = pd.read_csv('data/production_company_types.csv')
production_country_types = pd.read_csv('data/production_country_types.csv')
spoken_languages = pd.read_csv('data/spoken_languages.csv')
spoken_language_types = pd.read_csv('data/spoken_language_types.csv')
status = pd.read_csv('data/status.csv')
types = pd.read_csv('data/types.csv')

### SIDEBAR FILTER ###

with st.sidebar:
    st.title("User and Content Analysis of TV Series Streaming Company")
    st.subheader("_Made By: :blue[Datazine]_", divider="gray")

# Sidebar filter
status_choice = st.sidebar.multiselect("Select (1 or more) Status", status["status_name"].sort_values().unique())
if status_choice:
    shows_with_status = shows.merge(
        status, 
        left_on='status_id', 
        right_on='status_id'
    )
    shows2 = shows_with_status[
        shows_with_status['status_name'].isin(status_choice)
    ]
    shows2 = shows2.drop_duplicates(subset='show_id')
else:
    shows2 = shows.copy()

production_country_choice = st.sidebar.multiselect("Select (1 or more) Production Country", production_country_types["production_country_name"].sort_values().unique())
if production_country_choice:
    production_countries_merged = production_countries.merge(
        production_country_types, 
        left_on='production_country_type_id', 
        right_on='production_country_type_id'
    )
    filtered_production_countries = production_countries_merged[
        production_countries_merged['production_country_name'].isin(production_country_choice)
    ]
    shows3 = shows2.merge(
        filtered_production_countries, 
        left_on='show_id', 
        right_on='show_id'
    )
    shows3 = shows3.drop_duplicates(subset='show_id')
else:
    shows3 = shows2.copy()

origin_country_choice = st.sidebar.multiselect("Select (1 or more) Origin Country", origin_country_types["origin_country_name"].sort_values().unique())
if origin_country_choice:
    origin_countries_merged = production_countries.merge(
        origin_country_types, 
        left_on='origin_country_type_id', 
        right_on='origin_country_type_id'
    )
    filtered_origin_countries = origin_countries_merged[
        origin_countries_merged['origin_country_name'].isin(origin_country_choice)
    ]
    shows4 = shows3.merge(
        filtered_origin_countries, 
        left_on='show_id', 
        right_on='show_id'
    )
    shows4 = shows4.drop_duplicates(subset='show_id')
else:
    shows4 = shows3.copy()

### FILTER DATA ###

def format_number(num):
    if num > 1000:
        if not num % 1000:
            return f'{num // 1000} K'
        return f'{round(num / 1000, 2)} K'
    return f'{round(num, 2)}'

# Top 5 genres on the library
genres_merged = genres.merge(genre_types, left_on='genre_type_id', right_on='genre_type_id')
shows_genres = shows4.merge(genres_merged, left_on='show_id', right_on='show_id')
genre_counts = shows_genres.groupby('genre_name').agg(
    count=('show_id', 'size'),
    total_popularity=('popularity', 'mean')
).reset_index()
genre_counts_1 = genre_counts.sort_values(by='count', ascending=False).head(5)
genre_counts_1.columns = ['Genre Name', 'Count', 'Average Popularity']

# Top 5 Most Popular Genres from 20000 shows
top_20000_popular_shows = shows4.sort_values(by='popularity', ascending=False).head(20000)
top_20000_popular_shows = top_20000_popular_shows[top_20000_popular_shows['popularity'] > 0]
genres_merged_1 = genres.merge(genre_types, left_on='genre_type_id', right_on='genre_type_id')
shows_genres_1 = top_20000_popular_shows.merge(genres_merged_1, left_on='show_id', right_on='show_id')
genre_counts_2 = shows_genres_1.groupby('genre_name').agg(
    count=('show_id', 'size'),
    total_popularity=('popularity', 'mean')
).reset_index()
popularity_counts = genre_counts_2.sort_values(by='total_popularity', ascending=False).head(5)
popularity_counts.columns = ['Genre Name', 'Count', 'Average Popularity']




# Display Top 5 Network Companies With Progress Bar
networks_merged = networks.merge(network_types, left_on='network_type_id', right_on='network_type_id')
shows_networks = shows4.merge(networks_merged, left_on='show_id', right_on='show_id')
network_counts = shows_networks.groupby('network_name').agg(
    count=('show_id', 'size'),
).reset_index()
network_counts_1 = network_counts.sort_values(by='count', ascending=False).head(5)
network_counts_1.columns = ['Network Name', 'Count']

# Display Top 5 Spoken Languages With Progress Bar
spoken_languages_merged = spoken_languages.merge(spoken_language_types, left_on='spoken_language_type_id', right_on='spoken_language_type_id')
shows_spoken_languages = shows4.merge(spoken_languages_merged, left_on='show_id', right_on='show_id')
spoken_language_counts = shows_spoken_languages.groupby('spoken_language_name').agg(
    count=('show_id', 'size'),
).reset_index()
spoken_language_counts_1 = spoken_language_counts.sort_values(by='count', ascending=False).head(5)
spoken_language_counts_1.columns = ['Spoken Language Name', 'Count']

# Display Top 5 Types
shows_types = shows4.merge(types, left_on='type_id', right_on='type_id')
type_counts = shows_types.groupby('type_name').agg(
    count=('show_id', 'size'),
).reset_index()
type_counts_1 = type_counts.sort_values(by='count', ascending=False).head(5)
type_counts_1.columns = ['Type', 'Count']

# Display Top Genres in The Most Popular Companies
shows_with_companies = shows4.merge(
    production_companies, left_on='show_id', right_on='show_id'
).merge(
    production_company_types, left_on='production_company_type_id', right_on='production_company_type_id'
)
shows_with_genres = shows_with_companies.merge(
    genres, left_on='show_id', right_on='show_id'
).merge(
    genre_types, left_on='genre_type_id', right_on='genre_type_id'
)
top_production_companies = shows_with_genres['production_company_name'].value_counts().sort_values(ascending=False).head(3).index
shows_top_3_companies = shows_with_genres[shows_with_genres['production_company_name'].isin(top_production_companies)]
pivot_companies = shows_top_3_companies.pivot_table(
    index='production_company_name', 
    columns='genre_name', 
    aggfunc='size', 
    fill_value=0
)
pivot_companies["total"] = pivot_companies.sum(axis=1, numeric_only=True)
pivot_companies = pivot_companies.sort_values(by="total", ascending=False)

# Display New Content Popularity
air_dates_2 = air_dates.copy()
air_dates_2["date"] = pd.to_datetime(air_dates_2["date"])
show_air_dates_2 = top_20000_popular_shows.merge(air_dates_2, left_on='show_id', right_on='show_id')
show_air_dates_2023 = show_air_dates_2[(show_air_dates_2["date"].dt.year >= 2023) & (show_air_dates_2["is_first"] == 1)]
shows_genres_a = show_air_dates_2023.merge(genres_merged, left_on='show_id', right_on='show_id')
genre_counts_3 = shows_genres_a.groupby('genre_name').agg(
    count=('show_id', 'size'),
    total_popularity=('popularity', 'mean')
).reset_index()
new_show_popularity = genre_counts_3.sort_values(by='total_popularity', ascending=False).head(5)
new_show_popularity.columns = ['Genre Name', 'Count', 'Average Popularity']


### DASHBOARD CONTENT ###

st.markdown('<style>div.block-container{padding-top:3rem;}</style>', unsafe_allow_html=True)

# st.dataframe(monthly_popularity.head(50))

cl1, cl2 = st.columns((2))

with cl1:
    st.metric(label="Total of Shows", value=format_number(shows4.shape[0]))
with cl2:
    st.metric(label="Average Popularity", value=format_number(top_20000_popular_shows["popularity"].mean()))


col1, col2 = st.columns((2))

with col1:
    st.markdown("#### Top 5 Genres Stored In Library")
    fig = px.bar(genre_counts_1, x = "Genre Name", y="Count", text=[x for x in genre_counts_1["Count"]],
                 template = "seaborn", hover_name="Genre Name", hover_data={
                     'Genre Name': False,
                     'Average Popularity': False
                 }, color="Count", color_continuous_scale="teal")
    st.plotly_chart(fig,use_container_width=True, height = 200)

with col2:
    st.markdown("#### Top 5 Most Popular Genres")
    fig = px.bar(popularity_counts, x = "Genre Name", y="Average Popularity", text=['{:,.2f}'.format(x) for x in popularity_counts["Average Popularity"]],
                 template = "seaborn", hover_name="Genre Name", hover_data={
                     'Genre Name': False,
                     'Count': False,
                     'Average Popularity': ':.2f'
                 }, color="Average Popularity", color_continuous_scale="teal")
    # fig.update_layout(xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig,use_container_width=True, height = 200)
    st.caption("_From maximum the most popular 20.000 shows and popularity ≠ 0_")


st.markdown("#### Trends of Show Popularity (Jan. 2021 - Dec. 2023)")

## GENRE FILTER 1
genre_trend_choice = st.multiselect("Select (1 or more) Genres to the Line Chart", genre_types["genre_name"].sort_values().unique())
if genre_trend_choice:
    genres_trend_merged = genres.merge(
        genre_types, 
        left_on='genre_type_id', 
        right_on='genre_type_id'
    )
    filtered_genres_trend = genres_trend_merged[
        genres_trend_merged['genre_name'].isin(genre_trend_choice)
    ]
    shows_trend = top_20000_popular_shows.merge(
        filtered_genres_trend, 
        left_on='show_id', 
        right_on='show_id'
    )
    shows_trend = shows_trend.drop_duplicates(subset='show_id')
else:
    shows_trend = top_20000_popular_shows.copy()
# Display Genre Popularity Overtime (Line Chart)
air_dates_1 = air_dates.copy()
air_dates_1["date"] = pd.to_datetime(air_dates_1["date"])
show_air_dates = shows_trend.merge(air_dates_1, left_on='show_id', right_on='show_id')
show_in_range = show_air_dates[
    (show_air_dates['date'] >= '2021-01-01') &
    (show_air_dates['date'] <= '2023-12-31')
]

show_in_range['month_year'] = show_in_range['date'].dt.to_period('M')
monthly_popularity = show_in_range.groupby(['month_year', 'is_first'])['popularity'].mean().reset_index()

monthly_popularity['is_first'] = monthly_popularity['is_first'].replace({1: 'Debut/Premiere', 0: 'Non-Debut/Premiere'})
monthly_popularity.columns = ['Months', 'Debut Status', 'Average Popularity']

monthly_popularity['Months'] = monthly_popularity['Months'].dt.to_timestamp()

monthly_pivot = monthly_popularity.pivot(index='Months', columns='Debut Status', values='Average Popularity')

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=monthly_pivot.index, 
    y=monthly_pivot['Debut/Premiere'], 
    mode='lines+markers',
    name='Debut/Premiere',
    line=dict(color='green')
))

fig.add_trace(go.Scatter(
    x=monthly_pivot.index, 
    y=monthly_pivot['Non-Debut/Premiere'], 
    mode='lines+markers',
    name='Non-Debut/Premiere',
    line=dict(color='orange')
))

fig.update_layout(
    height=500, width=1000,
    xaxis_title='Months',
    yaxis_title='Average Popularity',
    xaxis=dict(type='date'),  
    template="plotly_dark",
    showlegend=True
)

st.plotly_chart(fig, use_container_width=True)


st.markdown("#### Relationship between Popularity and Vote Average")

## GENRE FILTER 2
genre_types_2 = genre_types.copy()
genre_scatter_choice = st.multiselect("Select (1 or more) Genres to the Scatter Chart", genre_types_2["genre_name"].sort_values().unique())
if genre_scatter_choice:
    genres_popularity_merged = genres.merge(
        genre_types_2, 
        left_on='genre_type_id', 
        right_on='genre_type_id'
    )
    filtered_genres_popularity = genres_popularity_merged[
        genres_popularity_merged['genre_name'].isin(genre_scatter_choice)
    ]
    shows_popularity = top_20000_popular_shows.merge(
        filtered_genres_popularity, 
        left_on='show_id', 
        right_on='show_id'
    )
    shows_popularity = shows_popularity.drop_duplicates(subset='show_id')
else:
    shows_popularity = top_20000_popular_shows.copy()

# Correlation Between Popularity And User Vote
show_votes_aggregated = shows_popularity.merge(
    show_votes,
    left_on='show_id', 
    right_on='show_id'
)
show_votes_aggregated = show_votes_aggregated[show_votes_aggregated["vote_count"] >= 20]

scatter_plot = px.scatter(show_votes_aggregated, hover_data={'name': True}, x = "popularity", y = "vote_average", size = "vote_count")
scatter_plot['layout'].update(xaxis = dict(title="Popularity",titlefont=dict(size=19)),
                       yaxis = dict(title = "Vote Average", titlefont = dict(size=19)))
scatter_plot.update_xaxes(autorangeoptions=dict(minallowed=20, maxallowed=1200))
st.plotly_chart(scatter_plot,use_container_width=True)
st.caption("_Only including shows with at least 20 vote counts. The size of the dot indicates how many vote counts._")

column1, column2, column3 = st.columns((3))

with column1:
    st.markdown("#### Top 5 Networks Associated")
    st.dataframe(network_counts_1,
                 column_order=("Network Name", "Count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Network Name": st.column_config.TextColumn(
                        "Network Name",
                    ),
                    "Count": st.column_config.ProgressColumn(
                        "Count",
                        format="%f",
                        min_value=0,
                        max_value=max(network_counts_1["Count"]),
                     )}
                 )
   
with column2:
    st.markdown("#### Top 5 Spoken Languages")
    st.dataframe(spoken_language_counts_1,
                 column_order=("Spoken Language Name", "Count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Spoken Language Name": st.column_config.TextColumn(
                        "Spoken Language Name",
                    ),
                    "Count": st.column_config.ProgressColumn(
                        "Count",
                        format="%f",
                        min_value=0,
                        max_value=max(spoken_language_counts_1["Count"]),
                     )}
                 )
    
with column3:
    st.markdown("#### Top 5 Show Types")
    st.dataframe(type_counts_1,
                 column_order=("Type", "Count"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Type": st.column_config.TextColumn(
                        "Type",
                    ),
                    "Count": st.column_config.ProgressColumn(
                        "Count",
                        format="%f",
                        min_value=0,
                        max_value=max(type_counts_1["Count"]),
                     )}
                 )
    
cols1, cols2 = st.columns((2))

with cols1:
    fig = go.Figure()
    for genre in pivot_companies.columns:
        if genre != "total":
            fig.add_trace(go.Bar(
                x=pivot_companies.index,
                y=pivot_companies[genre],
                name=genre
            ))
    st.markdown("#### Top 3 Production Companies based on Genres")
    fig.update_layout(
        barmode='stack',
        xaxis_title='Production Company',
        yaxis_title='Show Count',
        legend_title='Genre',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    st.plotly_chart(fig,use_container_width=True, height = 200)

with cols2:
    st.markdown("#### Top 5 Popular Genres of New Shows")
    fig = px.bar(new_show_popularity, x = "Genre Name", y="Average Popularity", text=['{:,.2f}'.format(x) for x in new_show_popularity["Average Popularity"]],
                 template = "seaborn", hover_name="Genre Name", hover_data={
                     'Genre Name': False,
                     'Count': False,
                     'Average Popularity': ':.2f'
                 }, color="Average Popularity", color_continuous_scale="teal")
    st.plotly_chart(fig,use_container_width=True, height = 200)
    st.caption("_New shows: The ones that started airing for the first time in 2023_")


