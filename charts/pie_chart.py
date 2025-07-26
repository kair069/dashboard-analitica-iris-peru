"""
Gráfica de pie/dona para distribuciones
"""
import plotly.graph_objects as go
from .base_chart import BaseChart

class PieChart(BaseChart):
    """Gráfica de pie y dona para distribuciones"""
    
    def create_figure(self, value_column='species', is_donut=True, **kwargs):
        """
        Crea gráfica de pie o dona
        Args:
            value_column: Columna para agrupar y contar
            is_donut: Si True, crea dona; si False, pie completo
        """
        if self.data is None or value_column not in self.data.columns:
            return go.Figure()
        
        # Contar valores
        value_counts = self.data[value_column].value_counts()
        
        # Determinar colores
        if value_column == 'species':
            colors = [self.species_colors.get(species, self.colors['primary']) 
                     for species in value_counts.index]
        else:
            colors = [self.colors['primary'], self.colors['success'], 
                     self.colors['warning'], self.colors['danger']][:len(value_counts)]
        
        # Crear figura
        fig = go.Figure(data=[go.Pie(
            labels=value_counts.index,
            values=value_counts.values,
            hole=0.6 if is_donut else 0,
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            textinfo='label+percent',
            textposition='outside' if not is_donut else 'auto',
            hovertemplate='<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>'
        )])
        
        # Configuración específica
        fig.update_layout(
            showlegend=not is_donut,  # Mostrar leyenda solo si no es dona
            annotations=[
                dict(text=f'Total<br>{value_counts.sum()}', 
                     x=0.5, y=0.5, font_size=16, showarrow=False)
            ] if is_donut else []
        )
        
        return fig
    
    def create_nested_pie(self, outer_column, inner_column, **kwargs):
        """
        Crea un pie chart anidado con dos niveles
        Args:
            outer_column: Columna para el anillo exterior
            inner_column: Columna para el anillo interior
        """
        if (self.data is None or 
            outer_column not in self.data.columns or 
            inner_column not in self.data.columns):
            return go.Figure()
        
        # Datos para anillo exterior
        outer_counts = self.data[outer_column].value_counts()
        # Datos para anillo interior
        inner_counts = self.data[inner_column].value_counts()
        
        fig = go.Figure()
        
        # Anillo exterior
        fig.add_trace(go.Pie(
            labels=outer_counts.index,
            values=outer_counts.values,
            domain={'x': [0.2, 0.8], 'y': [0.2, 0.8]},
            hole=0.7,
            name=outer_column.title()
        ))
        
        # Anillo interior
        fig.add_trace(go.Pie(
            labels=inner_counts.index,
            values=inner_counts.values,
            domain={'x': [0.3, 0.7], 'y': [0.3, 0.7]},
            hole=0.9,
            name=inner_column.title()
        ))
        
        return fig