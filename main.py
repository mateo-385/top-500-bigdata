import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título del dashboard
st.title('Top 5000 mejores películas según IMDB 🍿')

# Leer CSV
df = pd.read_csv('top_peliculas_imdb.csv')

# Mostrar los datos
st.write(df)

# Gráfico simple
genre_counts = df['generos'].str.split(', ').explode().value_counts()
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(genre_counts.index, genre_counts.values, color='skyblue')
ax.set_title('Cantidad de películas por género en el top 500 de IMDB', fontsize=16)
ax.set_xlabel('Género', fontsize=12)
ax.set_ylabel('Cantidad de películas', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig)