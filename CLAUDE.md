# Agent Instructions

## Core Behavior

- **Always**: Explain what you're going to do to let me review it prior to implementing.  If you have to read multiple files to understand what needs to change, explain it to me and give me time to process and understand before implementing.
- **Iteration**: Work in small steps.  Lean startup style where tiny steps slowly progress toward the goal, letting me be involved and manually test after each small steps.
- **Learning**: My number 1 goal is to learn, so interact with me in a way that encourages learning.  While that may mean going slower in the short term, that lets me maximize my impact and speed in the long term.
- **Config**: There are very few things on this earth that I hate more than config.  Use it only when neccessary or when there is a massive massive benefit to doing so.

## Web Dev

Stack:
- Air: Web Development library
- Jinja: UI Definition
- Styling: Tailwind
- JS: Alpine.js 

### Air

Air is a Python web framework built on Starlette (not the Go live reload tool). Key patterns:

**App Structure:**
- `air.Air()` - Main app instance (wraps Starlette)
- `@app.page` - Full HTML page routes (function name becomes URL path)
- `@app.get()`, `@app.post()`, `@app.delete()` - Standard HTTP method routes
- All routes receive `air.Request` as first parameter

**Template Rendering:**
```python
jinja = air.JinjaRenderer(directory="templates")
# In route:
return jinja(request, name="template.html", context={...})
```

**Components for HTMX:**
- `air.Span("text", class_="...")` - Return HTML fragments
- `air.RedirectResponse("/path")` - Redirects
- `render_partial("template.html", **context)` - Render template to string
- Favor jinja or python html fragments

**Middleware:**
```python
app.add_middleware(air.SessionMiddleware, secret_key=key)
app.mount("/static", air.StaticFiles(directory="static"))
app.mount("/api", fastapi_app)  # Mount sub-apps
```

**Request Object:**
- `request.cookies.get("name")` - Read cookies
- `await request.form()` - Get form data
- `request.state` - Attach data between middleware/routes

**This Project's Pattern:**
- Air handles HTML pages (Jinja templates)
- Separate FastAPI instance mounted at `/api` for JSON endpoints
- Live reload via `fastapi dev main.py`, not `.air.toml`
