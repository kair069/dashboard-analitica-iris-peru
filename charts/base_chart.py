"""
Clase base para todas las gráficas del dashboard
"""
import plotly.graph_objects as go
from abc import ABC, abstractmethod

class BaseChart(ABC):
    """Clase base abstracta para todas las gráficas"""
    
    def __init__(self, data=None):
        self.data = data
        self.colors = {
            'primary': '#3b82f6',
            'success': '#10b981', 
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#06b6d4'
        }
        self.species_colors = {
            'setosa': '#3b82f6',
            'versicolor': '#10b981',
            'virginica': '#f59e0b'
        }
    
    def get_theme(self):
        """Retorna el tema común para todas las gráficas"""
        return {
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'font': dict(family='Inter, sans-serif', size=11, color='#374151'),
            'margin': dict(l=0, r=0, t=0, b=0),
            'xaxis': dict(showgrid=True, gridcolor='#f3f4f6'),
            'yaxis': dict(showgrid=True, gridcolor='#f3f4f6'),
            'legend': dict(
                orientation='h', 
                yanchor='bottom', 
                y=-0.15, 
                xanchor='center', 
                x=0.5
            )
        }
    
    def apply_theme(self, fig):
        """Aplica el tema común a la figura"""
        fig.update_layout(**self.get_theme())
        return fig
    
    def set_data(self, data):
        """Establece los datos para la gráfica"""
        self.data = data
        return self
    
    @abstractmethod
    def create_figure(self, **kwargs):
        """Método abstracto que debe implementar cada gráfica"""
        pass
    
    def get_figure(self, **kwargs):
        """Retorna la figura con tema aplicado"""
        fig = self.create_figure(**kwargs)
        return self.apply_theme(fig)