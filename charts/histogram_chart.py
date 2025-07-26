"""
Gráfica de histograma para distribuciones
"""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from .base_chart import BaseChart

class HistogramChart(BaseChart):
    """Gráfica de histograma con diferentes configuraciones"""
    
    def create_figure(self, column, bins=20, color_column=None, overlay=False, **kwargs):
        """
        Crea histograma
        Args:
            column: Columna numérica para el histograma
            bins: Número de bins
            color_column: Columna para colorear por categoría
            overlay: Si True, superpone histogramas; si False, los separa
        """
        if self.data is None or column not in self.data.columns:
            return go.Figure()
        
        if color_column and color_column in self.data.columns:
            # Histograma por categorías
            fig = px.histogram(
                self.data,
                x=column,
                color=color_column,
                nbins=bins,
                barmode='overlay' if overlay else 'group',
                opacity=0.7 if overlay else 1,
                color_discrete_map=self.species_colors if color_column == 'species' else None,
                title=""
            )
        else:
            # Histograma simple
            fig = px.histogram(
                self.data,
                x=column,
                nbins=bins,
                color_discrete_sequence=[self.colors['primary']],
                title=""
            )
        
        # Personalizar layout
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title='Frecuencia',
            bargap=0.1
        )
        
        return fig
    
    def create_density_plot(self, column, color_column=None, **kwargs):
        """
        Crea gráfica de densidad
        Args:
            column: Columna numérica
            color_column: Columna para colorear por categoría
        """
        if self.data is None or column not in self.data.columns:
            return go.Figure()
        
        fig = go.Figure()
        
        if color_column and color_column in self.data.columns:
            # Densidad por categorías
            for i, category in enumerate(self.data[color_column].unique()):
                data_subset = self.data[self.data[color_column] == category][column]
                
                fig.add_trace(go.Histogram(
                    x=data_subset,
                    histnorm='probability density',
                    name=str(category),
                    opacity=0.7,
                    marker_color=list(self.species_colors.values())[i] if color_column == 'species' else list(self.colors.values())[i]
                ))
        else:
            # Densidad simple
            fig.add_trace(go.Histogram(
                x=self.data[column],
                histnorm='probability density',
                marker_color=self.colors['primary'],
                opacity=0.7
            ))
        
        fig.update_layout(
            xaxis_title=column.replace('_', ' ').title(),
            yaxis_title='Densidad',
            barmode='overlay'
        )
        
        return fig