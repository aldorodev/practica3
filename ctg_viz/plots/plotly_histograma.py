import plotly.express as px
import pandas as pd
from plotly.graph_objects import Figure

def crear_plotly_histograma(df: pd.DataFrame, variable_continua: str, clase_objetivo: str) -> Figure:
    """
    Genera un histograma interactivo de Plotly, segmentado por una clase objetivo.
    Retorna el objeto figura de Plotly.
    """
    df_copy = df.copy()
    # Plotly prefiere strings o objetos para el 'color'
    df_copy[clase_objetivo] = df_copy[clase_objetivo].astype(str) 
    
    fig = px.histogram(
        df_copy, 
        x=variable_continua, 
        color=clase_objetivo,
        marginal="box", 
        nbins=50,
        title=f'Histograma Interactivo de {variable_continua} por Clase'
    )
    fig.update_layout(xaxis_title=variable_continua, yaxis_title="Conteo")
    return fig