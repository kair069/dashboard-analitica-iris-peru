"""
Aplicación principal del Dashboard Iris - Versión Modular
"""
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from callbacks.auth_callbacks import register_auth_callbacks
from layouts.login_layout import get_login_layout
from layouts.main_layout import get_main_layout
from callbacks.chart_callbacks import register_callbacks
from callbacks.filter_callbacks import register_filter_callbacks

# Inicializar app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    suppress_callback_exceptions=True
)

app.title = "Iris Analytics Dashboard"

# Layout principal

## Esto lo comente
app.layout = get_main_layout()


# ================================================================
# LAYOUT PRINCIPAL CON ROUTING
# ================================================================

# def serve_layout():
#     """Layout principal con routing de páginas"""
#     return html.Div([
#         dcc.Location(id="main-url", refresh=False),
#         html.Div(id="page-content"),
#         html.Div(id="session-validation"),  # Para validación de sesión
#         dcc.Store(id="session-store", data={})  # Store global de sesión
#     ])

# app.layout = serve_layout

# # ================================================================
# # CALLBACK DE ROUTING PRINCIPAL
# # ================================================================

# @app.callback(
#     Output("page-content", "children"),
#     [Input("main-url", "pathname"),
#      Input("session-store", "data")]
# )
# def display_page(pathname, session_data):
#     """Maneja el routing entre páginas"""
    
#     # Si no hay pathname, ir a login
#     if not pathname or pathname == "/":
#         return get_login_layout()
    
#     # Página de login
#     elif pathname == "/login":
#         return get_login_layout()
    
#     # Página principal del dashboard
#     elif pathname == "/dashboard":
#         # Verificar autenticación
#         if session_data.get("authenticated"):
#             return get_authenticated_layout(session_data)
#         else:
#             return get_login_layout()
    
#     # Página no encontrada
#     else:
#         return html.Div([
#             html.H1("404 - Página no encontrada"),
#             html.P("La página que buscas no existe."),
#             dcc.Link("Volver al inicio", href="/dashboard")
#         ], className="text-center mt-5")

# def get_authenticated_layout(session_data):
#     """Retorna el layout del dashboard con información del usuario"""
#     user = session_data["user"]
    
#     # Header con información del usuario
#     user_header = html.Div([
#         html.Div([
#             html.H1("Dashboard Overview", style={
#                 "color": "#1e293b", 
#                 "margin": "0", 
#                 "font-weight": "700"
#             }),
#             html.P("Análisis en tiempo real del dataset Iris", style={
#                 "color": "#64748b", 
#                 "margin": "0"
#             })
#         ], style={"flex": "1"}),
        
#         # Información del usuario
#         html.Div([
#             html.Div([
#                 html.Span(f"Bienvenido, {user['name']}", style={
#                     "color": "#1e293b",
#                     "font-weight": "500",
#                     "margin-right": "20px"
#                 }),
#                 html.Div(id="user-info-dropdown")
#             ], className="d-flex align-items-center")
#         ])
#     ], style={
#         "background": "white",
#         "padding": "20px",
#         "box-shadow": "0 1px 3px rgba(0,0,0,0.1)",
#         "border-bottom": "1px solid #e2e8f0",
#         "display": "flex",
#         "justify-content": "space-between",
#         "align-items": "center"
#     })
    
#     # Obtener el layout principal y modificar el header
#     main_layout = get_main_layout()
    
#     # Reemplazar el header original con el nuevo
#     if hasattr(main_layout, 'children') and len(main_layout.children) > 1:
#         sidebar = main_layout.children[0]  # Sidebar
#         content = main_layout.children[1]  # Content
        
#         # Modificar el content para usar el nuevo header
#         if hasattr(content, 'children') and len(content.children) > 0:
#             content.children[0] = user_header  # Reemplazar header
    
#     return main_layout

# ================================================================
# REGISTRAR TODOS LOS CALLBACKS
# ================================================================

# Registrar callbacks
# Callbacks de autenticación (PRIMERO)
register_auth_callbacks(app)

register_callbacks(app)

register_filter_callbacks(app)

# ================================================================
# CSS PERSONALIZADO PARA LOGIN
# ================================================================

# app.index_string = '''
# <!DOCTYPE html>
# <html>
#     <head>
#         {%metas%}
#         <title>{%title%}</title>
#         {%favicon%}
#         {%css%}
#         <style>
#             @keyframes float {
#                 0% { transform: translateY(0px); }
#                 50% { transform: translateY(-20px); }
#                 100% { transform: translateY(0px); }
#             }
            
#             .login-container {
#                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#                 min-height: 100vh;
#             }
            
#             /* Estilos para mejorar el login */
#             .form-control:focus {
#                 border-color: #3b82f6;
#                 box-shadow: 0 0 0 0.2rem rgba(59, 130, 246, 0.25);
#             }
            
#             .btn-primary {
#                 background: linear-gradient(45deg, #3b82f6, #1d4ed8);
#                 border: none;
#                 transition: all 0.3s ease;
#             }
            
#             .btn-primary:hover {
#                 background: linear-gradient(45deg, #1d4ed8, #1e40af);
#                 transform: translateY(-1px);
#                 box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
#             }
#         </style>
#     </head>
#     <body>
#         {%app_entry%}
#         <footer>
#             {%config%}
#             {%scripts%}
#             {%renderer%}
#         </footer>
#     </body>
# </html>
# '''


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)