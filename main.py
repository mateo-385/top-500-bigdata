import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# Título del dashboard
st.title('Top 5000 mejores películas según IMDB 🍿')

# Función para cargar datos
@st.cache_data
def cargar_datos(filepath):
    return pd.read_csv(filepath)

# Función para mostrar datos
def mostrar_datos(df):
    st.write(df)

# Función para generar gráfico de barras
def grafico_barras(df):
    genre_counts = df['generos'].str.split(', ').explode().value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(genre_counts.index, genre_counts.values, color='skyblue')
    ax.set_title('Cantidad de películas por género en el top 500 de IMDB', fontsize=16)
    ax.set_xlabel('Género', fontsize=12)
    ax.set_ylabel('Cantidad de películas', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

# Función para generar histograma con tendencia
def grafico_histograma(df):
    fig, ax1 = plt.subplots(figsize=(10, 6))

    df['decada'] = (df['año'] // 10) * 10

    all_decades = list(range((df['año'].min() // 10) * 10, ((df['año'].max() // 10) + 2) * 10, 10))

    counts, bins, patches = ax1.hist(df['año'], bins=all_decades, color='skyblue', edgecolor='black', align='left')

    ax1.set_title('Distribución de películas y votos por década', fontsize=16)
    ax1.set_xlabel('Década', fontsize=12)
    ax1.set_ylabel('Cantidad de películas', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    plt.xticks(all_decades[:-1], rotation=45)


    votes_per_decade = df.groupby('decada')['votos'].sum().reindex(all_decades[:-1], fill_value=0)
    ax2 = ax1.twinx()
    
    def millions(x, pos):
        return f'{int(x/1e6)}M'

    ax2.yaxis.set_major_formatter(ticker.FuncFormatter(millions))
    ax2.plot(votes_per_decade.index, votes_per_decade.values, color='green', marker='o', linestyle='-', label='Votos Totales')
    ax2.set_ylabel('Total de votos', fontsize=12, color='green')
    ax2.tick_params(axis='y', labelcolor='green')

    ax2.legend(loc='upper left')

    plt.tight_layout()
    st.pyplot(fig)

# Función para generar boxplot de puntuaciones por género
def grafico_boxplot(df):
    genres_exploded = df.assign(generos=df['generos'].str.split(', ')).explode('generos')
    fig, ax = plt.subplots(figsize=(12, 6))
    genres_exploded.boxplot(column='puntuacion', by='generos', ax=ax, grid=False, patch_artist=True, boxprops=dict(facecolor='skyblue'))
    ax.set_title('Distribución de puntuaciones por género', fontsize=16)
    ax.set_xlabel('Género', fontsize=12)
    ax.set_ylabel('Puntuación', fontsize=12)
    plt.suptitle('')
    plt.xticks(rotation=45)
    ax.yaxis.grid(True, linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
    plt.tight_layout()
    st.pyplot(fig)

# Cargar datos
df = cargar_datos('top_peliculas_imdb.csv')

# Mostrar datos
mostrar_datos(df)

# Generar gráficos
grafico_barras(df)
grafico_histograma(df)
grafico_boxplot(df)