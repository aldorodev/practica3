import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import pandas.api.types

def crear_heatmap_correlacion(df: pd.DataFrame, metodo: str = 'spearman', cmap: str = 'coolwarm', figsize: tuple = (16, 14)) -> plt.Figure:
    """
    Genera un Heatmap de correlación para todas las variables numéricas del DataFrame.
    Retorna el objeto figura.
    """
    # Seleccionar solo columnas numéricas
    cols_corr = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    df_corr = df[cols_corr]

    # Calcular la matriz de correlación
    matriz_corr = df_corr.corr(method=metodo)

    # Generar el Heatmap
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        matriz_corr,
        annot=True,     
        cmap=cmap, 
        fmt=".2f",      
        linewidths=.5,  
        cbar_kws={'label': f'Coeficiente de Correlación de {metodo.capitalize()}'},
        ax=ax
    )
    ax.set_title(f'Heatmap de Correlación (Método: {metodo.capitalize()})', fontsize=18)
    return fig