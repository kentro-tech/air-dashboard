import plotly.graph_objects as go

# Chart colors
COLORS = {
    'blue': '#3b82f6',
    'green': '#10b981',
    'amber': '#f59e0b',
    'purple': '#8b5cf6',
    'pink': '#ec4899',
    'cyan': '#06b6d4',
    'red': '#ef4444',
    'indigo': '#6366f1',
}

# Open-Meteo API configuration (no API key required!)
BASE_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Major cities to monitor (name, lat, lon)
CITIES = [
    ("New York", 40.7128, -74.0060),
    ("Los Angeles", 34.0522, -118.2437),
    ("London", 51.5074, -0.1278),
    ("Tokyo", 35.6762, 139.6503),
    ("Delhi", 28.7041, 77.1025),
    ("Beijing", 39.9042, 116.4074),
]


def categorize_aqi(aqi_value):
    """Categorize European AQI into readable labels."""
    match aqi_value:
        case None:
            return "Unknown", COLORS['blue']
        case _ if aqi_value <= 20:
            return "Good", COLORS['green']
        case _ if aqi_value <= 40:
            return "Fair", COLORS['cyan']
        case _ if aqi_value <= 60:
            return "Moderate", COLORS['amber']
        case _ if aqi_value <= 80:
            return "Poor", COLORS['red']
        case _:
            return "Very Poor", COLORS['purple']


def hex_to_rgba(hex_color: str, alpha: float = 0.1) -> str:
    """Convert hex color to rgba string."""
    r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
    return f'rgba({r}, {g}, {b}, {alpha})'


def fig_to_html(fig: go.Figure, title: str) -> str:
    """Convert plotly figure to HTML string."""
    return fig.to_html(
        include_plotlyjs=False,
        div_id=title.replace(' ', '-').lower(),
        full_html=False
    )
