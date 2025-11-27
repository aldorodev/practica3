import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import sys

# Importamos las funciones directamente desde nuestra librería instalada 'ctg_viz'
from ctg_viz import (
    crear_histograma_con_densidad,
    crear_multi_boxplots,
    crear_barras_frecuencia,
    crear_plotly_histograma,
    crear_heatmap_correlacion
)

# --- CONFIGURACIÓN DE VARIABLES ---
CLASE_OBJETIVO = 'NSP'
VAR_HISTOGRAMA = 'ASTV'
VAR_MULTIPLOT = ['LBE', 'ALTV', 'MLTV']
DATA_FILE = "CTG.csv"


# --- FUNCIÓN DE CARGA Y LIMPIEZA DE DATOS ---
def load_and_clean_data(file_path):
    """Carga y limpia el DataFrame CTG."""
    if not os.path.exists(file_path):
        print(f"Error: No se encontró el archivo {file_path}. Asegúrate de que esté en el directorio de ejecución.")
        # Usamos sys.exit(1) para terminar el programa en caso de error crítico
        sys.exit(1)

    print(f"Cargando y limpiando datos desde {file_path}...")
    df = pd.read_csv(file_path)
    
    # 1. Eliminar columnas no relevantes/de metadatos
    cols_a_eliminar = ['FileName', 'Date', 'SegFile', 'b', 'e']
    df_depurado = df.drop(columns=cols_a_eliminar, errors='ignore')
    
    # 2. Limpiar NaNs y asegurar tipos correctos
    df_depurado = df_depurado.dropna()
    df_depurado[CLASE_OBJETIVO] = pd.to_numeric(df_depurado[CLASE_OBJETIVO], errors='coerce').astype('Int64')
    df_depurado = df_depurado.dropna(subset=[CLASE_OBJETIVO])
    
    print(f"Datos cargados y limpios. Filas: {len(df_depurado)}")
    return df_depurado.copy()


# --- EJECUCIÓN DE GRÁFICAS ---
def run_plots(df):
    
    # 1. Gráfico Matplotlib/Seaborn: Histograma (Se requiere fig.show() para abrir la ventana)
    print("\n--- 1. Ejecutando Histograma con Densidad (Matplotlib) ---")
    fig_hist = crear_histograma_con_densidad(
        df=df, 
        variable_continua=VAR_HISTOGRAMA, 
        clase_objetivo=CLASE_OBJETIVO
    )
    fig_hist.show()
    
    # 2. Gráfico Matplotlib/Seaborn: Multi Boxplots
    print("\n--- 2. Ejecutando Multi Boxplots (Matplotlib) ---")
    fig_box = crear_multi_boxplots(
        df=df, 
        variables_a_plotear=[v for v in VAR_MULTIPLOT if v in df.columns],
        clase_objetivo=CLASE_OBJETIVO
    )
    fig_box.show()
    
    # 3. Gráfico Matplotlib/Seaborn: Heatmap
    print("\n--- 3. Ejecutando Heatmap de Correlación (Matplotlib) ---")
    fig_heatmap = crear_heatmap_correlacion(df=df)
    fig_heatmap.show()
    
    # 4. Gráfico Plotly (Se abre en el navegador)
    print("\n--- 4. Ejecutando Histograma Interactivo (Plotly) ---")
    fig_plotly = crear_plotly_histograma(
        df=df, 
        variable_continua=VAR_HISTOGRAMA, 
        clase_objetivo=CLASE_OBJETIVO
    )
    # Plotly Express tiene su propia función show() que lanza el navegador
    fig_plotly.show()
    print("El gráfico de Plotly se ha abierto en tu navegador web por defecto.")
    
    # Bloquea hasta que se cierren las figuras de Matplotlib
    plt.show() 


if __name__ == "__main__":
    df_depurado = load_and_clean_data(DATA_FILE)
    run_plots(df_depurado)