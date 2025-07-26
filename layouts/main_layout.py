"""
Layout principal con sidebar y contenido
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

def get_main_layout():
    """Retorna el layout principal"""
    
    # Sidebar
    sidebar = html.Div([
        html.Div([
            html.I(className="fas fa-chart-line", style={"font-size": "24px", "color": "#60a5fa", "margin-right": "10px"}),
            html.H4("Iris Analytics", style={"color": "white", "margin": "0"})
        ], className="d-flex align-items-center mb-4"),
        
        html.Hr(style={"border-color": "rgba(255,255,255,0.3)"}),
        
        html.H6("Filtros", style={"color": "#94a3b8", "font-size": "12px", "text-transform": "uppercase"}),
        
        html.Label("Especies:", style={"color": "white", "font-size": "13px"}),
        dcc.Dropdown(
            id="species-filter",
            options=[
                {"label": "Todas", "value": "all"},
                {"label": "Setosa", "value": "setosa"},
                {"label": "Versicolor", "value": "versicolor"},
                {"label": "Virginica", "value": "virginica"}
            ],
            value="all",
            className="mb-3",
            style={"font-size": "12px"}
        ),
        
        html.Label("Región:", style={"color": "white", "font-size": "13px"}),
        dcc.Dropdown(
            id="region-filter",
            options=[
                {"label": "Todas", "value": "all"},
                {"label": "North America", "value": "North America"},
                {"label": "Europe", "value": "Europe"},
                {"label": "Asia", "value": "Asia"},
                {"label": "South America", "value": "South America"}
            ],
            value="all",
            style={"font-size": "12px"}
        ),
        
        # ===============================================
        # ✅ AQUÍ EMPIEZAN LOS COMPONENTES NUEVOS
        # ===============================================
        
        # Contador de registros filtrados
        html.Div([
            html.Hr(style={"border-color": "rgba(255,255,255,0.3)", "margin": "20px 0 15px 0"}),
            dbc.Badge(
                id="filter-counter",
                children="150 registros",
                color="info",
                className="w-100 py-2",
                style={"font-size": "11px"}
            )
        ], className="mb-3"),

        # Botón para resetear filtros
        dbc.Button([
            html.I(className="fas fa-undo me-2"),
            "Resetear Filtros"
        ], 
        id="reset-filters-btn",
        color="outline-light",
        size="sm",
        className="w-100 mb-3",
        style={"font-size": "12px"}),

        # Filtros predefinidos
        html.Div([
            html.Label("Presets:", style={"color": "white", "font-size": "13px"}),
            dcc.Dropdown(
                id="filter-preset-dropdown",
                options=[
                    {"label": "🌸 Todas las especies", "value": "all"},
                    {"label": "🇺🇸 Setosa en NA", "value": "setosa-na"},
                    {"label": "🇪🇺 Versicolor en Europa", "value": "versicolor-eu"},
                    {"label": "🇯🇵 Virginica en Asia", "value": "virginica-asia"},
                    {"label": "🌺 Flores grandes", "value": "large-flowers"},
                    {"label": "🌼 Flores pequeñas", "value": "small-flowers"}
                ],
                placeholder="Seleccionar preset...",
                style={"font-size": "11px"}
            )
        ], className="mb-3"),

        # Toggle para filtros avanzados
        dbc.Button([
            html.I(className="fas fa-sliders-h me-2"),
            "Filtros Avanzados"
        ],
        id="advanced-filters-toggle",
        color="outline-light",
        size="sm",
        className="w-100 mb-2",
        style={"font-size": "11px"}),

        # Filtros avanzados colapsables
        dbc.Collapse([
            html.Div([
                # Rango de longitud de sépalo
                html.Label("Longitud Sépalo:", style={"color": "white", "font-size": "12px"}),
                dcc.RangeSlider(
                    id="sepal-length-range",
                    min=0, max=8, value=[4, 8],
                    marks={i: f'{i}' for i in range(0, 9, 2)},
                    className="mb-3"
                ),
                
                # Rango de ancho de sépalo
                html.Label("Ancho Sépalo:", style={"color": "white", "font-size": "12px"}),
                dcc.RangeSlider(
                    id="sepal-width-range",
                    min=0, max=5, value=[2, 5],
                    marks={i: f'{i}' for i in range(0, 6)},
                    className="mb-3"
                )
            ], style={"padding": "10px", "background": "rgba(255,255,255,0.1)", "border-radius": "8px"})
        ], id="advanced-filters-collapse", is_open=False),

        # Sugerencias inteligentes
        html.Div(id="filter-suggestions", className="mt-3"),

        # Advertencias de filtros
        html.Div(id="filter-warning", className="mt-2"),

        # Store para historial de filtros
        dcc.Store(id="filter-history-store", data=[])
        
        # ===============================================
        # ✅ AQUÍ TERMINAN LOS COMPONENTES NUEVOS
        # ===============================================
        
    ], style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "280px",
        "padding": "20px",
        "background": "linear-gradient(180deg, #1e3a8a 0%, #1e40af 100%)",
        "overflow-y": "auto",
        "z-index": 1000,
        "box-shadow": "2px 0 10px rgba(0,0,0,0.1)"
    })
    
    # Header principal
    header = html.Div([
        html.H1("Dashboard Overview", style={"color": "#1e293b", "margin": "0", "font-weight": "700"}),
        html.P("Análisis en tiempo real del dataset Iris", style={"color": "#64748b", "margin": "0"})
    ], style={
        "background": "white",
        "padding": "20px",
        "box-shadow": "0 1px 3px rgba(0,0,0,0.1)",
        "border-bottom": "1px solid #e2e8f0"
    })
    
    # Contenido principal (RESTO DEL CÓDIGO IGUAL)
    content = html.Div([
        header,
        html.Div([
            # Tarjetas de métricas
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.H3(id="total-sessions", children="0", style={"color": "#1e293b", "margin": "0", "font-weight": "700"}),
                                    html.P("Total Sesiones", style={"color": "#64748b", "margin": "0", "font-size": "13px"})
                                ]),
                                html.I(className="fas fa-users", style={"font-size": "24px", "color": "#3b82f6"})
                            ], className="d-flex justify-content-between align-items-start")
                        ])
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.H3(id="total-users", children="0", style={"color": "#1e293b", "margin": "0", "font-weight": "700"}),
                                    html.P("Total Usuarios", style={"color": "#64748b", "margin": "0", "font-size": "13px"})
                                ]),
                                html.I(className="fas fa-user-check", style={"font-size": "24px", "color": "#10b981"})
                            ], className="d-flex justify-content-between align-items-start")
                        ])
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.H3(id="avg-sepal", children="0", style={"color": "#1e293b", "margin": "0", "font-weight": "700"}),
                                    html.P("Prom. Sépalo", style={"color": "#64748b", "margin": "0", "font-size": "13px"})
                                ]),
                                html.I(className="fas fa-ruler", style={"font-size": "24px", "color": "#f59e0b"})
                            ], className="d-flex justify-content-between align-items-start")
                        ])
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.H3(id="species-count", children="0", style={"color": "#1e293b", "margin": "0", "font-weight": "700"}),
                                    html.P("Especies", style={"color": "#64748b", "margin": "0", "font-size": "13px"})
                                ]),
                                html.I(className="fas fa-seedling", style={"font-size": "24px", "color": "#ef4444"})
                            ], className="d-flex justify-content-between align-items-start")
                        ])
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=3)
            ], className="mb-4"),
            
            # PRIMERA FILA DE GRÁFICAS - AHORA CON 3 COLUMNAS
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5("Sesiones a lo largo del tiempo", style={"margin": "0", "font-weight": "600", "color": "#1e293b"})
                        ], style={"background": "white", "border-bottom": "1px solid #e2e8f0"}),
                        dbc.CardBody([
                            dcc.Graph(id="time-series-chart", style={"height": "350px"})
                        ], style={"padding": "0"})
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=6),  # Mantener time series en 6 columnas
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5("Distribución de Especies", style={"margin": "0", "font-weight": "600", "color": "#1e293b"})
                        ], style={"background": "white", "border-bottom": "1px solid #e2e8f0"}),
                        dbc.CardBody([
                            dcc.Graph(id="pie-chart", style={"height": "350px"})
                        ], style={"padding": "10px"})
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=3),  # CAMBIO: Reduje pie chart a 3 columnas
                
                # NUEVA GRÁFICA: Box Plot
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.Div([
                                html.H5("Análisis de Distribución", style={"margin": "0", "font-weight": "600", "color": "#1e293b"}),
                                dcc.Dropdown(
                                    id="boxplot-feature-selector",
                                    options=[
                                        {"label": "Long. Sépalo", "value": "sepal length (cm)"},
                                        {"label": "Ancho Sépalo", "value": "sepal width (cm)"},
                                        {"label": "Long. Pétalo", "value": "petal length (cm)"},
                                        {"label": "Ancho Pétalo", "value": "petal width (cm)"}
                                    ],
                                    value="sepal length (cm)",
                                    style={"font-size": "11px", "margin-top": "5px"}
                                )
                            ])
                        ], style={"background": "white", "border-bottom": "1px solid #e2e8f0"}),
                        dbc.CardBody([
                            dcc.Graph(id="box-plot-chart", style={"height": "280px"})
                        ], style={"padding": "5px"})
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=3)  # NUEVA: Box plot en 3 columnas
            ], className="mb-4"),
            
            # SEGUNDA FILA DE GRÁFICAS - NUEVA: Agregué la gráfica de histograma aquí
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader([
                            html.H5("Distribución de Características", style={"margin": "0", "font-weight": "600", "color": "#1e293b"})
                        ], style={"background": "white", "border-bottom": "1px solid #e2e8f0"}),
                        dbc.CardBody([
                            # Dropdown para seleccionar característica
                            html.Div([
                                html.Label("Característica:", style={"font-size": "13px", "margin-bottom": "5px"}),
                                dcc.Dropdown(
                                    id="feature-selector",
                                    options=[
                                        {"label": "Longitud Sépalo", "value": "sepal length (cm)"},
                                        {"label": "Ancho Sépalo", "value": "sepal width (cm)"},
                                        {"label": "Longitud Pétalo", "value": "petal length (cm)"},
                                        {"label": "Ancho Pétalo", "value": "petal width (cm)"}
                                    ],
                                    value="sepal length (cm)",
                                    style={"font-size": "12px"}
                                )
                            ], style={"margin-bottom": "15px"}),
                            dcc.Graph(id="histogram-chart", style={"height": "300px"})
                        ], style={"padding": "15px"})
                    ], style={"border": "none", "box-shadow": "0 1px 3px rgba(0,0,0,0.1)"})
                ], width=12)  # CORREGIDO: Lo puse en toda la fila (width=12)
            ], className="mb-4"),
            
            # TERCERA FILA DE GRÁFICAS
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Análisis Correlación", style={
                            "margin": "0", 
                            "font-weight": "600", 
                            "color": "#1e293b",
                            "font-size": "14px"  # Título más pequeño para que quepa
                        })
                    ], style={"background": "white", "border-bottom": "1px solid #e2e8f0", "padding": "10px 15px"}),
                    dbc.CardBody([
                        dcc.Graph(id="scatter-chart", style={"height": "280px"})
                    ], style={"padding": "5px"})
                ], style={
                    "border": "none", 
                    "box-shadow": "0 2px 8px rgba(0,0,0,0.08)",
                    "border-radius": "12px"
                })
            ], width=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Mapa Correlación", style={
                            "margin": "0", 
                            "font-weight": "600", 
                            "color": "#1e293b",
                            "font-size": "14px"
                        })
                    ], style={"background": "white", "border-bottom": "1px solid #e2e8f0", "padding": "10px 15px"}),
                    dbc.CardBody([
                        dcc.Graph(id="heatmap-chart", style={"height": "280px"})
                    ], style={"padding": "5px"})
                ], style={
                    "border": "none", 
                    "box-shadow": "0 2px 8px rgba(0,0,0,0.08)",
                    "border-radius": "12px"
                })
            ], width=4),

            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.H5("Sesiones x Región", style={
                            "margin": "0", 
                            "font-weight": "600", 
                            "color": "#1e293b",
                            "font-size": "14px"
                        })
                    ], style={"background": "white", "border-bottom": "1px solid #e2e8f0", "padding": "10px 15px"}),
                    dbc.CardBody([
                        dcc.Graph(id="bar-chart", style={"height": "280px"})
                    ], style={"padding": "5px"})
                ], style={
                    "border": "none", 
                    "box-shadow": "0 2px 8px rgba(0,0,0,0.08)",
                    "border-radius": "12px"
                })
            ], width=4)
        ], className="mb-5")
            
        ], style={"padding": "20px"})
        
    ], style={
        "margin-left": "280px",
        "background": "#f8fafc",
        "min-height": "100vh"
    })
    
    return html.Div([
        sidebar,
        content
    ], style={"font-family": "'Inter', sans-serif"})