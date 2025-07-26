"""
Gráfica de dispersión/scatter plot
"""
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression
from .base_chart import BaseChart

class ScatterChart(BaseChart):
    """Gráfica de dispersión con opciones avanzadas"""
    
    def create_figure(self, x_column, y_column, color_column='species', 
                     size_column=None, add_regression=False, **kwargs):
        """
        Crea gráfica de dispersión
        Args:
            x_column: Columna para eje X
            y_column: Columna para eje Y  
            color_column: Columna para colorear puntos
            size_column: Columna para tamaño de puntos (opcional)
            add_regression: Si agregar línea de regresión
        """
        if (self.data is None or 
            x_column not in self.data.columns or 
            y_column not in self.data.columns):
            return go.Figure()
        
        # Crear gráfica base con plotly express
        fig = px.scatter(
            self.data,
            x=x_column,
            y=y_column,
            color=color_column if color_column in self.data.columns else None,
            size=size_column if size_column and size_column in self.data.columns else None,
            color_discrete_map=self.species_colors if color_column == 'species' else None,
            opacity=0.7,
            title=""
        )
        
        # Personalizar markers
        fig.update_traces(
            marker=dict(
                size=8 if not size_column else None,
                line=dict(width=1, color='white'),
                sizemin=4
            )
        )
        
        # Agregar línea de regresión si se solicita
        if add_regression:
            self._add_regression_line(fig, x_column, y_column)
        
        # Actualizar labels
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title(),
            yaxis_title=y_column.replace('_', ' ').title()
        )
        
        return fig
    
    def _add_regression_line(self, fig, x_column, y_column):
        """Añade línea de regresión a la gráfica"""
        try:
            # Preparar datos sin valores NaN
            mask = ~(self.data[x_column].isna() | self.data[y_column].isna())
            x_clean = self.data[mask][x_column].values.reshape(-1, 1)
            y_clean = self.data[mask][y_column].values
            
            if len(x_clean) < 2:
                return fig
            
            # Calcular regresión
            reg = LinearRegression().fit(x_clean, y_clean)
            
            # Crear línea de regresión
            x_range = np.linspace(x_clean.min(), x_clean.max(), 100).reshape(-1, 1)
            y_pred = reg.predict(x_range)
            
            # Añadir línea
            fig.add_trace(go.Scatter(
                x=x_range.flatten(),
                y=y_pred,
                mode='lines',
                name=f'Regresión (R² = {reg.score(x_clean, y_clean):.3f})',
                line=dict(color='#6b7280', width=2, dash='dash'),
                hovertemplate='Línea de Regresión<extra></extra>'
            ))
            
        except Exception as e:
            print(f"Error al agregar línea de regresión: {e}")
        
        return fig
    
    def create_matrix_plot(self, columns=None, **kwargs):
        """
        Crea matriz de scatter plots
        Args:
            columns: Lista de columnas para la matriz
        """
        if self.data is None:
            return go.Figure()
        
        if columns is None:
            # Usar columnas numéricas por defecto
            numeric_columns = self.data.select_dtypes(include=[np.number]).columns
            columns = numeric_columns[:4] if len(numeric_columns) >= 4 else numeric_columns
        
        # Filtrar columnas que existen
        columns = [col for col in columns if col in self.data.columns]
        
        if len(columns) < 2:
            return go.Figure()
        
        fig = px.scatter_matrix(
            self.data,
            dimensions=columns,
            color='species' if 'species' in self.data.columns else None,
            color_discrete_map=self.species_colors,
            title=""
        )
        
        fig.update_traces(
            diagonal_visible=False,
            marker=dict(size=4, opacity=0.6)
        )
        
        return fig
    
    def create_bubble_chart(self, x_column, y_column, size_column, color_column='species', **kwargs):
        """
        Crea gráfica de burbujas
        Args:
            x_column: Columna para eje X
            y_column: Columna para eje Y
            size_column: Columna para tamaño de burbujas
            color_column: Columna para color
        """
        required_columns = [x_column, y_column, size_column]
        if (self.data is None or 
            not all(col in self.data.columns for col in required_columns)):
            return go.Figure()
        
        fig = px.scatter(
            self.data,
            x=x_column,
            y=y_column,
            size=size_column,
            color=color_column if color_column in self.data.columns else None,
            color_discrete_map=self.species_colors if color_column == 'species' else None,
            size_max=20,
            opacity=0.7
        )
        
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title(),
            yaxis_title=y_column.replace('_', ' ').title()
        )
        
        return fig