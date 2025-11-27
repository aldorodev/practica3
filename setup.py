from setuptools import setup, find_packages

setup(
    name='ctg-viz',
    version='0.1.0',
    description='Librería de visualización para el análisis de Cardiotocografía (CTG).',
    long_description='Conjunto de funciones para generar visualizaciones estáticas e interactivas del dataset CTG, compatibles con Streamlit.',
    author='Aldo Rodriguez',
    packages=find_packages(), 
    install_requires=[
        'pandas',
        'matplotlib',
        'seaborn',
        'plotly',
        'streamlit', 
        'numpy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)