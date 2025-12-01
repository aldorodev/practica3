import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from .preprocessing import detectar_outliers_iqr
from . import utils 

def check_data_completeness_AldoAlbertoRodriguezFlores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un DataFrame de resumen de calidad de datos, incluyendo:
    - Conteo de Nulos y Porc de Completitud.
    - Tipo de Dato y Clasificación (Continua, Discreta, Categórica de Alta Cardinalidad).
    - Tipo General (Numérica o Categórica según utils.py).
    - Estadísticos de Dispersión (IQR, límites y conteo/Porc de Outliers para columnas Continuas).
    
    Args:
        df: DataFrame de entrada (se espera que sea el df_capping para el reporte final).

    Returns:
        pd.DataFrame: DataFrame resumen.
    """
    
    resumen_dic: Dict[str, Dict[str, Any]] = {}
    
    #Obtenemos las listas de columnas usando utils.py
    col_numericas = utils.columnas_numericas(df)
    col_categoricas = utils.columnas_categoricas(df)
    
    for col in df.columns:
        num_nulos = df[col].isnull().sum()
        num_filas = len(df)
        porcen_nulos = (num_nulos / num_filas) * 100
        porcen_completo = 100 - porcen_nulos
        dtype_str = str(df[col].dtype)
        num_unicos = df[col].nunique()
        
        # --- Clasificación usando las listas de utils.py 
        if col in col_numericas:
            tipo_general = "Numérica" 
            if num_unicos > 10:
                clasificacion = "Continua"
            else:
                clasificacion = "Discreta" 
        elif col in col_categoricas:
            tipo_general = "Categórica" 
            if num_unicos > 10:
                clasificacion = "Categórica" 
            else:
                 clasificacion = "Discreta"
        else:
            tipo_general = "Otro" 
            if num_unicos <= 10:
                clasificacion = "Discreta"
            else:
                clasificacion = "Otro (Alta Cardinalidad)" 
            
        resumen_dic[col] = {
            "Conteo Nulos": int(num_nulos),
            "Porc de Completitud": float(porcen_completo),
            "Tipo de Dato": dtype_str,
            "Tipo General": tipo_general, 
            "Clasificación": clasificacion, 
            "Valores Únicos": int(num_unicos), 
            
            # Inicializacion 
            "IQR": np.nan,
            "Lim Inf Outlier": np.nan,
            "Lim Sup Outlier": np.nan,
            "Conteo Outliers": np.nan,
            "Porctentaje Outliers": np.nan,
        }

    df_resumen = pd.DataFrame.from_dict(resumen_dic, orient='index')
    
    # Dispersión (IQR y Outliers) 
    col_continuas = df_resumen[df_resumen["Clasificación"] == "Continua"].index.tolist()
    
    if col_continuas:
        outlier_datos = detectar_outliers_iqr(df, columnas=col_continuas)

        for col, datos in outlier_datos.items():
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            df_resumen.loc[col, "IQR"] = float(IQR)
            df_resumen.loc[col, "Lim Inf Outlier"] = datos["lim_inferior"]
            df_resumen.loc[col, "Lim Sup Outlier"] = datos["lim_superior"]
            df_resumen.loc[col, "Conteo Outliers"] = datos["num_outliers"]
            df_resumen.loc[col, "Porctentaje Outliers"] = datos["porcentaje_outliers"]

    
    # Eliminar la columna auxiliar y ordenar las columnas para una mejor presentación
    df_resumen = df_resumen.drop(columns=["Valores Únicos"])
    
    # ORDEN DE COLUMNAS 
    col_orden = [
        "Conteo Nulos", "Porc de Completitud", "Tipo de Dato", "Tipo General", 
        "Clasificación", "IQR", "Lim Inf Outlier", "Lim Sup Outlier", 
        "Conteo Outliers", "Porctentaje Outliers"
    ]
    df_resumen = df_resumen[col_orden]
    
    pd.options.display.float_format = '{:,.2f}'.format
    
    return df_resumen.sort_values(by="Porctentaje Outliers", ascending=True)