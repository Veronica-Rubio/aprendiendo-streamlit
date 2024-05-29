import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
@st.cache
def cargar_datos():
    data = pd.read_csv('IMDB-Movie-Data')
    return data

data = cargar_datos()

# Título de la aplicación
st.title('Aplicación de Búsqueda de Películas')

# Crear sidebar para búsqueda
st.sidebar.header('Parámetros de Búsqueda')
titulo = st.sidebar.text_input('Título de la Película')
director = st.sidebar.text_input('Director')
genero = st.sidebar.text_input('Género')
año_inicio = st.sidebar.number_input('Año de Inicio', min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), step=1, format="%i")
año_fin = st.sidebar.number_input('Año de Fin', min_value=int(data['Year'].min()), max_value=int(data['Year'].max()), step=1, format="%i")
grafico_tipo = st.sidebar.selectbox('Tipo de Gráfico', ['Rating', 'Ingresos'])

# Botón de búsqueda
if st.sidebar.button('Buscar'):
    # Filtrar datos
    resultados = data[(data['Title'].str.contains(titulo, case=False, na=False)) &
                      (data['Director'].str.contains(director, case=False, na=False)) &
                      (data['Genre'].str.contains(genero, case=False, na=False)) &
                      (data['Year'] >= año_inicio) & (data['Year'] <= año_fin)]

    # Mostrar resultados
    if resultados.empty:
        st.write('No se encontraron películas que coincidan con los criterios de búsqueda.')
    else:
        st.write(f'Se encontraron {len(resultados)} películas:')
        st.dataframe(resultados)

        # Gráfico según el tipo seleccionado
        if grafico_tipo == 'Rating':
            plt.figure(figsize=(10, 5))
            plt.hist(resultados['Rating'], bins=20, color='blue', alpha=0.7)
            plt.title('Distribución de Ratings')
            plt.xlabel('Rating')
            plt.ylabel('Frecuencia')
            st.pyplot(plt)
        elif grafico_tipo == 'Ingresos':
            plt.figure(figsize=(10, 5))
            plt.hist(resultados['Revenue (Millions)'].dropna(), bins=20, color='green', alpha=0.7)
            plt.title('Distribución de Ingresos')
            plt.xlabel('Ingresos (Millones de dólares)')
            plt.ylabel('Frecuencia')
            st.pyplot(plt)

# Ejecutar la aplicación: streamlit run nombre_de_tu_archivo.py
