import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def crear_kde_plot(df: pd.DataFrame, variable_densidad: str, clase_objetivo: str, palette: str = 'icefire') -> plt.Figure:
    """
    Genera un gráfico de Estimación de Densidad de Kernel (KDE) 
    segmentado por una clase objetivo. Retorna el objeto figura.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(
        data=df,
        x=variable_densidad,
        hue=clase_objetivo,
        fill=True,      
        alpha=.5,       
        linewidth=2,
        palette=palette,
        ax=ax
    )

    ax.set_title(f'Estimación de Densidad de Kernel (KDE) de {variable_densidad} por Clase', fontsize=16)
    ax.set_xlabel(variable_densidad)
    ax.set_ylabel('Densidad')
    return fig