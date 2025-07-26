"""
Gráfica de box plot (diagrama de caja) para análisis de distribuciones
"""
import plotly.express as px
import plotly.graph_objects as go
from .base_chart import BaseChart

class BoxPlotChart(BaseChart):
    """Gráfica de box plot con diferentes configuraciones"""
    
    def create_figure(self, y_column, x_column=None, color_column='species', **kwargs):
        """
        Crea box plot
        Args:
            y_column: Columna numérica para el eje Y
            x_column: Columna categórica para el eje X (opcional)
            color_column: Columna para colorear cajas
        """
        if self.data is None or y_column not in self.data.columns:
            return go.Figure()
        
        # Si no se especifica x_column, usar color_column como x
        if x_column is None:
            x_column = color_column if color_column in self.data.columns else None
        
        if x_column and x_column in self.data.columns:
            # Box plot por categorías
            fig = px.box(
                self.data,
                x=x_column,
                y=y_column,
                color=color_column if color_column in self.data.columns else None,
                color_discrete_map=self.species_colors if color_column == 'species' else None,
                title=""
            )
        else:
            # Box plot simple
            fig = px.box(
                self.data,
                y=y_column,
                color_discrete_sequence=[self.colors['primary']],
                title=""
            )
        
        # Personalizar layout
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title() if x_column else 'Categoría',
            yaxis_title=y_column.replace('_', ' ').title(),
            showlegend=False  # Ocultar leyenda para box plots
        )
        
        # Personalizar cajas
        fig.update_traces(
            marker=dict(size=4, opacity=0.6),  # Puntos outliers más pequeños
            line=dict(width=2)  # Líneas más gruesas
        )
        
        return fig
    
    def create_violin_plot(self, y_column, x_column=None, color_column='species', **kwargs):
        """
        Crea violin plot (combinación de box plot y densidad)
        Args:
            y_column: Columna numérica para el eje Y
            x_column: Columna categórica para el eje X
            color_column: Columna para colorear
        """
        if self.data is None or y_column not in self.data.columns:
            return go.Figure()
        
        if x_column is None:
            x_column = color_column if color_column in self.data.columns else None
        
        if x_column and x_column in self.data.columns:
            fig = px.violin(
                self.data,
                x=x_column,
                y=y_column,
                color=color_column if color_column in self.data.columns else None,
                color_discrete_map=self.species_colors if color_column == 'species' else None,
                title=""
            )
        else:
            fig = px.violin(
                self.data,
                y=y_column,
                color_discrete_sequence=[self.colors['primary']],
                title=""
            )
        
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title() if x_column else 'Categoría',
            yaxis_title=y_column.replace('_', ' ').title(),
            showlegend=False
        )
        
        return fig