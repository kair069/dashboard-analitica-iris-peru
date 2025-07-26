"""
Sistema de autenticación empresarial para el dashboard
"""
import hashlib
import secrets
from datetime import datetime, timedelta
import json
import os

class AuthSystem:
    """Sistema de autenticación simple para empresa"""
    
    def __init__(self):
        self.users_file = "auth/users.json"
        self.sessions_file = "auth/sessions.json"
        self.ensure_files_exist()
        
        # Usuarios por defecto (en producción usar base de datos)
        self.default_users = {
            "admin@empresa.com": {
                "password": self.hash_password("admin123"),
                "name": "Administrador",
                "role": "admin",
                "department": "IT",
                "created": datetime.now().isoformat()
            },
            "analista@empresa.com": {
                "password": self.hash_password("analista123"),
                "name": "Analista de Datos",
                "role": "analyst",
                "department": "Analytics",
                "created": datetime.now().isoformat()
            },
            "gerente@empresa.com": {
                "password": self.hash_password("gerente123"),
                "name": "Gerente General",
                "role": "manager",
                "department": "Management",
                "created": datetime.now().isoformat()
            }
        }
    
    def ensure_files_exist(self):
        """Crea directorio y archivos de autenticación si no existen"""
        os.makedirs("auth", exist_ok=True)
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def hash_password(self, password):
        """Hash seguro de contraseña"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self):
        """Carga usuarios del archivo"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            # Si no hay usuarios, crear los por defecto
            if not users:
                users = self.default_users
                self.save_users(users)
            
            return users
        except:
            return self.default_users
    
    def save_users(self, users):
        """Guarda usuarios al archivo"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(users, f, indent=2)
        except:
            pass
    
    def load_sessions(self):
        """Carga sesiones activas"""
        try:
            with open(self.sessions_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def save_sessions(self, sessions):
        """Guarda sesiones activas"""
        try:
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
        except:
            pass
    
    def authenticate(self, email, password):
        """Autentica usuario"""
        users = self.load_users()
        
        if email in users:
            hashed_password = self.hash_password(password)
            if users[email]["password"] == hashed_password:
                # Crear sesión
                session_token = secrets.token_urlsafe(32)
                sessions = self.load_sessions()
                
                sessions[session_token] = {
                    "email": email,
                    "name": users[email]["name"],
                    "role": users[email]["role"],
                    "department": users[email]["department"],
                    "login_time": datetime.now().isoformat(),
                    "expires": (datetime.now() + timedelta(hours=8)).isoformat()
                }
                
                self.save_sessions(sessions)
                return session_token, users[email]
        
        return None, None
    
    def validate_session(self, session_token):
        """Valida si la sesión es válida"""
        if not session_token:
            return False, None
        
        sessions = self.load_sessions()
        
        if session_token in sessions:
            session = sessions[session_token]
            expires = datetime.fromisoformat(session["expires"])
            
            if datetime.now() < expires:
                return True, session
            else:
                # Sesión expirada, eliminarla
                del sessions[session_token]
                self.save_sessions(sessions)
        
        return False, None
    
    def logout(self, session_token):
        """Cierra sesión"""
        sessions = self.load_sessions()
        if session_token in sessions:
            del sessions[session_token]
            self.save_sessions(sessions)
    
    def get_all_users(self):
        """Obtiene lista de todos los usuarios (solo admin)"""
        users = self.load_users()
        return {email: {k: v for k, v in user.items() if k != 'password'} 
                for email, user in users.items()}

# Instancia global
auth = AuthSystem()