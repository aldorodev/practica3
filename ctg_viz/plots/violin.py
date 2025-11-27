import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def crear_violin_swarmplot(df: pd.DataFrame, variable_violin: str, clase_objetivo: str, palette: str = 'Pastel2') -> plt.Figure:
    """
    Genera un gráfico de violín con un swarmplot superpuesto para visualizar 
    la distribución y los puntos individuales por clase. Retorna el objeto figura.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Gráfico de Violín
    sns.violinplot(
        x=clase_objetivo,
        y=variable_violin,
        data=df,
        inner=None, 
        palette=palette,
        ax=ax
    )

    # Swarmplot Superpuesto
    sns.swarmplot(
        x=clase_objetivo,
        y=variable_violin,
        data=df,
        color='k', 
        size=3,
        alpha=0.6, 
        ax=ax
    )

    ax.set_title(f'Distribución de {variable_violin} por Clase: Violín y Puntos Individuales', fontsize=16)
    ax.set_xlabel(f'Clase {clase_objetivo}')
    ax.set_ylabel(variable_violin)
    return fig