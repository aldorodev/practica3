import pandas as pd
import numpy as np
import pytest
from ctg_viz.preprocessing import (
    eliminar_columnas_con_nulos,
    imputar_valores,
    verificar_unicos_outliers,
    detectar_outliers_iqr,
    # Se incluye capping solo si es necesario, pero los 4 tests principales no lo usan.
    # capping 
)



@pytest.fixture
def data_frame():
    """
    DataFrame de prueba para imputación y outliers (10 filas).
    """
    data_dic = {
        # imputar: 1 nulo (10%). Mediana = 6.0
        'col_low': [1, 2, np.nan, 4, 5, 6, 7, 8, 9, 10], 
        # imputar: Categórica, 1 nulo. Moda='dog'
        'col_cat': ['cat', 'dog', np.nan, 'cat', 'dog', 'dog', 'cat', 'dog', 'cat', 'dog'], 
        # outliers: 10 únicos (NO APTA), 1 outlier (1000). Q1=14.25, Q3=18.75, LimSup=25.5
        'col_outlier': [10, 12, 14, 15, 16, 17, 18, 19, 20, 1000], 
    }
    print(pd.DataFrame(data_dic).head())
    return pd.DataFrame(data_dic)

@pytest.fixture
def df_test():
    """
    DataFrame grande (500 filas) para el test de nulos.
    """
    num_filas = 500
    df_grande = pd.DataFrame({
        # 50 nulos (10%) -> Queda
        'col_queda': [1, 2, np.nan, 4, 5, 6, 7, 8, 9, 10] * (num_filas // 10), 
        # 200 nulos (40%) -> Se elimina con umbral 0.20
        'col_elimina': [10, 20, 30, np.nan, np.nan, np.nan, np.nan, 80, 90, 100] * (num_filas // 10), 
    })
    print(df_grande.head())

    return df_grande


# --------------------------------------------------------------------------------
#  Test eliminar_columnas_con_nulos
# --------------------------------------------------------------------------------
def test_nulos_eliminar_col(df_test):
    """
    Verifica que las columnas que superan el 20% de nulos sean eliminadas.
    """
    df_entrada = df_test
    # 500 filas, umbral (0.20) = 100 nulos. 'col_elimina' tiene 200 nulos (se elimina).
    df_salida = eliminar_columnas_con_nulos(df_entrada, umbral_porcentaje=0.20)
    
    
    assert 'col_elimina' not in df_salida.columns
    assert 'col_queda' in df_salida.columns
    assert len(df_salida.columns) == 1

# --------------------------------------------------------------------------------
# Test para imputar_valores
# --------------------------------------------------------------------------------
def test_imputar_mediana_moda(data_frame):
    """
    Verifica que los valores numéricos se imputen con la mediana (6.0) y 
    los categóricos con la moda ('dog').
    """
    df_entrada = data_frame
    
    df_res = imputar_valores(df_entrada, metodo_num="mediana")
    print("Imputación: \n")
    # Prueba numérica
    assert df_res['col_low'].isnull().sum() == 0
    assert df_res['col_low'].iloc[2] == 6.0 
    
    # Prueba categórica
    assert df_res['col_cat'].isnull().sum() == 0
    assert df_res['col_cat'].iloc[2] == 'dog'

# --------------------------------------------------------------------------------
# Test para verificar_unicos_outliers 
# --------------------------------------------------------------------------------
def test_verificar_unicos(data_frame):
    """
    Verifica la clasificación de columnas en APTAS (>= 10 únicos) y NO APTAS (< 10 únicos).
    """
    # Se asegura que ambas listas tengan la misma longitud (11)
    df_unico = pd.DataFrame({
        'col_noapta': [1, 2, 3, 4, 5] * 2 + [1], # Longitud 11. 5 únicos, NO APTA
        'col_apta': list(range(1, 12)),           # Longitud 11. 11 únicos, APTA
    })
    
    col_aptas = verificar_unicos_outliers(df_unico)
    print("Columnas aptas:", col_aptas)
    assert col_aptas == ['col_apta']
    assert 'col_noapta' not in col_aptas

# --------------------------------------------------------------------------------
#  Test detectar_outliers_iqr
# --------------------------------------------------------------------------------
def test_detectar_iqr_outlier(data_frame):
    """
    Verifica la detección correcta del número de outliers y el límite superior (IQR).
    El límite superior correcto para esta serie es 25.5.
    """
    df_entrada = data_frame
    # Columna 'col_outlier'. Límite Superior = 25.5
    
    resultados_iqr = detectar_outliers_iqr(df_entrada, columnas=['col_outlier'])
    print("Resultados IQR:", resultados_iqr)
    assert 'col_outlier' in resultados_iqr
    assert resultados_iqr['col_outlier']['num_outliers'] == 1
    # Se corrige la aserción al valor correcto (25.5)
    assert resultados_iqr['col_outlier']['lim_superior'] == 25.5