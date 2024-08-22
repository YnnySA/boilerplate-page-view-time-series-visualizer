# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 15:25:31 2024

@author: Yenny SA
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
df = pd.read_csv("fcc-forum-pageviews.csv", 
                 parse_dates=["date"], 
                 index_col="date")


# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025))&
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_bar_plot(df):
    
    # Verificar si el índice es de tipo datetime
    if not pd.api.types.is_datetime64_any_dtype(df.index):
        raise TypeError("El índice del DataFrame debe ser de tipo datetime.")
    
    # Hacer una copia del DataFrame
    df_copy = df.copy()

    # Extraer el año y el mes del índice
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.strftime('%B')

    # Agrupar por año y mes, luego calcular el promedio de visitas
    df_grouped = df_copy.groupby(['year', 'month'])['value'].mean().unstack()

    # Graficar
    ax = df_grouped.plot(kind='bar', figsize=(12, 8))

    # Configurar las etiquetas y el título
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.set_title('Average Daily Page Views per Month')
    ax.legend(title='Months')

    # Mostrar la gráfica
    plt.show()

    
draw_bar_plot(df)
