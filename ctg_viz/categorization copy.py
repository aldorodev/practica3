from typing import Dict, Any
import pandas as pd
import numpy as np


def check_data_completeness_AldoAlbertoRodriguezFlores(df: pd.DataFrame) -> pd.DataFrame:
    """Genera un reporte por columna con:
       - conteo de nulos
       - % de completitud
       - tipo de dato
       - estadísticas de dispersión (para numéricas)
       - clasificación: 'continuo' o 'discreto' o 'categorico'

    Args:
        df: DataFrame.

    Returns:
        DataFrame resumen indexado por columna.
    """
    filas = []
    n = len(df)
    for col in df.columns:
        nulos = int(df[col].isnull().sum())
        completitud = 100.0 * (1 - nulos / n) if n > 0 else 0.0
        tipo = str(df[col].dtype)

        resumen = {
            "columna": col,
            "nulos": nulos,
            "pct_completitud": round(completitud, 2),
            "tipo": tipo
        }

        if pd.api.types.is_numeric_dtype(df[col]):
            serie = df[col].dropna()
            resumen.update({
                "min": float(serie.min()) if not serie.empty else np.nan,
                "q1": float(serie.quantile(0.25)) if not serie.empty else np.nan,
                "mediana": float(serie.median()) if not serie.empty else np.nan,
                "q3": float(serie.quantile(0.75)) if not serie.empty else np.nan,
                "max": float(serie.max()) if not serie.empty else np.nan,
                "mean": float(serie.mean()) if not serie.empty else np.nan,
                "std": float(serie.std()) if not serie.empty else np.nan,
            })
            nunicos = int(serie.nunique())
            if nunicos > 10:
                clas = "continuo"
            else:
                clas = "discreto"
            resumen["clasificacion"] = clas
            resumen["num_unicos"] = nunicos
        else:
            # categóricos
            nunicos = int(df[col].nunique(dropna=True))
            resumen.update({
                "num_unicos": nunicos,
                "clasificacion": "categorico"
            })

        filas.append(resumen)

    df_reporte = pd.DataFrame(filas).set_index("columna")
    return df_reporte
