"""
Componente del menú lateral (sidebar)
"""
import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_bootstrap_components as dbc

def create_sidebar():
    """
    Crea el sidebar con estilo similar a Google Analytics
    """
    sidebar_style = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "280px",
        "padding": "20px 0",
        "background": "linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%)",
        "color": "white",
        "overflow-y": "auto",
        "z-index": 1000,
        "box-shadow": "2px 0 10px rgba(0,0,0,0.1)"
    }
    
    # Logo y título
    header = html.Div([
        html.Div([
            html.I(className="fas fa-chart-line", style={
                "font-size": "28px", 
                "color": "#60a5fa",
                "margin-right": "12px"
            }),
            html.H4("Iris Analytics", className="mb-0", style={
                "font-weight": "600",
                "color": "white"
            })
        ], className="d-flex align-items-center mb-4 px-3")
    ])
    
    # Sección de navegación principal
    nav_items = [
        {
            "icon": "fas fa-home",
            "label": "Overview",
            "id": "nav-overview",
            "active": True
        },
        {
            "icon": "fas fa-chart-bar",
            "label": "Species Analysis",
            "id": "nav-species"
        },
        {
            "icon": "fas fa-scatter-chart",
            "label": "Correlations",
            "id": "nav-correlations"
        },
        {
            "icon": "fas fa-map-marked-alt",
            "label": "Geographic View",
            "id": "nav-geographic"
        },
        {
            "icon": "fas fa-clock",
            "label": "Time Series",
            "id": "nav-timeseries"
        }
    ]
    
    nav_section = html.Div([
        html.H6("Navigation", className="text-uppercase px-3 mb-3", style={
            "font-size": "11px",
            "color": "#94a3b8",
            "font-weight": "600",
            "letter-spacing": "1px"
        }),
        html.Ul([
            html.Li([
                dbc.Button([
                    html.I(className=item["icon"], style={"margin-right": "12px", "width": "16px"}),
                    item["label"]
                ],
                id=item["id"],
                color="link",
                className="text-start w-100 border-0 px-3 py-2",
                style={
                    "color": "white" if item.get("active") else "#cbd5e1",
                    "background": "rgba(255,255,255,0.1)" if item.get("active") else "transparent",
                    "border-radius": "8px",
                    "font-weight": "500" if item.get("active") else "400",
                    "transition": "all 0.2s ease"
                })
            ], className="mb-1 px-2")
            for item in nav_items
        ], className="list-unstyled")
    ], className="mb-4")
    
    # Sección de filtros
    filters_section = html.Div([
        html.H6("Filters", className="text-uppercase px-3 mb-3", style={
            "font-size": "11px",
            "color": "#94a3b8",
            "font-weight": "600",
            "letter-spacing": "1px"
        }),
        
        # Filtro de especies
        html.Div([
            html.Label("Species", className="form-label text-light mb-2 px-3", style={
                "font-size": "13px",
                "font-weight": "500"
            }),
            dcc.Dropdown(
                id="species-filter",
                options=[
                    {"label": "All Species", "value": "all"},
                    {"label": "Setosa", "value": "setosa"},
                    {"label": "Versicolor", "value": "versicolor"},
                    {"label": "Virginica", "value": "virginica"}
                ],
                value="all",
                className="mx-3",
                style={"font-size": "13px"}
            )
        ], className="mb-3"),
        
        # Filtro de región
        html.Div([
            html.Label("Region", className="form-label text-light mb-2 px-3", style={
                "font-size": "13px",
                "font-weight": "500"
            }),
            dcc.Dropdown(
                id="region-filter",
                options=[],  # Se llenará dinámicamente
                value="all",
                className="mx-3",
                style={"font-size": "13px"}
            )
        ], className="mb-3"),
        
        # Filtro de fecha
        html.Div([
            html.Label("Date Range", className="form-label text-light mb-2 px-3", style={
                "font-size": "13px",
                "font-weight": "500"
            }),
            dcc.DatePickerRange(
                id="date-range-filter",
                className="mx-3",
                style={"font-size": "13px"}
            )
        ], className="mb-3")
    ])
    
    # Pie del sidebar
    footer = html.Div([
        html.Hr(style={"border-color": "rgba(255,255,255,0.2)"}),
        html.Div([
            html.I(className="fas fa-user-circle", style={
                "font-size": "20px",
                "margin-right": "8px",
                "color": "#60a5fa"
            }),
            html.Span("Admin User", style={
                "font-size": "13px",
                "color": "#e2e8f0"
            })
        ], className="px-3")
    ], style={"margin-top": "auto"})
    
    return html.Div([
        header,
        nav_section,
        filters_section,
        footer
    ], style=sidebar_style, id="sidebar")