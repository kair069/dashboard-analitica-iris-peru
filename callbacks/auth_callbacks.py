"""
Callbacks para el sistema de autenticación
"""
from dash import callback, Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
from dash import html, dcc
from auth.auth_system import auth

def register_auth_callbacks(app):
    """Registra callbacks de autenticación"""
    
    @app.callback(
        [Output("login-alert", "children"),
         Output("session-store", "data"),
         Output("url-location", "pathname")],
        Input("login-button", "n_clicks"),
        [State("login-email", "value"),
         State("login-password", "value"),
         State("remember-me", "value")],
        prevent_initial_call=True
    )
    def handle_login(n_clicks, email, password, remember):
        """Maneja el proceso de login"""
        if n_clicks and email and password:
            session_token, user_data = auth.authenticate(email, password)
            
            if session_token:
                # Login exitoso
                session_data = {
                    "token": session_token,
                    "user": user_data,
                    "authenticated": True
                }
                
                success_alert = dbc.Alert([
                    html.I(className="fas fa-check-circle me-2"),
                    f"¡Bienvenido, {user_data['name']}!"
                ], color="success", dismissable=True)
                
                return success_alert, session_data, "/dashboard"
            else:
                # Login fallido
                error_alert = dbc.Alert([
                    html.I(className="fas fa-exclamation-triangle me-2"),
                    "Credenciales incorrectas. Verifique su email y contraseña."
                ], color="danger", dismissable=True)
                
                return error_alert, {}, no_update
        
        return no_update, no_update, no_update
    
    @app.callback(
        Output("user-info-dropdown", "children"),
        Input("session-store", "data")
    )
    def update_user_info(session_data):
        """Actualiza información del usuario en el header"""
        if session_data.get("authenticated"):
            user = session_data["user"]
            
            return dbc.DropdownMenu([
                dbc.DropdownMenuItem([
                    html.I(className="fas fa-user me-2"),
                    f"{user['name']}"
                ], header=True),
                dbc.DropdownMenuItem([
                    html.I(className="fas fa-building me-2"),
                    f"{user['department']}"
                ], disabled=True),
                dbc.DropdownMenuItem([
                    html.I(className="fas fa-id-badge me-2"),
                    f"Rol: {user['role'].title()}"
                ], disabled=True),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem([
                    html.I(className="fas fa-cog me-2"),
                    "Configuración"
                ], id="user-settings"),
                dbc.DropdownMenuItem([
                    html.I(className="fas fa-sign-out-alt me-2"),
                    "Cerrar Sesión"
                ], id="logout-button", className="text-danger")
            ], 
            label=[
                html.I(className="fas fa-user-circle me-2"),
                user['name'].split()[0]  # Solo primer nombre
            ],
            color="outline-primary",
            size="sm")
        
        return html.Div()
    
    @app.callback(
        [Output("session-store", "data", allow_duplicate=True),
         Output("url-location", "pathname", allow_duplicate=True)],
        Input("logout-button", "n_clicks"),
        State("session-store", "data"),
        prevent_initial_call=True
    )
    def handle_logout(n_clicks, session_data):
        """Maneja el cierre de sesión"""
        if n_clicks and session_data.get("authenticated"):
            # Eliminar sesión del servidor
            auth.logout(session_data.get("token"))
            
            # Limpiar datos de sesión
            return {}, "/login"
        
        return no_update, no_update
    
    @app.callback(
        Output("session-validation", "children"),
        [Input("url-location", "pathname"),
         Input("session-store", "data")]
    )
    def validate_session_on_navigation(pathname, session_data):
        """Valida sesión en cada navegación"""
        if pathname == "/login":
            return html.Div()
        
        # Si no está en login, verificar autenticación
        if not session_data.get("authenticated"):
            return dcc.Location(pathname="/login", id="redirect-to-login")
        
        # Validar token en el servidor
        token = session_data.get("token")
        is_valid, server_session = auth.validate_session(token)
        
        if not is_valid:
            return dcc.Location(pathname="/login", id="redirect-to-login")
        
        return html.Div()
    
    @app.callback(
        Output("role-based-content", "style"),
        Input("session-store", "data")
    )
    def show_role_based_content(session_data):
        """Muestra contenido basado en el rol del usuario"""
        if session_data.get("authenticated"):
            user_role = session_data["user"]["role"]
            
            # Ejemplo: solo admin puede ver ciertos elementos
            if user_role == "admin":
                return {"display": "block"}
            else:
                return {"display": "none"}
        
        return {"display": "none"}