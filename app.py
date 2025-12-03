import streamlit as st
import pandas as pd

# Cargar tu base de datos
base_datos = pd.read_excel("peliculasfin.xlsx")

st.title("Califica todas las películas")

for idx, row in base_datos.iterrows():
    pelicula = row["Nombre"] 

    st.subheader(pelicula)

    seleccion = st.feedback("thumbs")

    if seleccion is not None:
        if seleccion == 0:
            st.write("No me gustó 👎")
        else:
            st.write("Me gustó 👍")

    st.write("---")
