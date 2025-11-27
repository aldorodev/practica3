
import pandas as pd
import numpy as np
from typing import Iterable, List, Dict, Tuple



def eliminar_columnas_con_nulos(df: pd.DataFrame, umbral_porcentaje: float = 0.20) -> pd.DataFrame:
    """Elimina columnas que superen un umbral de 20%  valores nulos.

    Args:
        df: DataFrame original.
        umbral_porcentaje: Umbral del 20% para eliminar columnas.

    Returns:
        DataFrame sin las columnas que superen el umbral.
    """
    if not 0 <= umbral_porcentaje <= 1:
        raise ValueError("umbral_porcentaje debe estar entre 0 y 1")
    num_filas = len(df)
    umbral = int(np.floor(umbral_porcentaje * num_filas))
    total_nulos = df.isnull().sum()
    col_eliminar = total_nulos[total_nulos > umbral].index.tolist()
    df_resultado = df.drop(columns=col_eliminar) if col_eliminar else df.copy()
    print(f"Columnas eliminadas (>{umbral_porcentaje*100:.1f}% nulos = {umbral} nulos): {len(col_eliminar)} columnas")
    return df_resultado


def imputar_valores(df: pd.DataFrame,
                    col_num: Iterable[str] = None,
                    col_cat: Iterable[str] = None,
                    metodo_num: str = "mediana") -> pd.DataFrame:
    """Imputa valores faltantes:
       - numéricos: mediana o media
       - categóricos: moda

    Args:
        df: DataFrame con valores faltantes.
        col_num: lista de columnas numéricas (si None se detectan automáticamente).
        col_cat: lista de columnas categóricas (si None se detectan automáticamente).
        metodo_num: 'mediana' o 'media'.

    Returns:
        DataFrame con valores imputados.
    """
    
    df_res = df.copy()
    total_cambios_num = 0
    total_cambios_cat = 0


    if col_num is None:
        col_num = df_res.select_dtypes(include=np.number).columns.tolist()
    if col_cat is None:
        col_cat = df_res.select_dtypes(include=['object', 'category']).columns.tolist()

    for col in col_num:
        cambios_col = df_res[col].isnull().sum()
        if metodo_num == "mediana":
            valor = df_res[col].median()
        elif metodo_num == "media":
            valor = df_res[col].mean()
        else:
            valor = df_res[col].median()
            
        df_res[col] = df_res[col].fillna(valor)
        print(f" Columna '{col}' (Numérica): {cambios_col} valores imputados, valor ({valor:.2f}). ")
    

    for col in col_cat:
        cambios_col = df_res[col].isnull().sum()
        if df_res[col].isnull().any():
            moda = df_res[col].mode()
            if moda.empty:
                valor = ""
            else:
                valor = moda[0]
            df_res[col] = df_res[col].fillna(valor)
        
        print(f" Columna '{col}' (Categórica): {cambios_col} valores imputado, valor ({valor}).")
    return df_res


def verificar_unicos_outliers(df: pd.DataFrame) -> List[str]:
    """
    Verifica el número de valores únicos en las columnas numéricas.
    Imprime la clasificación y **devuelve la lista de columnas aptas** (>= 10 valores únicos) 
    para el análisis de outliers tradicional.

    Args:
        df (pd.DataFrame): El DataFrame a analizar.

    Returns:
        List[str]: Una lista con los nombres de las columnas que tienen 10 o más valores únicos.
    """
    col_num = df.select_dtypes(include=np.number).columns

    col_aptas = []
    col_no_aptas = []

    for col in col_num:
        unique_count = df[col].nunique()

        if unique_count <= 10:
            print(f"**NO APTA** - {col}: {unique_count} valores únicos (Posiblemente variable categórica/ordinal)")
            col_no_aptas.append(col)
        else:
            print(f"**APTA**    - {col}: {unique_count} valores únicos (Adecuada para análisis de outliers)")
            col_aptas.append(col)
    
    print(f"Columnas Aptas para Outliers ({len(col_aptas)}): {col_aptas}")
    print(f"Columnas No Aptas ({len(col_no_aptas)}): {col_no_aptas}")

    return col_aptas


def detectar_outliers_iqr(df: pd.DataFrame, 
                          columnas: Iterable[str] = None
                         ) -> Dict[str, Dict[str, float]]:
    """Detecta outliers por IQR para columnas numéricas seleccionadas.

    Args:
        df: DataFrame.
        columnas: columnas a evaluar (si es None se usan las numéricas).

    Returns:
        Diccionario por columna con keys: 'num_outliers', 'porcentaje_outliers', 'lim_inferior', 'lim_superior'.
    """
    
    if columnas is None:
        columnas = df.select_dtypes(include=np.number).columns.tolist()
    columnas_a_procesar = [col for col in columnas if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]

    resultado = {}
    n = len(df)
    
    if n == 0:
        return resultado
        
    for col in columnas_a_procesar:
        serie = df[col].dropna() 
        
        #if len(serie) < 4: 
        #    continue
            
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        
        if IQR == 0:
            continue
            
        lim_inf = Q1 - 1.5 * IQR
        lim_sup = Q3 + 1.5 * IQR
        
        num_outliers = int(((serie < lim_inf) | (serie > lim_sup)).sum())
        porcentaje_outliers =  (num_outliers / n) * 100
        
        resultado[col] = {
            "num_outliers": int(num_outliers),
            "porcentaje_outliers": float(porcentaje_outliers),
            "lim_inferior": float(lim_inf),
            "lim_superior": float(lim_sup)
        }

   
        
    return resultado



def capping(df: pd.DataFrame, columnas: Iterable[str] = None) -> pd.DataFrame:
    """
    Aplica el 'capping' (limitación) a los valores atípicos (outliers) 
    en las columnas numéricas especificadas usando el método 1.5 * IQR.
    Si 'columnas' es None, procesa todas las columnas numéricas.
    """
    
    df_capping = df.copy()


    
    if columnas is None:
        cols_to_process: List[str] = df_capping.select_dtypes(include=np.number).columns.tolist()
    else:
        cols_to_process = list(columnas) 

    for col in cols_to_process:
        if col not in df_capping.columns or not np.issubdtype(df_capping[col].dtype, np.number):
            if col in df_capping.columns:
                print(f"Columna '{col}' no es numérica. Omitiendo.")
            continue
            
        Q1 = df_capping[col].quantile(0.25)
        Q3 = df_capping[col].quantile(0.75)
        IQR = Q3 - Q1
        
        lim_inferior = Q1 - 1.5 * IQR
        lim_superior = Q3 + 1.5 * IQR
        
        outliers_bajos = (df_capping[col] < lim_inferior).sum()
        outliers_altos = (df_capping[col] > lim_superior).sum()
        
        if outliers_bajos > 0 or outliers_altos > 0:
            df_capping[col] = df_capping[col].clip(lower=lim_inferior, upper=lim_superior)
            print(f"Columna '{col}': {outliers_bajos} bajos, valor {lim_inferior:.2f} | {outliers_altos} altos, valor {lim_superior:.2f}")

    return df_capping