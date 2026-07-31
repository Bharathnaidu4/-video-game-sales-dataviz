import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------- Page config & theme ----------
st.set_page_config(page_title="Global Video Game Sales Dashboard", layout="wide")

BLUE = '#0072B2'
ORANGE = '#E69F00'
GREEN = '#009E73'
VERMILLION = '#D55E00'
GREY = '#999999'
CVD_SEQUENCE = [BLUE, ORANGE, GREEN, VERMILLION, '#56B4E9', '#F0E442', GREY]


def style(fig, height=430):
    fig.update_layout(
        template='simple_white',
        font=dict(family='Arial', size=13, color='#333333'),
        title=dict(font=dict(size=16, color='#1a1a1a'), x=0, xanchor='left'),
        margin=dict(l=60, r=30, t=70, b=50),
        height=height,
        plot_bgcolor='white',
        paper_bgcolor='white',
    )
    fig.update_xaxes(showgrid=False, showline=True, linecolor='#CCCCCC', zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor='#F0F0F0', showline=False, zeroline=False)
    return fig


@st.cache_data
def load_data():
    df = pd.read_csv('vgsales.csv')
    df = df.dropna(subset=['Year', 'Publisher']).copy()
    df['Year'] = df['Year'].astype(int)
    df = df[(df['Year'] >= 1980) & (df['Year'] <= 2016)]
    return df


df = load_data()

# ---------- Header ----------
st.title("🎮 Global Video Game Sales — Interactive Dashboard")
st.caption("1980–2016 · 16,000+ titles · Source: Kaggle (VGChartz)")

# ---------- Sidebar filters (meaningful interactivity) ----------
st.sidebar.header("Filters")

year_range = st.sidebar.slider(
    "Year range",
    int(df['Year'].min()), int(df['Year'].max()),
    (int(df['Year'].min()), int(df['Year'].max()))
)

all_genres = sorted(df['Genre'].unique())
selected_genres = st.sidebar.multiselect("Genre", all_genres, default=all_genres)

all_regions = {'North America': 'NA_Sales', 'Europe': 'EU_Sales', 'Japan': 'JP_Sales', 'Other': 'Other_Sales'}
selected_region_label = st.sidebar.selectbox("Region focus", list(all_regions.keys()), index=0)
region_col = all_regions[selected_region_label]

top_n_platforms = st.sidebar.slider("Number of platforms to show", 5, 15, 10)

# Apply filters
mask = (df['Year'].between(year_range[0], year_range[1])) & (df['Genre'].isin(selected_genres))
fdf = df[mask]

if fdf.empty:
    st.warning("No data matches the current filters. Try widening your selection.")
    st.stop()

# ---------- Top-line metrics ----------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Games in view", f"{len(fdf):,}")
col2.metric("Total global sales", f"{fdf['Global_Sales'].sum():,.0f}M units")
col3.metric(f"{selected_region_label} sales", f"{fdf[region_col].sum():,.0f}M units")
col4.metric("Top platform", fdf.groupby('Platform')['Global_Sales'].sum().idxmax())

st.divider()

# ---------- Tabs (multi-tab dashboard, per bonus) ----------
tab1, tab2, tab3 = st.tabs(["📊 Platforms & Publishers", "🌍 Regional Trends", "📈 Sales Over Time"])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        platform_sales = fdf.groupby('Platform')['Global_Sales'].sum().sort_values(ascending=False).head(top_n_platforms).reset_index()
        colors = [ORANGE if i == 0 else GREY for i in range(len(platform_sales))]
        fig1 = go.Figure(go.Bar(x=platform_sales['Platform'], y=platform_sales['Global_Sales'], marker_color=colors))
        fig1.update_layout(title=f'Top {top_n_platforms} Platforms by Global Sales', yaxis_title='Global Sales (Millions)', xaxis_title='')
        st.plotly_chart(style(fig1), use_container_width=True)

    with c2:
        top_pub = fdf.groupby('Publisher')['Global_Sales'].sum().sort_values(ascending=False).head(8).sort_values().reset_index()
        colors2 = [ORANGE if v == top_pub['Global_Sales'].max() else GREY for v in top_pub['Global_Sales']]
        fig2 = go.Figure(go.Bar(x=top_pub['Global_Sales'], y=top_pub['Publisher'], orientation='h', marker_color=colors2))
        fig2.update_layout(title='Top Publishers by Global Sales', xaxis_title='Global Sales (Millions)', yaxis_title='')
        st.plotly_chart(style(fig2), use_container_width=True)

    top_genre_pub = fdf.groupby(['Genre', 'Publisher'])['Global_Sales'].sum().reset_index()
    top_genre_pub = top_genre_pub.sort_values('Global_Sales', ascending=False).groupby('Genre').head(1).sort_values('Global_Sales')
    fig3 = px.bar(top_genre_pub, x='Global_Sales', y='Genre', color='Publisher', orientation='h',
                  color_discrete_sequence=CVD_SEQUENCE)
    fig3.update_layout(title='Leading Publisher per Genre', xaxis_title='Global Sales (Millions)', yaxis_title='')
    st.plotly_chart(style(fig3, height=420), use_container_width=True)

with tab2:
    genre_region = fdf.groupby('Genre')[['NA_Sales', 'EU_Sales', 'JP_Sales']].sum().reset_index()
    genre_region = genre_region.sort_values('NA_Sales', ascending=False)
    genre_region_melt = genre_region.melt(id_vars='Genre', var_name='Region', value_name='Sales')
    genre_region_melt['Region'] = genre_region_melt['Region'].str.replace('_Sales', '')
    fig4 = px.bar(genre_region_melt, x='Genre', y='Sales', color='Region', barmode='group',
                  color_discrete_map={'NA': BLUE, 'EU': ORANGE, 'JP': GREEN})
    fig4.update_layout(title='Genre Preference by Region', yaxis_title='Sales (Millions)', xaxis_title='', legend_title='')
    fig4.update_xaxes(tickangle=45)
    st.plotly_chart(style(fig4, height=460), use_container_width=True)

    region_by_year = fdf.groupby('Year')[['NA_Sales', 'EU_Sales', 'JP_Sales', 'Other_Sales']].sum()
    region_share = (region_by_year.div(region_by_year.sum(axis=1), axis=0) * 100).reset_index()
    region_melt = region_share.melt(id_vars='Year', var_name='Region', value_name='Share')
    region_melt['Region'] = region_melt['Region'].str.replace('_Sales', '')
    fig5 = px.area(region_melt, x='Year', y='Share', color='Region',
                    color_discrete_map={'NA': BLUE, 'EU': ORANGE, 'JP': GREEN, 'Other': GREY})
    fig5.update_layout(title="Regional Share of Global Sales Over Time", yaxis_title='Share (%)', xaxis_title='', legend_title='')
    st.plotly_chart(style(fig5), use_container_width=True)

with tab3:
    yearly = fdf.groupby('Year')['Global_Sales'].sum().reset_index()
    fig6 = go.Figure(go.Scatter(x=yearly['Year'], y=yearly['Global_Sales'], mode='lines', line=dict(color=BLUE, width=3)))
    fig6.update_layout(title='Global Sales Trend for Current Filters', yaxis_title='Global Sales (Millions)', xaxis_title='')
    st.plotly_chart(style(fig6), use_container_width=True)

    st.caption("Adjust the year range, genre, and region filters in the sidebar to explore how trends change across different slices of the data.")

st.divider()
st.caption("Data Visualization Final Project · Global Video Game Sales (1980–2016) · Built with Streamlit + Plotly")
