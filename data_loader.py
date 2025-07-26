"""
Cargador de datos simple
"""
import pandas as pd
from sklearn.datasets import load_iris
import numpy as np

def load_iris_data():
    """Carga y prepara el dataset Iris"""
    iris = load_iris()
    df = pd.DataFrame(iris.data, columns=iris.feature_names)
    df['species'] = iris.target_names[iris.target]
    
    # Datos simulados adicionales
    np.random.seed(42)
    n = len(df)
    df['sessions'] = np.random.poisson(50, n) + 20
    df['users'] = (df['sessions'] * np.random.uniform(0.6, 0.9, n)).astype(int)
    df['page_views'] = (df['sessions'] * np.random.uniform(2, 5, n)).astype(int)
    df['region'] = np.random.choice(['North America', 'Europe', 'Asia', 'South America'], n)
    
    return df