import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List

def crear_dot_boxplot(df: pd.DataFrame, variable_dot: str, clase_objetivo: str, clases_a_comparar: List[int] = [1, 3], palette: str = 'tab10') -> plt.Figure:
    """
    Genera un Dot Plot (Stripplot) superpuesto con un Boxplot para comparar 
    una variable continua entre dos clases específicas. Retorna el objeto figura.
    """
    if len(clases_a_comparar) != 2:
        raise ValueError("Se requieren exactamente 2 clases para la comparación visual óptima.")

    df_dot = df[df[clase_objetivo].isin(clases_a_comparar)].copy()
    df_dot[clase_objetivo] = df_dot[clase_objetivo].astype(str)

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 1. Stripplot (Dot Plot)
    sns.stripplot(
        data=df_dot,
        y=variable_dot,
        x=clase_objetivo,
        hue=clase_objetivo,
        size=5,
        jitter=True, 
        palette=palette,
        legend=False,
        ax=ax
    )
    
    # 2. Boxplot (Superpuesto para contexto)
    sns.boxplot(
        data=df_dot,
        y=variable_dot,
        x=clase_objetivo,
        color='white',
        width=0.3,
        linewidth=1,
        ax=ax
    )

    ax.set_title(f'Dot Plot (Comparación) de {variable_dot} entre Clases {clases_a_comparar[0]} y {clases_a_comparar[1]}', fontsize=16)
    ax.set_xlabel(clase_objetivo)
    ax.set_ylabel(variable_dot)
    ax.grid(axis='y', linestyle='--')
    return fig