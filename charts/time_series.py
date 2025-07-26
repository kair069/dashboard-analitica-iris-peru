"""
Gráfica de series de tiempo
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .base_chart import BaseChart

class TimeSeriesChart(BaseChart):
    """Gráfica de series de tiempo para sesiones y usuarios"""
    
    def create_figure(self, date_range_days=30, **kwargs):
        """
        Crea la gráfica de series de tiempo
        Args:
            date_range_days: Número de días para simular
        """
        if self.data is None:
            return go.Figure()
        
        # Simular datos diarios basados en los datos filtrados
        dates = pd.date_range(start='2024-01-01', periods=date_range_days, freq='D')
        
        # Calcular promedios de los datos filtrados
        avg_sessions = self.data['sessions'].mean() if 'sessions' in self.data.columns else 50
        avg_users = self.data['users'].mean() if 'users' in self.data.columns else 35
        
        # Generar datos simulados con variación realista
        np.random.seed(42)
        daily_sessions = np.random.poisson(avg_sessions, date_range_days)
        daily_users = (daily_sessions * np.random.uniform(0.6, 0.8, date_range_days)).astype(int)
        
        # Crear la figura
        fig = go.Figure()
        
        # Línea de sesiones
        fig.add_trace(go.Scatter(
            x=dates,
            y=daily_sessions,
            mode='lines+markers',
            name='Sesiones',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=6, line=dict(width=1, color='white')),
            hovertemplate='<b>Sesiones</b><br>Fecha: %{x}<br>Valor: %{y:,}<extra></extra>'
        ))
        
        # Línea de usuarios
        fig.add_trace(go.Scatter(
            x=dates,
            y=daily_users,
            mode='lines+markers',
            name='Usuarios',
            line=dict(color=self.colors['success'], width=3),
            marker=dict(size=6, line=dict(width=1, color='white')),
            hovertemplate='<b>Usuarios</b><br>Fecha: %{x}<br>Valor: %{y:,}<extra></extra>'
        ))
        
        # Configuración específica para series de tiempo
        fig.update_layout(
            hovermode='x unified',
            xaxis_title='Fecha',
            yaxis_title='Cantidad'
        )
        
        return fig
    
    def create_single_metric_series(self, metric_column, color=None, **kwargs):
        """
        Crea una serie de tiempo para una sola métrica
        Args:
            metric_column: Columna a graficar
            color: Color personalizado para la línea
        """
        if self.data is None or metric_column not in self.data.columns:
            return go.Figure()
        
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        avg_value = self.data[metric_column].mean()
        
        np.random.seed(42)
        daily_values = np.random.poisson(avg_value, 30)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=dates,
            y=daily_values,
            mode='lines+markers',
            name=metric_column.title(),
            line=dict(color=color or self.colors['primary'], width=3),
            marker=dict(size=6),
            fill='tonexty' if kwargs.get('fill_area') else None,
            fillcolor=f"rgba({color or self.colors['primary']}, 0.1)" if kwargs.get('fill_area') else None
        ))
        
        return fig