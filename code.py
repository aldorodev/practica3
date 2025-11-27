import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Imports de limpieza y preprocesamiento
from ctg_viz import eliminar_columnas_con_nulos, imputar_valores, verificar_unicos_outliers, detectar_outliers_iqr, capping
from ctg_viz.categorization import check_data_completeness_AldoAlbertoRodriguezFlores

# Imports de visualización
from ctg_viz import (
    crear_histograma_con_densidad,
    crear_multi_boxplots,
    crear_barras_frecuencia,
    crear_lineplot_tendencia,
    crear_dot_boxplot,
    crear_kde_plot,
    crear_violin_swarmplot,
    crear_heatmap_correlacion
)


CLASE_OBJETIVO = 'NSP'
VAR_CONTINUA_PRINCIPAL = 'ASTV'
VAR_MULTIPLOT = ['LBE', 'ALTV', 'MLTV']
DATA_PATH = "dataset/CTG.csv" 
PLOTS_DIR = "plots_output" 


# =================================================================
#  Carga y Preprocesamiento de Datos
# =================================================================

if not os.path.exists(DATA_PATH):
    print(f"Error: No se encontró el archivo en la ruta '{DATA_PATH}'.")
    sys.exit(1)

df = pd.read_csv(DATA_PATH)
df = eliminar_columnas_con_nulos(df, umbral_porcentaje=0.20)
print("-------------------------------------------------")
print("Datos después de eliminar columnas con nulos:")
print(df.head())
print(f"Shape: {df.shape}")

df = imputar_valores(df, metodo_num="mediana")

# Lista de columnas APTAS 
columnas_aptas = verificar_unicos_outliers(df)

# Detectar outliers en las columnas aptas
outliers_resultado = detectar_outliers_iqr(df, columnas=columnas_aptas) 
columnas_para_capping = outliers_resultado.keys()
print("\n-------------------------------------------------")
print("Columnas para Capping (Outliers detectados):")
print(columnas_para_capping) 

# Columnas con capping
df_capping = capping(df, columnas=columnas_para_capping)

print("\n-------------------------------------------------")
print("Capping aplicado:")
print(df_capping.head())

# Presentacion de datos de la función para Analisis de Datos
reporte = check_data_completeness_AldoAlbertoRodriguezFlores(df_capping)
print("\n-------------------------------------------------")
print("Reporte de Integridad del DataFrame Final (df_capping):")
print("-------------------------------------------------")
print(reporte.iloc[:, 0:5])
print(reporte.iloc[:, 5:10]) 



print("\n\n=================================================")
print("  Grafícas Estáticas con Matplotlib/Seaborn  ")
print("=================================================")

#Crear el directorio de salida
if not os.path.exists(PLOTS_DIR):
    os.makedirs(PLOTS_DIR)
    print(f"Directorio de salida creado: '{PLOTS_DIR}/'")

print("\n--- Generando, Guardando (PNG) y Mostrando las 8 Gráficas Estáticas ---")

# Histogramas 
fig = crear_histograma_con_densidad(df_capping, VAR_CONTINUA_PRINCIPAL, CLASE_OBJETIVO)
fig.savefig(os.path.join(PLOTS_DIR, '01_histograma_densidad.png'))
print("Generado: 01_histograma_densidad.png")
fig.show() 

# Boxplots 
valid_vars = [v for v in VAR_MULTIPLOT if v in df_capping.columns]
fig = crear_multi_boxplots(df_capping, valid_vars, CLASE_OBJETIVO)
fig.savefig(os.path.join(PLOTS_DIR, '02_multi_boxplots.png'))
print("Generado: 02_multi_boxplots.png")
fig.show()

# Barras Horizontales 
fig = crear_barras_frecuencia(df_capping, CLASE_OBJETIVO)
fig.savefig(os.path.join(PLOTS_DIR, '03_barras_frecuencia.png'))
print("Generado: 03_barras_frecuencia.png")
fig.show()

# Líneas 
fig = crear_lineplot_tendencia(df_capping, VAR_CONTINUA_PRINCIPAL)
fig.savefig(os.path.join(PLOTS_DIR, '04_lineplot_tendencia.png'))
print("Generado: 04_lineplot_tendencia.png")
fig.show()

# Dot Plots
fig = crear_dot_boxplot(df_capping, VAR_CONTINUA_PRINCIPAL, CLASE_OBJETIVO, clases_a_comparar=[1, 3])
fig.savefig(os.path.join(PLOTS_DIR, '05_dot_boxplot.png'))
print("Generado: 05_dot_boxplot.png")
fig.show()

# Densidad (KDE)
fig = crear_kde_plot(df_capping, VAR_CONTINUA_PRINCIPAL, CLASE_OBJETIVO)
fig.savefig(os.path.join(PLOTS_DIR, '06_kde_densidad.png'))
print("Generado: 06_kde_densidad.png")
fig.show()

# Violín
fig = crear_violin_swarmplot(df_capping, VAR_CONTINUA_PRINCIPAL, CLASE_OBJETIVO)
fig.savefig(os.path.join(PLOTS_DIR, '07_violin_swarmplot.png'))
print("Generado: 07_violin_swarmplot.png")
fig.show()

# Heatmap
fig = crear_heatmap_correlacion(df_capping)
fig.savefig(os.path.join(PLOTS_DIR, '08_heatmap_correlacion.png'))
print("Generado: 08_heatmap_correlacion.png")
fig.show()


# Se bloquea la ejecución hasta que el usuario cierre las ventanas de Matplotlib
print("\n=================================================")
print(f"Archivos PNG guardados en el directorio: '{PLOTS_DIR}/'")
print("El script pausado hasta cerrar todas las ventanas de gráficas estáticas.")
plt.show()