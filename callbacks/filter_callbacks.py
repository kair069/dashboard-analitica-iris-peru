"""
Callbacks para filtros inteligentes y dinámicos
"""
from dash import callback, Input, Output, State, ALL, no_update, ctx
import dash_bootstrap_components as dbc
from dash import html
from data_loader import load_iris_data
import pandas as pd

def register_filter_callbacks(app):
    """Registra callbacks para filtros inteligentes"""
    
    # ================================================================
    # 1. FILTROS DINÁMICOS - Actualizar opciones basado en datos
    # ================================================================
    
    @app.callback(
        Output('region-filter', 'options'),
        Input('species-filter', 'value')
    )
    def update_region_options(selected_species):
        """Actualiza opciones de región basado en la especie seleccionada"""
        df = load_iris_data()
        
        if selected_species != 'all':
            df = df[df['species'] == selected_species]
        
        available_regions = df['region'].unique()
        
        options = [{"label": "Todas", "value": "all"}]
        options.extend([
            {"label": region, "value": region} 
            for region in sorted(available_regions)
        ])
        
        return options
    
    # ================================================================
    # 2. CONTADORES DINÁMICOS - Mostrar cuántos datos quedan
    # ================================================================
    
    @app.callback(
        [Output('filter-counter', 'children'),
         Output('filter-counter', 'color')],
        [Input('species-filter', 'value'),
         Input('region-filter', 'value')]
    )
    def update_filter_counter(species, region):
        """Muestra contador de registros filtrados"""
        df = load_iris_data()
        total_records = len(df)
        
        # Aplicar filtros
        if species != 'all':
            df = df[df['species'] == species]
        if region != 'all':
            df = df[df['region'] == region]
        
        filtered_records = len(df)
        percentage = (filtered_records / total_records) * 100
        
        # Color según porcentaje
        if percentage > 75:
            color = "success"
        elif percentage > 50:
            color = "warning"
        elif percentage > 25:
            color = "info"
        else:
            color = "danger"
        
        counter_text = f"{filtered_records} de {total_records} registros ({percentage:.1f}%)"
        
        return counter_text, color
    
    # ================================================================
    # 3. RESET FILTERS - Botón para limpiar todos los filtros
    # ================================================================
    
    @app.callback(
        [Output('species-filter', 'value'),
         Output('region-filter', 'value'),
         Output('feature-selector', 'value'),
         Output('boxplot-feature-selector', 'value')],
        Input('reset-filters-btn', 'n_clicks'),
        prevent_initial_call=True
    )
    def reset_all_filters(n_clicks):
        """Resetea todos los filtros a valores por defecto"""
        if n_clicks:
            return 'all', 'all', 'sepal length (cm)', 'sepal length (cm)'
        return no_update, no_update, no_update, no_update
    
    # ================================================================
    # 4. FILTROS AVANZADOS - Rangos numéricos
    # ================================================================
    
    @app.callback(
        Output('advanced-filters-collapse', 'is_open'),
        Input('advanced-filters-toggle', 'n_clicks'),
        State('advanced-filters-collapse', 'is_open')
    )
    def toggle_advanced_filters(n_clicks, is_open):
        """Toggle para mostrar/ocultar filtros avanzados"""
        if n_clicks:
            return not is_open
        return is_open
    
    @app.callback(
        [Output('sepal-length-range', 'min'),
         Output('sepal-length-range', 'max'),
         Output('sepal-length-range', 'value'),
         Output('sepal-width-range', 'min'),
         Output('sepal-width-range', 'max'),
         Output('sepal-width-range', 'value')],
        Input('species-filter', 'value')
    )
    def update_range_sliders(selected_species):
        """Actualiza rangos de sliders basado en datos filtrados"""
        df = load_iris_data()
        
        if selected_species != 'all':
            df = df[df['species'] == selected_species]
        
        # Rangos para sepal length
        sepal_min = df['sepal length (cm)'].min()
        sepal_max = df['sepal length (cm)'].max()
        sepal_values = [sepal_min, sepal_max]
        
        # Rangos para sepal width
        width_min = df['sepal width (cm)'].min()
        width_max = df['sepal width (cm)'].max()
        width_values = [width_min, width_max]
        
        return (sepal_min, sepal_max, sepal_values, 
                width_min, width_max, width_values)
    
    # ================================================================
    # 5. FILTROS INTELIGENTES - Sugerencias automáticas
    # ================================================================
    
    @app.callback(
        Output('filter-suggestions', 'children'),
        [Input('species-filter', 'value'),
         Input('region-filter', 'value')]
    )
    def show_filter_suggestions(species, region):
        """Muestra sugerencias inteligentes de filtros"""
        df = load_iris_data()
        suggestions = []
        
        # Sugerencia basada en datos
        if species == 'all' and region == 'all':
            # Mostrar la especie más común
            most_common_species = df['species'].value_counts().index[0]
            suggestions.append(
                dbc.Alert([
                    html.I(className="fas fa-lightbulb me-2"),
                    f"💡 La especie más común es {most_common_species.title()}. ",
                    dbc.Button("Filtrar", color="link", size="sm", 
                              id={'type': 'suggestion-btn', 'species': most_common_species},
                              className="p-0 text-decoration-underline")
                ], color="info", className="py-2 px-3 mb-2", dismissable=True)
            )
        
        if species != 'all' and region == 'all':
            # Mostrar región más común para esa especie
            species_data = df[df['species'] == species]
            most_common_region = species_data['region'].value_counts().index[0]
            suggestions.append(
                dbc.Alert([
                    html.I(className="fas fa-map-marker-alt me-2"),
                    f"🌍 Para {species}, la región principal es {most_common_region}. ",
                    dbc.Button("Aplicar", color="link", size="sm",
                              id={'type': 'suggestion-btn', 'region': most_common_region},
                              className="p-0 text-decoration-underline")
                ], color="success", className="py-2 px-3 mb-2", dismissable=True)
            )
        
        return suggestions
    
    # ================================================================
    # 6. PRESETS DE FILTROS - Configuraciones predefinidas
    # ================================================================
    
    @app.callback(
        [Output('species-filter', 'value', allow_duplicate=True),
         Output('region-filter', 'value', allow_duplicate=True)],
        Input('filter-preset-dropdown', 'value'),
        prevent_initial_call=True
    )
    def apply_filter_preset(preset):
        """Aplica configuraciones predefinidas de filtros"""
        presets = {
            'all': ('all', 'all'),
            'setosa-na': ('setosa', 'North America'),
            'versicolor-eu': ('versicolor', 'Europe'),
            'virginica-asia': ('virginica', 'Asia'),
            'large-flowers': ('virginica', 'all'),  # Virginica tiene flores más grandes
            'small-flowers': ('setosa', 'all')      # Setosa tiene flores más pequeñas
        }
        
        if preset in presets:
            return presets[preset]
        
        return no_update, no_update
    
    # ================================================================
    # 7. HISTORIAL DE FILTROS - Guardar configuraciones recientes
    # ================================================================
    
    @app.callback(
        Output('filter-history-store', 'data'),
        [Input('species-filter', 'value'),
         Input('region-filter', 'value')],
        State('filter-history-store', 'data')
    )
    def update_filter_history(species, region, history_data):
        """Guarda historial de configuraciones de filtros"""
        if history_data is None:
            history_data = []
        
        current_config = {
            'species': species,
            'region': region,
            'timestamp': pd.Timestamp.now().isoformat()
        }
        
        # Evitar duplicados recientes
        if not history_data or history_data[-1] != current_config:
            history_data.append(current_config)
            
            # Mantener solo los últimos 5
            if len(history_data) > 5:
                history_data = history_data[-5:]
        
        return history_data
    
    # ================================================================
    # 8. VALIDACIÓN DE FILTROS - Prevenir configuraciones inválidas
    # ================================================================
    
    @app.callback(
        Output('filter-warning', 'children'),
        [Input('species-filter', 'value'),
         Input('region-filter', 'value')]
    )
    def validate_filter_combination(species, region):
        """Valida que la combinación de filtros tenga datos"""
        df = load_iris_data()
        
        # Aplicar filtros
        if species != 'all':
            df = df[df['species'] == species]
        if region != 'all':
            df = df[df['region'] == region]
        
        if len(df) == 0:
            return dbc.Alert([
                html.I(className="fas fa-exclamation-triangle me-2"),
                "⚠️ No hay datos disponibles para esta combinación de filtros."
            ], color="warning", className="py-2 px-3")
        
        if len(df) < 5:
            return dbc.Alert([
                html.I(className="fas fa-info-circle me-2"),
                f"📊 Solo {len(df)} registros disponibles. Los resultados pueden ser limitados."
            ], color="info", className="py-2 px-3")
        
        return []