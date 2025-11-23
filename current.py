import httpx
import plotly.graph_objects as go
from shared import COLORS, BASE_URL, CITIES, categorize_aqi, fig_to_html


async def fetch_air_quality(lat: float, lon: float) -> dict:
    """Fetch current air quality data for a location from Open-Meteo."""
    params = {
        'latitude': lat,
        'longitude': lon,
        'current': 'pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone,ammonia,european_aqi',
        'timezone': 'auto'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params, timeout=10.0)
        response.raise_for_status()
        return response.json()


async def fetch_all_cities():
    """Fetch air quality data for all monitored cities."""
    cities_data = []

    for city_name, lat, lon in CITIES:
        data = await fetch_air_quality(lat, lon)
        current = data['current']
        aqi_value = current['european_aqi']
        aqi_label, _ = categorize_aqi(aqi_value)

        cities_data.append({
            'name': city_name,
            'lat': lat,
            'lon': lon,
            'aqi': aqi_value,
            'aqi_label': aqi_label,
            'components': {
                'pm2_5': current['pm2_5'],
                'pm10': current['pm10'],
                'co': current['carbon_monoxide'],
                'no2': current['nitrogen_dioxide'],
                'so2': current['sulphur_dioxide'],
                'o3': current['ozone'],
                'nh3': current['ammonia'],
            }
        })

    return cities_data


def create_pollutant_comparison(cities_data):
    """Create bar chart comparing pollutant levels across cities."""
    city_names = [city['name'] for city in cities_data]

    pollutants = ['pm2_5', 'pm10', 'co', 'no2', 'so2', 'o3']
    pollutant_labels = {
        'pm2_5': 'PM2.5',
        'pm10': 'PM10',
        'co': 'CO',
        'no2': 'NO₂',
        'so2': 'SO₂',
        'o3': 'O₃'
    }

    fig = go.Figure()

    colors_list = [COLORS['blue'], COLORS['green'], COLORS['amber'],
                   COLORS['red'], COLORS['purple'], COLORS['cyan']]

    for i, pollutant in enumerate(pollutants):
        values = [city['components'][pollutant] for city in cities_data]
        fig.add_trace(go.Bar(
            name=pollutant_labels[pollutant],
            x=city_names,
            y=values,
            marker=dict(color=colors_list[i])
        ))

    fig.update_layout(
        title='Pollutant Levels by City (μg/m³)',
        barmode='group',
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=20, t=60, b=60),
        xaxis_title='City',
        yaxis_title='Concentration (μg/m³)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig_to_html(fig, 'pollutant-comparison')


def create_aqi_distribution(cities_data):
    """Create pie chart showing AQI category distribution."""
    aqi_counts = {}
    aqi_colors_map = {}
    for city in cities_data:
        label = city['aqi_label']
        aqi_counts[label] = aqi_counts.get(label, 0) + 1
        if label not in aqi_colors_map:
            _, color = categorize_aqi(city['aqi'])
            aqi_colors_map[label] = color

    labels = list(aqi_counts.keys())
    values = list(aqi_counts.values())
    colors = [aqi_colors_map[label] for label in labels]

    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            marker=dict(colors=colors),
            hole=0.3
        )
    ])

    fig.update_layout(
        title='Air Quality Distribution',
        height=400,
        template='plotly_white',
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig_to_html(fig, 'aqi-distribution')


def create_pm_comparison(cities_data):
    """Create scatter plot comparing PM2.5 vs PM10."""
    city_names = [city['name'] for city in cities_data]
    pm25 = [city['components']['pm2_5'] for city in cities_data]
    pm10 = [city['components']['pm10'] for city in cities_data]
    aqi_colors = [categorize_aqi(city['aqi'])[1] for city in cities_data]

    fig = go.Figure(data=[
        go.Scatter(
            x=pm25,
            y=pm10,
            mode='markers+text',
            text=city_names,
            textposition='top center',
            marker=dict(
                size=20,
                color=aqi_colors,
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{text}</b><br>PM2.5: %{x:.1f}<br>PM10: %{y:.1f}<extra></extra>'
        )
    ])

    fig.update_layout(
        title='PM2.5 vs PM10 Comparison',
        xaxis_title='PM2.5 (μg/m³)',
        yaxis_title='PM10 (μg/m³)',
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=20, t=60, b=40)
    )

    return fig_to_html(fig, 'pm-comparison')


def create_component_breakdown(cities_data):
    """Create stacked bar chart showing component breakdown for each city."""
    city_names = [city['name'] for city in cities_data]

    components = {
        'CO': [city['components']['co'] / 100 for city in cities_data],
        'NO₂': [city['components']['no2'] for city in cities_data],
        'O₃': [city['components']['o3'] for city in cities_data],
        'SO₂': [city['components']['so2'] for city in cities_data],
        'NH₃': [city['components']['nh3'] for city in cities_data],
    }

    fig = go.Figure()

    colors_list = [COLORS['red'], COLORS['purple'], COLORS['cyan'],
                   COLORS['pink'], COLORS['indigo']]

    for i, (component, values) in enumerate(components.items()):
        fig.add_trace(go.Bar(
            name=component,
            x=city_names,
            y=values,
            marker=dict(color=colors_list[i])
        ))

    fig.update_layout(
        title='Gas Component Breakdown by City (CO scaled ÷100)',
        barmode='stack',
        height=400,
        template='plotly_white',
        margin=dict(l=40, r=20, t=60, b=60),
        xaxis_title='City',
        yaxis_title='Concentration (μg/m³)',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig_to_html(fig, 'component-breakdown')


async def get_dashboard_data():
    """Fetch all data for the current Air Quality dashboard."""
    cities_data = await fetch_all_cities()

    aqi_values = [city['aqi'] for city in cities_data]
    avg_pm25 = sum(city['components']['pm2_5'] for city in cities_data) / len(cities_data)

    stats = {
        'total_cities': len(cities_data),
        'avg_aqi': round(sum(aqi_values) / len(aqi_values), 1),
        'avg_pm25': round(avg_pm25, 1),
        'poor_or_worse': sum(1 for aqi in aqi_values if aqi >= 60)
    }

    charts = {
        'pollutant_comparison': create_pollutant_comparison(cities_data),
        'aqi_distribution': create_aqi_distribution(cities_data),
        'pm_comparison': create_pm_comparison(cities_data),
        'component_breakdown': create_component_breakdown(cities_data),
    }

    return {
        'stats': stats,
        'charts': charts,
        'cities': cities_data
    }
