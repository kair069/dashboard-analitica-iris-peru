"""
Callbacks modulares usando las clases de gráficas
"""
from dash import callback, Input, Output
from data_loader import load_iris_data
from charts.time_series import TimeSeriesChart
from charts.pie_chart import PieChart
from charts.scatter_chart import ScatterChart
from charts.bar_chart import BarChart
from charts.histogram_chart import HistogramChart
from charts.box_plot import BoxPlotChart  # ← NUEVO: Import del BoxPlot

#NUEVO

from charts.heatmap import HeatmapChart  # ← Agregar esta línea

def register_callbacks(app):
    """Registra todos los callbacks usando clases modulares"""
    

    @app.callback(
    Output("heatmap-chart", "figure"),
    [Input("species-filter", "value")]
    )
    def update_heatmap_chart(species):
        """Actualiza heatmap usando clase modular"""
        df = load_iris_data()
        
        if species != "all":
            df = df[df['species'] == species]
        
        # Crear instancia de HeatmapChart
        chart = HeatmapChart(df)
        
        # Generar figura
        fig = chart.get_figure()
        
        return fig




    
    @app.callback(
        [Output("total-sessions", "children"),
         Output("total-users", "children"), 
         Output("avg-sepal", "children"),
         Output("species-count", "children")],
        [Input("species-filter", "value"),
         Input("region-filter", "value")]
    )
    def update_metrics(species, region):
        """Actualiza las métricas principales"""
        df = load_iris_data()
        
        # Aplicar filtros
        filtered_df = apply_filters(df, species, region)
        
        total_sessions = f"{filtered_df['sessions'].sum():,}"
        total_users = f"{filtered_df['users'].sum():,}"
        avg_sepal = f"{filtered_df['sepal length (cm)'].mean():.1f} cm"
        species_count = filtered_df['species'].nunique()
        
        return total_sessions, total_users, avg_sepal, species_count

    @app.callback(
        Output("time-series-chart", "figure"),
        [Input("species-filter", "value"),
         Input("region-filter", "value")]
    )
    def update_time_series(species, region):
        """Actualiza gráfica de series de tiempo usando clase modular"""
        df = load_iris_data()
        filtered_df = apply_filters(df, species, region)
        
        # Crear instancia de la clase TimeSeriesChart
        chart = TimeSeriesChart(filtered_df)
        
        # Generar la figura
        fig = chart.get_figure(date_range_days=30)
        
        return fig

    # ← NUEVO: Callback para el box plot
    @app.callback(
        Output("box-plot-chart", "figure"),
        [Input("species-filter", "value"),
         Input("boxplot-feature-selector", "value")]
    )
    def update_box_plot_chart(species, feature):
        """Actualiza box plot usando clase modular"""
        df = load_iris_data()
        
        # Aplicar filtro de especies si es necesario (pero para box plot es mejor mostrar comparación)
        # if species != "all":
        #     df = df[df['species'] == species]
        
        # Crear instancia de BoxPlotChart
        chart = BoxPlotChart(df)
        
        # Generar figura mostrando distribución por especies
        fig = chart.get_figure(
            y_column=feature,
            x_column='species',
            color_column='species'
        )
        
        return fig

    @app.callback(
        Output("pie-chart", "figure"),
        [Input("region-filter", "value")]
    )
    def update_pie_chart(region):
        """Actualiza gráfica de pie usando clase modular"""
        df = load_iris_data()
        
        # Para el pie chart, filtrar solo por región (mostrar todas las especies)
        if region != "all":
            df = df[df['region'] == region]
        
        # Crear instancia de PieChart
        chart = PieChart(df)
        
        # Generar figura tipo dona
        fig = chart.get_figure(value_column='species', is_donut=True)
        
        return fig

    @app.callback(
        Output("scatter-chart", "figure"),
        [Input("species-filter", "value"),
         Input("region-filter", "value")]
    )
    def update_scatter_chart(species, region):
        """Actualiza gráfica de dispersión usando clase modular"""
        df = load_iris_data()
        filtered_df = apply_filters(df, species, region)
        
        # Crear instancia de ScatterChart
        chart = ScatterChart(filtered_df)
        
        # Generar figura con línea de regresión
        fig = chart.get_figure(
            x_column='sepal length (cm)',
            y_column='petal length (cm)',
            color_column='species',
            add_regression=True
        )
        
        return fig

    @app.callback(
        Output("bar-chart", "figure"),
        [Input("species-filter", "value")]
    )
    def update_bar_chart(species):
        """Actualiza gráfica de barras usando clase modular"""
        df = load_iris_data()
        
        if species != "all":
            df = df[df['species'] == species]
        
        # Crear instancia de BarChart
        chart = BarChart(df)
        
        # Generar figura agrupando por región y sumando sesiones
        fig = chart.get_figure(
            x_column='region',
            y_column='sessions'
        )
        
        return fig

    # ← NUEVO: Callback para el histograma
    @app.callback(
        Output("histogram-chart", "figure"),
        [Input("species-filter", "value"),
         Input("feature-selector", "value")]
    )
    def update_histogram_chart(species, feature):
        """Actualiza histograma usando clase modular"""
        df = load_iris_data()
        
        # Aplicar filtro de especies si es necesario
        if species != "all":
            df = df[df['species'] == species]
        
        # Crear instancia de HistogramChart
        chart = HistogramChart(df)
        
        # Generar figura con overlapping por especies
        fig = chart.get_figure(
            column=feature,
            color_column='species',
            overlay=True,
            bins=25
        )
        
        return fig

def apply_filters(df, species=None, region=None):
    """
    Función auxiliar para aplicar filtros
    Args:
        df: DataFrame a filtrar
        species: Filtro de especies
        region: Filtro de región
    Returns:
        DataFrame filtrado
    """
    filtered_df = df.copy()
    
    if species and species != "all":
        filtered_df = filtered_df[filtered_df['species'] == species]
    
    if region and region != "all":
        filtered_df = filtered_df[filtered_df['region'] == region]
    
    return filtered_df