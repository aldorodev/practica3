import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def crear_lineplot_tendencia(df: pd.DataFrame, variable_linea: str, muestra: int = 300, color: str = 'darkblue') -> plt.Figure:
    """
    Genera un lineplot para visualizar una tendencia de una variable continua 
    a lo largo del índice del DataFrame (simulando tiempo). Retorna el objeto figura.
    """
    df_line = df.sort_index().reset_index()
    
    # Tomamos una muestra para que el gráfico sea legible
    if len(df_line) > muestra:
        df_plot = df_line.sample(n=muestra, random_state=42).sort_values('index')
    else:
        df_plot = df_line

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.lineplot(
        data=df_plot, 
        x='index', 
        y=variable_linea,
        color=color,
        alpha=0.6,
        ax=ax
    )
    ax.set_title(f'Tendencia de {variable_linea} a lo largo del Índice (Simulación Temporal)', fontsize=16)
    ax.set_xlabel('Índice de Registro (Tiempo Simulado)')
    ax.set_ylabel(variable_linea)
    ax.grid(True, linestyle=':')
    return fig