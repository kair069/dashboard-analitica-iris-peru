"""
Gráfica de dispersión para el análisis de correlaciones
"""
import plotly.express as px
import plotly.graph_objects as go
from .base_chart import BaseChart

class ScatterPlot(BaseChart):
    """
    Gráfica de dispersión personalizada para el dataset Iris
    """
    
    def __init__(self, data=None):
        super().__init__(data)
        self.color_map = {
            'setosa': '#3b82f6',
            'versicolor': '#10b981', 
            'virginica': '#f59e0b'
        }
    
    def create_figure(self, x_col='Sepal Length (Cm)', y_col='Sepal Width (Cm)', 
                     color_col='Species', size_col=None, title=None):
        """
        Crea la gráfica de dispersión
        """
        if self.data is None:
            return go.Figure()
        
        # Crear la gráfica base
        fig = px.scatter(
            self.data,
            x=x_col,
            y=y_col,
            color=color_col,
            size=size_col if size_col else None,
            color_discrete_map=self.color_map,
            title=title or f'{y_col} vs {x_col}',
            opacity=0.7
        )
        
        # Personalizar markers
        fig.update_traces(
            marker=dict(
                size=8 if not size_col else None,
                line=dict(width=1, color='white'),
                sizemin=4
            )
        )
        
        # Personalizar hover
        hover_template = (
            f"<b>%{{customdata[0]}}</b><br>"
            f"{x_col}: %{{x}}<br>"
            f"{y_col}: %{{y}}"
        )
        
        if size_col:
            hover_template += f"<br>{size_col}: %{{marker.size}}"
        
        hover_template += "<extra></extra>"
        
        # Añadir datos personalizados para hover
        for trace in fig.data:
            species = trace.name
            species_data = self.data[self.data[color_col] == species]
            trace.customdata = species_data[[color_col]].values
            trace.hovertemplate = hover_template
        
        # Añadir línea de regresión si se solicita
        self.add_regression_line(fig, x_col, y_col)
        
        return fig
    
    def add_regression_line(self, fig, x_col, y_col):
        """
        Añade línea de regresión a la gráfica
        """
        import numpy as np
        from sklearn.linear_model import LinearRegression
        
        if self.data is None:
            return fig
        
        # Calcular regresión lineal
        X = self.data[x_col].values.reshape(-1, 1)
        y = self.data[y_col].values
        
        # Filtrar valores NaN
        mask = ~(np.isnan(X.flatten()) | np.isnan(y))
        X_clean = X[mask]
        y_clean = y[mask]
        
        if len(X_clean) < 2:
            return fig
        
        reg = LinearRegression().fit(X_clean, y_clean)
        
        # Crear línea de regresión
        x_range = np.linspace(X_clean.min(), X_clean.max(), 100).reshape(-1, 1)
        y_pred = reg.predict(x_range)
        
        # Añadir línea de regresión
        fig.add_trace(
            go.Scatter(
                x=x_range.flatten(),
                y=y_pred,
                mode='lines',
                name=f'Regression (R² = {reg.score(X_clean, y_clean):.3f})',
                line=dict(color='#6b7280', width=2, dash='dash'),
                hovertemplate='Regression Line<extra></extra>'
            )
        )
        
        return fig
    
    def create_matrix_plot(self, columns=None):
        """
        Crea una matriz de gráficas de dispersión
        """
        if self.data is None:
            return go.Figure()
        
        if columns is None:
            columns = ['Sepal Length (Cm)', 'Sepal Width (Cm)', 
                      'Petal Length (Cm)', 'Petal Width (Cm)']
        
        fig = px.scatter_matrix(
            self.data,
            dimensions=columns,
            color='Species',
            color_discrete_map=self.color_map,
            title='Feature Correlation Matrix'
        )
        
        fig.update_traces(
            diagonal_visible=False,
            marker=dict(size=4, opacity=0.6)
        )
        
        return fig