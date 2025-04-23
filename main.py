import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Título del dashboard
st.title('Top 5000 mejores películas según IMDB 🍿')

# Función para cargar datos
@st.cache_data
def cargar_datos(filepath):
    return pd.read_csv(filepath)

# Función para mostrar datos
def mostrar_datos(df):
    df.set_index('puesto', inplace=True)
    st.write(df)


# Función para generar gráfico de barras interactivo
def grafico_barras(df):
    genre_counts = df['generos'].str.split(', ').explode().value_counts()
    fig = px.bar(
        x=genre_counts.index,
        y=genre_counts.values,
        labels={'x': 'Género', 'y': 'Cantidad de películas'},
        title='Cantidad de películas por género en el top 500 de IMDB',
        
    )
    fig.update_traces(textposition='outside', marker_color='skyblue')
    fig.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig)


# Función para generar histograma interactivo con tendencia
def grafico_histograma(df):
    df['decada'] = (df['año'] // 10) * 10
    all_decades = list(range((df['año'].min() // 10) * 10, ((df['año'].max() // 10) + 2) * 10, 10))

    # Datos para el histograma
    counts = df['decada'].value_counts().reindex(all_decades[:-1], fill_value=0)

    # Datos para la línea de tendencia
    votes_per_decade = df.groupby('decada')['votos'].sum().reindex(all_decades[:-1], fill_value=0)

    # Crear figura
    fig = go.Figure()

    # Añadir histograma
    fig.add_trace(go.Bar(
        x=all_decades[:-1],
        y=counts.values,
        name='Cantidad de películas',
        marker_color='skyblue',
        hovertemplate='Década: %{x}<br>Cantidad: %{y}<extra></extra>'
    ))

    # Línea de tendencia (votos totales)
    fig.add_trace(go.Scatter(
        x=all_decades,
        y=list(votes_per_decade),
        mode='lines+markers',
        name='Votos Totales',
        line=dict(color='green'),
        yaxis='y2',  # ← esta línea es clave
        hovertemplate='Década: %{x}<br>Votos: %{y}<extra></extra>'
    ))

    # Configurar diseño
    fig.update_layout(
        title='Distribución de películas y votos por década',
        xaxis_title='Década',
        yaxis_title='Cantidad de películas',
        yaxis2=dict(title='Total de votos', overlaying='y', side='right'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        xaxis=dict(tickangle=45)
    )

    st.plotly_chart(fig)

## Función para generar boxplot interactivo
def grafico_boxplot(df):
    genres_exploded = df.assign(generos=df['generos'].str.split(', ')).explode('generos')

    # Crear figura
    fig = px.box(
        genres_exploded,
        x='generos',
        y='puntuacion',
        color='generos',
        title='Distribución de puntuaciones por género',
        labels={'generos': 'Género', 'puntuacion': 'Puntuación'},
        template='plotly_white'
    )

    # Configurar diseño
    fig.update_layout(
        xaxis_title='Género',
        yaxis_title='Puntuación',
        xaxis=dict(tickangle=45),
        showlegend=False
    )

    st.plotly_chart(fig)

# Cargar datos
df = cargar_datos('top_peliculas_imdb.csv')

# Mostrar datos
mostrar_datos(df)

# Generar gráficos
grafico_barras(df)
grafico_histograma(df)
grafico_boxplot(df)