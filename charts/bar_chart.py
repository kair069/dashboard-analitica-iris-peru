"""
Gráficas de barras (vertical y horizontal)
"""
import plotly.express as px
import plotly.graph_objects as go
from .base_chart import BaseChart

class BarChart(BaseChart):
    """Gráficas de barras con diferentes configuraciones"""
    
    def create_figure(self, x_column, y_column=None, orientation='vertical', 
                     color_column=None, **kwargs):
        """
        Crea gráfica de barras
        Args:
            x_column: Columna para eje X (o categorías si y_column es None)
            y_column: Columna para eje Y (opcional, si None se hace conteo)
            orientation: 'vertical' o 'horizontal'
            color_column: Columna para colorear barras
        """
        if self.data is None or x_column not in self.data.columns:
            return go.Figure()
        
        # Si no se especifica y_column, hacer conteo de x_column
        if y_column is None:
            chart_data = self.data[x_column].value_counts().reset_index()
            chart_data.columns = [x_column, 'count']
            y_column = 'count'
        else:
            if y_column not in self.data.columns:
                return go.Figure()
            # Agrupar datos
            chart_data = self.data.groupby(x_column)[y_column].sum().reset_index()
        
        # Crear gráfica según orientación
        if orientation == 'horizontal':
            fig = px.bar(
                chart_data,
                x=y_column,
                y=x_column,
                orientation='h',
                color=color_column if color_column and color_column in chart_data.columns else y_column,
                color_continuous_scale='Blues' if not color_column else None,
                title=""
            )
        else:
            fig = px.bar(
                chart_data,
                x=x_column,
                y=y_column,
                color=color_column if color_column and color_column in chart_data.columns else y_column,
                color_continuous_scale='Blues' if not color_column else None,
                title=""
            )
        
        # Personalizar layout
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title(),
            yaxis_title=y_column.replace('_', ' ').title() if y_column != 'count' else 'Cantidad',
            showlegend=False if not color_column else True
        )
        
        return fig
    
    def create_grouped_bar(self, x_column, y_column, group_column, **kwargs):
        """
        Crea gráfica de barras agrupadas
        Args:
            x_column: Columna para eje X
            y_column: Columna para valores
            group_column: Columna para agrupar barras
        """
        required_columns = [x_column, y_column, group_column]
        if (self.data is None or 
            not all(col in self.data.columns for col in required_columns)):
            return go.Figure()
        
        fig = px.bar(
            self.data,
            x=x_column,
            y=y_column,
            color=group_column,
            barmode='group',
            color_discrete_map=self.species_colors if group_column == 'species' else None,
            title=""
        )
        
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title(),
            yaxis_title=y_column.replace('_', ' ').title()
        )
        
        return fig
    
    def create_stacked_bar(self, x_column, y_column, stack_column, **kwargs):
        """
        Crea gráfica de barras apiladas
        Args:
            x_column: Columna para eje X
            y_column: Columna para valores
            stack_column: Columna para apilar
        """
        required_columns = [x_column, y_column, stack_column]
        if (self.data is None or 
            not all(col in self.data.columns for col in required_columns)):
            return go.Figure()
        
        fig = px.bar(
            self.data,
            x=x_column,
            y=y_column,
            color=stack_column,
            barmode='stack',
            color_discrete_map=self.species_colors if stack_column == 'species' else None,
            title=""
        )
        
        fig.update_layout(
            xaxis_title=x_column.replace('_', ' ').title(),
            yaxis_title=y_column.replace('_', ' ').title()
        )
        
        return fig
    
    def create_waterfall_chart(self, categories, values, **kwargs):
        """
        Crea gráfica de cascada (waterfall)
        Args:
            categories: Lista de categorías
            values: Lista de valores
        """
        if len(categories) != len(values):
            return go.Figure()
        
        # Calcular valores acumulativos
        cumulative = [0]
        for i, val in enumerate(values[:-1]):
            cumulative.append(cumulative[-1] + val)
        
        fig = go.Figure()
        
        # Añadir barras
        for i, (cat, val) in enumerate(zip(categories, values)):
            fig.add_trace(go.Bar(
                x=[cat],
                y=[val],
                base=cumulative[i] if val > 0 else cumulative[i] + val,
                marker_color=self.colors['success'] if val > 0 else self.colors['danger'],
                name=cat
            ))
        
        fig.update_layout(
            showlegend=False,
            yaxis_title='Valor'
        )
        
        return fig