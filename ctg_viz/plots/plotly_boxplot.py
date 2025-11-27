import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure

def crear_plotly_boxplot_dispersión(df: pd.DataFrame, variable_y: str, clase_objetivo: str) -> Figure:
    """
    Genera un boxplot interactivo de Plotly con puntos de dispersión (tipo stripplot).
    Retorna el objeto figura de Plotly.
    """
    df_copy = df.copy()
    df_copy[clase_objetivo] = df_copy[clase_objetivo].astype(str)

    fig = px.box(
        df_copy, 
        x=clase_objetivo, 
        y=variable_y, 
        color=clase_objetivo,
        notched=True, 
        points="all", # Muestra los puntos individuales
        title=f'Boxplot Interactivo de {variable_y} por Clase'
    )
    fig.update_layout(xaxis_title=clase_objetivo, yaxis_title=variable_y)
    return fig