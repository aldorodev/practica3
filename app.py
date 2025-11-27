import streamlit as st
import pandas as pd
import os
import sys


from ctg_viz import (
    eliminar_columnas_con_nulos, imputar_valores, verificar_unicos_outliers, 
    detectar_outliers_iqr, capping
)


from ctg_viz import (
    crear_histograma_con_densidad, crear_multi_boxplots, crear_barras_frecuencia,
    crear_lineplot_tendencia, crear_dot_boxplot, crear_kde_plot, 
    crear_violin_swarmplot, crear_heatmap_correlacion,
    crear_plotly_histograma, crear_plotly_boxplot_dispersión
)


CLASE_OBJETIVO = 'NSP'
VAR_CONTINUA_PRINCIPAL = 'ASTV'
VAR_MULTIPLOT = ['LBE', 'ALTV', 'MLTV']
DATA_PATH = "dataset/CTG.csv" 


PLOT_OPTIONS = {
    "Histograma (Seaborn/KDE)": crear_histograma_con_densidad,
    "Gráfico de Densidad (Seaborn)": crear_kde_plot, 
    "Dot Plot (Seaborn)": crear_dot_boxplot, 
    "Gráfico de Violín/Swarmplot (Seaborn)": crear_violin_swarmplot, 
    "Histograma Interactivo (Plotly)": crear_plotly_histograma, 
    "Boxplot Interactivo (Plotly)": crear_plotly_boxplot_dispersión,
    
    "Gráfico de Líneas (Seaborn)": crear_lineplot_tendencia, # Solo necesita var. continua
    "Boxplots Múltiples (Seaborn)": crear_multi_boxplots, # Necesita lista de vars
    "Barras de Frecuencia (Seaborn)": crear_barras_frecuencia, # Necesita var. discreta
    "Heatmap de Correlación (Seaborn)": crear_heatmap_correlacion, # Solo necesita df
}

@st.cache_data
def load_and_preprocess_data(file_path):
    """Carga y aplica todo el preprocesamiento definido en tu flujo de trabajo."""
    if not os.path.exists(file_path):
        st.error(f"Error: No se encontró el archivo en la ruta '{file_path}'.")
        sys.exit(1)

    df = pd.read_csv(file_path)
    
    # Preprocesamiento
    df = eliminar_columnas_con_nulos(df, umbral_porcentaje=0.20)
    df = imputar_valores(df, metodo_num="mediana")
    columnas_aptas = verificar_unicos_outliers(df)
    outliers_resultado = detectar_outliers_iqr(df, columnas=columnas_aptas) 
    columnas_para_capping = outliers_resultado.keys()
    df_capping = capping(df, columnas=columnas_para_capping)
    
    return df_capping


# streamlit
def main():
    st.set_page_config(layout="wide")
    st.title("🩺 Análisis de Registros Cardiotocográficos (CTG)")
    
    
    df_capping = load_and_preprocess_data(DATA_PATH)
    
    st.sidebar.header("📊 Configuración de Visualización")
    
    
    plot_selection = st.sidebar.selectbox(
        "Elige el Tipo de Gráfica:",
        list(PLOT_OPTIONS.keys())
    )

    # Lista de variables disponibles para la selección
    continuous_cols = [col for col in df_capping.columns if col not in [CLASE_OBJETIVO]]
    
    # Mostrar/Ocultar y Seleccionar Variable Continua
    # Solo mostramos el selector si la gráfica lo requiere
    if plot_selection not in ["Boxplots Múltiples (Seaborn)", "Barras de Frecuencia (Seaborn)", "Heatmap de Correlación (Seaborn)"]:
        variable_seleccionada = st.sidebar.selectbox(
            "Selecciona la Variable Continua:",
            continuous_cols,
            index=continuous_cols.index(VAR_CONTINUA_PRINCIPAL)
        )
    else:
        # Usamos un valor por defecto o None si no se necesita
        variable_seleccionada = None 


    # Mostrar Datos 
    if st.sidebar.checkbox("Mostrar DataFrame Depurado"):
        st.subheader("DataFrame Procesado (df_capping)")
        st.dataframe(df_capping.head())
        
    st.markdown("---")
    
    # Generar y Mostrar Gráfica 
    st.subheader(f"Gráfica Generada: {plot_selection}")
    
   
    
    # Definición del mapa de parámetros requeridos
    PARAM_MAP = {
        "df": df_capping,
        # Argumentos  basados en el gráfico seleccionado
        "variable_continua": variable_seleccionada,
        "clase_objetivo": CLASE_OBJETIVO, #  variable objetivo
        "variables_a_plotear": [v for v in VAR_MULTIPLOT if v in df_capping.columns] # Variables para multi-boxplot
    }
    
    # Definición de la función y los argumentos necesarios según la selección
    plot_function = PLOT_OPTIONS[plot_selection]
    
 
    # Aquí es donde se define exactamente lo que necesita cada función
    argumentos_necesarios = {}
    
    try:
        if plot_selection in [
            "Histograma (Seaborn/KDE)", "Gráfico de Densidad (Seaborn)", "Dot Plot (Seaborn)", 
            "Gráfico de Violín/Swarmplot (Seaborn)", "Histograma Interactivo (Plotly)", 
            "Boxplot Interactivo (Plotly)"
        ]:
            # Argumentos: df, variable_continua, clase_objetivo
            argumentos_necesarios = {
                'df': PARAM_MAP['df'], 
                'variable_continua': PARAM_MAP['variable_continua'], 
                'clase_objetivo': PARAM_MAP['clase_objetivo']
            }
        elif plot_selection == "Boxplots Múltiples (Seaborn)":
            # Argumentos: df, variables_a_plotear, clase_objetivo
            argumentos_necesarios = {
                'df': PARAM_MAP['df'], 
                'variables_a_plotear': PARAM_MAP['variables_a_plotear'], 
                'clase_objetivo': PARAM_MAP['clase_objetivo']
            }
        elif plot_selection == "Gráfico de Líneas (Seaborn)":
            # Argumentos: df, variable_continua
            argumentos_necesarios = {
                'df': PARAM_MAP['df'], 
                'variable_continua': PARAM_MAP['variable_continua']
            }
        elif plot_selection == "Heatmap de Correlación (Seaborn)":
            # Argumentos: df
            argumentos_necesarios = {
                'df': PARAM_MAP['df']
            }
        elif plot_selection == "Barras de Frecuencia (Seaborn)":
            # Argumentos: df, variable_discreta (usando CLASE_OBJETIVO como variable discreta)
            argumentos_necesarios = {
                'df': PARAM_MAP['df'], 
                # La función en barras.py espera 'variable_discreta', usamos el valor de CLASE_OBJETIVO
                'variable_discreta': CLASE_OBJETIVO 
            }
        
        # Llamada dinámica a la función
        fig = plot_function(**argumentos_necesarios)
        
        #Mostrar el resultado
        if plot_selection.endswith("(Plotly)"):
            st.plotly_chart(fig, use_container_width=True) # Para Plotly
            st.success("Gráfica Interactiva lista.")
        else:
            st.pyplot(fig, use_container_width=True) # Para Matplotlib/Seaborn
            st.info("Gráfica Estática lista.")

    except Exception as e:
        st.error(f"Ocurrió un error al generar la gráfica: {e}")
        st.warning("Revisa los parámetros  o la compatibilidad de la variable seleccionada con el tipo de gráfico.")


if __name__ == "__main__":
    main()