"""
Módulo de gráficas modulares para dashboard
"""
from .base_chart import BaseChart
from .time_series import TimeSeriesChart
from .pie_chart import PieChart
from .scatter_chart import ScatterChart
from .bar_chart import BarChart
from .histogram_chart import HistogramChart

# Exportar todas las clases
__all__ = [
    'BaseChart',
    'TimeSeriesChart', 
    'PieChart',
    'ScatterChart',
    'BarChart',
    'HistogramChart'
]

# Diccionario para fácil acceso a las gráficas
CHART_CLASSES = {
    'time_series': TimeSeriesChart,
    'pie': PieChart,
    'scatter': ScatterChart,
    'bar': BarChart,
    'histogram': HistogramChart
}

def get_chart_class(chart_type):
    """
    Obtiene una clase de gráfica por su tipo
    Args:
        chart_type: Tipo de gráfica ('time_series', 'pie', 'scatter', etc.)
    Returns:
        Clase de gráfica correspondiente
    """
    return CHART_CLASSES.get(chart_type, BaseChart)

def create_chart(chart_type, data=None):
    """
    Factory function para crear gráficas
    Args:
        chart_type: Tipo de gráfica
        data: DataFrame con los datos
    Returns:
        Instancia de la gráfica
    """
    chart_class = get_chart_class(chart_type)
    return chart_class(data)

# Ejemplo de uso:
"""
from charts import create_chart, TimeSeriesChart
import pandas as pd

# Método 1: Usar factory function
df = pd.read_csv('datos.csv')
chart = create_chart('time_series', df)
fig = chart.get_figure()

# Método 2: Importar clase directamente  
chart = TimeSeriesChart(df)
fig = chart.get_figure()

# Método 3: Importar todas las clases
from charts import *
chart = ScatterChart(df)
fig = chart.get_figure(x_column='x', y_column='y')
"""