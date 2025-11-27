import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from .preprocessing import detectar_outliers_iqr



def check_data_completeness_AldoAlbertoRodriguezFlores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera un DataFrame de resumen de calidad de datos, incluyendo:
    - Conteo de Nulos y Porc de Completitud.
    - Tipo de Dato y Clasificación (Continua, Discreta, Categórica de Alta Cardinalidad).
    - Estadísticos de Dispersión (IQR, límites y conteo/Porc de Outliers para columnas Continuas).
    
    NOTA: En el flujo principal de 'code.py', esta función se llama con el 
    DataFrame ya procesado (imputado y con capping aplicado), lo cual 
    asegura que los estadísticos de dispersión sean finales.

    Criterios de Clasificación:
    - Continua: Más de 10 valores únicos Y tipo numérico.
    - Discreta: Menos o igual a 10 valores únicos (cualquier tipo).
    - Categórica (Alto Cardinalidad): Más de 10 valores únicos Y NO numérico.

    Args:
        df: DataFrame de entrada (se espera que sea el df_capping para el reporte final).

    Returns:
        pd.DataFrame: DataFrame resumen.
    """
    
    resumen_dic: Dict[str, Dict[str, Any]] = {}
    
    for col in df.columns:
        num_nulos = df[col].isnull().sum()
        num_filas = len(df)
        porcen_nulos = (num_nulos / num_filas) * 100
        porcen_completo = 100 - porcen_nulos
        dtype_str = str(df[col].dtype)
        num_unicos = df[col].nunique()
        
        #  Clasificación
        if num_unicos > 10 and pd.api.types.is_numeric_dtype(df[col]):
            clasificacion = "Continua"
        elif num_unicos <= 10:
            clasificacion = "Discreta"
        else:
            clasificacion = "Categórica" 
            
        resumen_dic[col] = {
            "Conteo Nulos": int(num_nulos),
            "Porc de Completitud": float(porcen_completo),
            "Tipo de Dato": dtype_str,
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
    # Solo calculamos para conlumnas Continuas
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
    
    col_orden = [
        "Conteo Nulos", "Porc de Completitud", "Tipo de Dato", "Clasificación",
        "IQR", "Lim Inf Outlier", "Lim Sup Outlier", "Conteo Outliers", 
        "Porctentaje Outliers"
    ]
    df_resumen = df_resumen[col_orden]
    
    pd.options.display.float_format = '{:,.2f}'.format
    
    return df_resumen.sort_values(by="Porctentaje Outliers", ascending=True)

