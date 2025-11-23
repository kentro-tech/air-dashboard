import httpx
import plotly.graph_objects as go
from shared import COLORS, BASE_URL, CITIES, fig_to_html, hex_to_rgba


async def fetch_historical_air_quality(lat: float, lon: float) -> dict:
    """Fetch 7-day historical air quality data from Open-Meteo."""
    params = {
        'latitude': lat,
        'longitude': lon,
        'hourly': 'pm10,pm2_5,european_aqi',
        'past_days': 7,
        'timezone': 'auto'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()


async def fetch_all_cities_historical():
    """Fetch historical air quality data for all cities."""
    cities_historical = []

    for city_name, lat, lon in CITIES:
        data = await fetch_historical_air_quality(lat, lon)
        hourly = data['hourly']

        cities_historical.append({
            'name': city_name,
            'lat': lat,
            'lon': lon,
            'timestamps': hourly['time'],
            'pm2_5': hourly['pm2_5'],
            'pm10': hourly['pm10'],
            'aqi': hourly['european_aqi']
        })

    return cities_historical


def create_aqi_trends(cities_historical):
    """Create line chart showing AQI trends over time for all cities."""
    fig = go.Figure()

    colors_list = [COLORS['blue'], COLORS['green'], COLORS['amber'],
                   COLORS['red'], COLORS['purple'], COLORS['cyan']]

    for i, city in enumerate(cities_historical):
        fig.add_trace(go.Scatter(
            x=city['timestamps'],
            y=city['aqi'],
            mode='lines',
            name=city['name'],
            line=dict(color=colors_list[i], width=2)
        ))

    fig.update_layout(
        title='Air Quality Index Trends (7 Days)',
        xaxis_title='Date & Time',
        yaxis_title='European AQI',
        height=500,
        template='plotly_white',
        margin=dict(l=40, r=20, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )

    return fig_to_html(fig, 'aqi-trends')


def create_pm25_trends(cities_historical):
    """Create area chart showing PM2.5 trends over time."""
    fig = go.Figure()

    colors_list = [COLORS['blue'], COLORS['green'], COLORS['amber'],
                   COLORS['red'], COLORS['purple'], COLORS['cyan']]

    for i, city in enumerate(cities_historical):
        fig.add_trace(go.Scatter(
            x=city['timestamps'],
            y=city['pm2_5'],
            mode='lines',
            name=city['name'],
            line=dict(color=colors_list[i], width=2),
            fill='tonexty' if i > 0 else 'tozeroy',
            fillcolor=hex_to_rgba(colors_list[i], 0.3)
        ))

    fig.update_layout(
        title='PM2.5 Trends (7 Days)',
        xaxis_title='Date & Time',
        yaxis_title='PM2.5 (μg/m³)',
        height=500,
        template='plotly_white',
        margin=dict(l=40, r=20, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )

    return fig_to_html(fig, 'pm25-trends')


def create_pm10_trends(cities_historical):
    """Create line chart showing PM10 trends over time."""
    fig = go.Figure()

    colors_list = [COLORS['blue'], COLORS['green'], COLORS['amber'],
                   COLORS['red'], COLORS['purple'], COLORS['cyan']]

    for i, city in enumerate(cities_historical):
        fig.add_trace(go.Scatter(
            x=city['timestamps'],
            y=city['pm10'],
            mode='lines+markers',
            name=city['name'],
            line=dict(color=colors_list[i], width=2),
            marker=dict(size=4)
        ))

    fig.update_layout(
        title='PM10 Trends (7 Days)',
        xaxis_title='Date & Time',
        yaxis_title='PM10 (μg/m³)',
        height=500,
        template='plotly_white',
        margin=dict(l=40, r=20, t=60, b=60),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        hovermode='x unified'
    )

    return fig_to_html(fig, 'pm10-trends')


async def get_trends_data():
    """Fetch all data for the trends dashboard."""
    cities_historical = await fetch_all_cities_historical()

    charts = {
        'aqi_trends': create_aqi_trends(cities_historical),
        'pm25_trends': create_pm25_trends(cities_historical),
        'pm10_trends': create_pm10_trends(cities_historical),
    }

    return {
        'charts': charts,
        'cities': [city['name'] for city in cities_historical]
    }
