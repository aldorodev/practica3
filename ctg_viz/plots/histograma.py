import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List

def crear_histograma_con_densidad(df: pd.DataFrame, variable_continua: str, clase_objetivo: str, palette: str = 'viridis') -> plt.Figure:
    """
    Genera un histograma de densidad con KDE, segmentado por una clase objetivo.
    Retorna el objeto figura de Matplotlib.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(
        data=df,
        x=variable_continua,
        hue=clase_objetivo,
        kde=True,
        palette=palette, 
        element="step",     
        stat="density",     
        common_norm=False,
        ax=ax
    )
    ax.set_title(f'Distribución de {variable_continua} por Clase Objetivo ({clase_objetivo})', fontsize=16)
    ax.set_xlabel(variable_continua)
    ax.set_ylabel('Densidad')
    ax.grid(axis='y', linestyle='--')
    
    # Intento de leyenda basada en las clases
    try:
        clases = sorted(df[clase_objetivo].unique())
        labels = [f'Clase {c}' for c in clases]
        ax.legend(title=clase_objetivo, labels=labels)
    except Exception:
        pass 
        
    return fig