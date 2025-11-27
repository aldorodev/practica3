import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List

def crear_multi_boxplots(df: pd.DataFrame, variables_a_plotear: List[str], clase_objetivo: str, palette: str = 'Set2') -> plt.Figure:
    """
    Genera múltiples boxplots para comparar varias variables continuas 
    contra una clase objetivo. Retorna el objeto figura de Matplotlib.
    """
    num_plots = len(variables_a_plotear)
    if num_plots == 0:
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0.5, 0.5, "No hay variables para plotear", ha='center', va='center')
        ax.axis('off')
        return fig
        
    fig, axes = plt.subplots(
        1, num_plots, 
        figsize=(5 * num_plots, 6), 
        sharey=False 
    )
    
    if num_plots == 1:
        axes = [axes]

    for i, col in enumerate(variables_a_plotear):
        sns.boxplot(
            data=df,
            y=col,
            x=clase_objetivo, 
            ax=axes[i],
            palette=palette
        )
        axes[i].set_title(f'Boxplot de {col}', fontsize=14)
        axes[i].set_xlabel(f'Clase {clase_objetivo}')
        axes[i].grid(axis='y', linestyle='--')

    plt.tight_layout()
    return fig