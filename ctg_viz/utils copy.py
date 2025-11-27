from typing import List
import pandas as pd
import numpy as np


def columnas_numericas(df: pd.DataFrame) -> List[str]:
    """Retorna lista de columnas numéricas."""
    return df.select_dtypes(include=np.number).columns.tolist()


def columnas_categoricas(df: pd.DataFrame) -> List[str]:
    """Retorna lista de columnas categóricas."""
    return df.select_dtypes(include=['object', 'category']).columns.tolist()
