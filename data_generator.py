import numpy as np
import pandas as pd

def generate_data():
    """Генерация случайных данных и создание Series"""
    data = np.random.randint(-10_000, 10_001, size=1_000)
    return pd.Series(data, name='Значения')

def prepare_data(series):
    """Подготовка данных для визуализации"""
    sorted_asc = series.sort_values().reset_index(drop=True)
    sorted_desc = series.sort_values(ascending=False).reset_index(drop=True)
    rounded_series = series.apply(lambda x: round(x/100) * 100)
    
    return sorted_asc, sorted_desc, rounded_series 