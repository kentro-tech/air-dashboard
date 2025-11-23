import air
from dotenv import load_dotenv
import current as current_module
import trends as trends_module

load_dotenv()

app = air.Air()
jinja = air.JinjaRenderer(directory="templates")


@app.page
async def index(request: air.Request):
    """Homepage - Air Framework Demo."""
    return jinja(request, name="index.html.j2")


@app.page
async def current(request: air.Request):
    """Current Air Quality Dashboard."""
    data = await current_module.get_dashboard_data()
    return jinja(
        request,
        name="current.html.j2",
        stats=data['stats'],
        charts=data['charts'],
        cities=data['cities']
    )


@app.page
async def trends(request: air.Request):
    """Air Quality Trends Dashboard."""
    data = await trends_module.get_trends_data()
    return jinja(
        request,
        name="trends.html.j2",
        charts=data['charts'],
        cities=data['cities']
    )
