import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def crear_barras_frecuencia(df: pd.DataFrame, variable_discreta: str, palette: str = 'Pastel1') -> plt.Figure:
    """
    Genera un gráfico de barras horizontales para mostrar la frecuencia 
    descendente de una variable discreta o categórica. Retorna el objeto figura.
    """
    frecuencia = df[variable_discreta].value_counts().sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=frecuencia.values,
        y=frecuencia.index.astype(str),
        palette=palette,
        orient='h',
        ax=ax
    )
    ax.set_title(f'Frecuencia Descendente de {variable_discreta}', fontsize=16)
    ax.set_xlabel('Conteo')
    ax.set_ylabel(variable_discreta)
    ax.grid(axis='x', linestyle='--')
    return fig