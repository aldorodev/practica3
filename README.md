

#  Documentación de la Práctica 3

Aldo Alberto Rodríguez Flores

Este documento presenta la arquitectura y la implementación del proyecto Práctica 3: Desarrollo de Módulo `ctg_viz` para Análisis Exploratorio y Validación de Datos aplicado al *dataset* de Monitoreo Fetal Cardiotocográfico (`CTG.csv`) y documentando todo en un repositorio profesional (GitHub) y un PDF explicativo. 

---



 La librería `ctg_viz`cuenta con diferentes módulos:

* **Módulo `preprocessing.py`:** Contiene la lógica de limpieza y tratamiento de dispersión.
    * `eliminar_columnas_con_nulos(df, umbral)`: Descarta columnas si más del **20%** de sus registros son nulos.
    * `imputar_valores(df, metodo_num)`: Rellena los nulos restantes usando **Mediana / Media** para numéricos y **Moda** para categóricos.
    * `detectar_outliers_iqr()`: Identifica valores atípicos mediante el criterio $\mathbf{1.5 \times IQR}$.
    * `capping()`: Aplica la corrección forzada de *outliers* al limitarlos a los umbrales calculados.
* **Módulo `categorization.py`:** Contiene la función de auditoría final y clasificación.
    * `check_data_completeness_AldoAlbertoRodriguezFlores(df)`: Genera el reporte final de calidad.
* **Módulo `plots/`:** Contiene funciones para la generación de visualizaciones avanzadas.
    * `crear_histograma_con_densidad()`: Incluye **KDE (Kernel Density Estimation)** segmentado por grupo.
    * `crear_multi_boxplots()`: Genera **subgráficos** por la clase objetivo para análisis comparativo de la dispersión.
    * `crear_heatmap_correlacion()`: Muestra matriz de **correlación** con anotaciones y selección de método.

---

### Conclusiones 



* **Integridad Verificada:** El *dataset* demostró una integridad inicial excelente. La función `eliminar_columnas_con_nulos` confirmó que ninguna variable superó el umbral de 20% de nulos, y la `imputar_valores` solo manejó un número trivial de valores faltantes, resultando en un 100% de completitud en el reporte final.
* **Corrección de Dispersión:** El principal desafío fue la extrema dispersión estadística. Variables cruciales como la Variabilidad de Largo Plazo (`ALTV`) presentaron un porcentaje significativo de *outliers*. La aplicación rigurosa de la función `capping()` fue crítica, logrando que el reporte de `check_data_completeness...` posterior al tratamiento confirmara que el `Porctentaje Outliers` es cero** para las variables Continuas, indicando la estabilidad estadística del conjunto de datos. 
* **Clasificación de Variables:** La clasificación automática diferenció correctamente las variables: las métricas fisiológicas de gran rango son Continuas, mientras que los contadores de eventos (`AC`, `DL`, `DS`) son Discretas y se tratarán como categóricas en el análisis de modelado.

### Archivos

**code.py** es el archivo principal que ejecuta las funciones *python3 code.py*

Se implementó **Streamlit** para poderlo ejecutar  *streamlit run app.py*

Para ejecutar los test se debe ejecutar *pytest*


---

### 📦 Código de `requirements.txt`

Para reproducir este entorno de análisis, se requieren las siguientes dependencias de Python:

```text
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.8.0
seaborn>=0.13.0
streamlit>=1.0.0
plotly>=5.0.0