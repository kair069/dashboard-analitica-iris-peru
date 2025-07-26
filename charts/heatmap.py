"""
Gráfica de mapa de calor para correlaciones
"""
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from .base_chart import BaseChart

class HeatmapChart(BaseChart):
    """Gráfica de mapa de calor para análisis de correlaciones"""
    
    def create_figure(self, columns=None, correlation_method='pearson', **kwargs):
        """
        Crea mapa de calor de correlación
        Args:
            columns: Lista de columnas numéricas (si None, usa todas las numéricas)
            correlation_method: 'pearson', 'spearman', 'kendall'
        """
        if self.data is None:
            return go.Figure()
        
        # Seleccionar columnas numéricas
        if columns is None:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns.tolist()
            # Filtrar columnas de características de iris
            columns = [col for col in numeric_cols if any(word in col.lower() 
                      for word in ['sepal', 'petal', 'length', 'width'])]
        
        # Verificar que las columnas existen
        columns = [col for col in columns if col in self.data.columns]
        
        if len(columns) < 2:
            return go.Figure()
        
        # Calcular matriz de correlación
        corr_matrix = self.data[columns].corr(method=correlation_method)
        
        # Crear el heatmap
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='<b>%{y} vs %{x}</b><br>Correlación: %{z:.3f}<extra></extra>'
        ))
        
        # Personalizar layout
        fig.update_layout(
            xaxis_title='',
            yaxis_title='',
            width=600,
            height=400,
            margin=dict(l=50, r=30, t=30, b=50)  # ← Márgenes específicos para heatmap
        )
        
        return fig
    
    def create_clustermap(self, columns=None, **kwargs):
        """
        Crea mapa de calor con clustering (agrupación)
        """
        # Implementación básica sin clustering por simplicidad
        return self.create_figure(columns=columns, **kwargs)