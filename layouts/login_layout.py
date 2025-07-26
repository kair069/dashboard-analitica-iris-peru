"""
Layout de la página de login empresarial
"""
from dash import html, dcc
import dash_bootstrap_components as dbc

def get_login_layout():
    """Retorna el layout de login empresarial"""
    
    return html.Div([
        # Fondo con gradiente
        html.Div([
            # Contenedor central
            html.Div([
                # Logo y título de la empresa
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line", style={
                            "font-size": "48px", 
                            "color": "#3b82f6",
                            "margin-bottom": "20px"
                        }),
                        html.H2("Iris Analytics", style={
                            "color": "#1e293b",
                            "font-weight": "700",
                            "margin-bottom": "8px"
                        }),
                        html.P("Sistema de Análisis de Datos Empresarial", style={
                            "color": "#64748b",
                            "margin-bottom": "40px"
                        })
                    ], className="text-center")
                ]),
                
                # Formulario de login
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Iniciar Sesión", className="text-center mb-4", style={
                            "color": "#1e293b",
                            "font-weight": "600"
                        }),
                        
                        # Alertas para mensajes
                        html.Div(id="login-alert", className="mb-3"),
                        
                        # Campo email
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Correo Electrónico", html_for="login-email"),
                                dbc.Input(
                                    id="login-email",
                                    type="email",
                                    placeholder="usuario@empresa.com",
                                    className="mb-3"
                                )
                            ])
                        ]),
                        
                        # Campo contraseña
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Contraseña", html_for="login-password"),
                                dbc.Input(
                                    id="login-password",
                                    type="password",
                                    placeholder="••••••••",
                                    className="mb-3"
                                )
                            ])
                        ]),
                        
                        # Checkbox recordar
                        dbc.Row([
                            dbc.Col([
                                dbc.Checkbox(
                                    id="remember-me",
                                    label="Recordar sesión",
                                    value=False,
                                    className="mb-3"
                                )
                            ])
                        ]),
                        
                        # Botón login
                        dbc.Row([
                            dbc.Col([
                                dbc.Button(
                                    "Iniciar Sesión",
                                    id="login-button",
                                    color="primary",
                                    className="w-100 mb-3",
                                    size="lg"
                                )
                            ])
                        ]),
                        
                        # Información de usuarios demo
                        html.Hr(),
                        html.Div([
                            html.H6("👥 Usuarios de Demostración:", style={
                                "color": "#64748b",
                                "font-size": "14px",
                                "margin-bottom": "10px"
                            }),
                            html.Ul([
                                html.Li([
                                    html.Strong("admin@empresa.com"), " / admin123 ",
                                    html.Span("(Administrador)", style={"color": "#3b82f6"})
                                ]),
                                html.Li([
                                    html.Strong("analista@empresa.com"), " / analista123 ",
                                    html.Span("(Analista)", style={"color": "#10b981"})
                                ]),
                                html.Li([
                                    html.Strong("gerente@empresa.com"), " / gerente123 ",
                                    html.Span("(Gerente)", style={"color": "#f59e0b"})
                                ])
                            ], style={
                                "font-size": "12px",
                                "color": "#64748b",
                                "list-style": "none",
                                "padding": "0"
                            })
                        ], style={
                            "background": "#f8fafc",
                            "padding": "15px",
                            "border-radius": "8px",
                            "border": "1px solid #e2e8f0"
                        })
                    ])
                ], style={
                    "max-width": "400px",
                    "width": "100%",
                    "box-shadow": "0 10px 25px rgba(0,0,0,0.1)",
                    "border": "none"
                })
                
            ], style={
                "display": "flex",
                "flex-direction": "column",
                "align-items": "center",
                "justify-content": "center",
                "min-height": "100vh",
                "padding": "20px"
            })
            
        ], style={
            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "min-height": "100vh",
            "position": "relative"
        }),
        
        # Elementos decorativos de fondo
        html.Div([
            html.Div(style={
                "position": "absolute",
                "top": "10%",
                "left": "10%",
                "width": "100px",
                "height": "100px",
                "background": "rgba(255,255,255,0.1)",
                "border-radius": "50%",
                "animation": "float 6s ease-in-out infinite"
            }),
            html.Div(style={
                "position": "absolute",
                "top": "70%",
                "right": "10%",
                "width": "150px",
                "height": "150px",
                "background": "rgba(255,255,255,0.05)",
                "border-radius": "50%",
                "animation": "float 8s ease-in-out infinite reverse"
            }),
            html.Div(style={
                "position": "absolute",
                "bottom": "20%",
                "left": "20%",
                "width": "80px",
                "height": "80px",
                "background": "rgba(255,255,255,0.08)",
                "border-radius": "50%",
                "animation": "float 10s ease-in-out infinite"
            })
        ], style={"position": "absolute", "top": "0", "left": "0", "width": "100%", "height": "100%", "pointer-events": "none"}),
        
        # Store para la sesión
        dcc.Store(id="session-store", data={}),
        dcc.Location(id="url-location", refresh=False)
        
    ])