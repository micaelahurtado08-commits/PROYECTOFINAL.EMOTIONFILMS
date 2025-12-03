import streamlit as st
import pandas as pd
import folium
import openpyxl
from streamlit.components.v1 import html

# Cargar base de datos (debe estar en la misma carpeta)
base_datos = pd.read_excel("peliculas_mapa.xlsx")
#st.dataframe(base_datos)


# Cargamos nuestra base de datos desde un archivo Excel previamente trabajado
df = pd.read_excel('peliculasfin.xlsx')

# -------------------- MENÚ DE PÁGINAS --------------------
# Definimos las dos secciones principales de la página: presentación y encuesta
# Dividir la página
lista_secciones = ["Inicio", "Películas", "Juegos", "Mapa"]
pagina_seleccionada = st.sidebar.selectbox("Selecciona una sección", lista_secciones)

# -------------------- PÁGINA DE PRESENTACIÓN --------------------

    # Configuramos la barra lateral con la imagen de perfil y el título
    # col1, col2 = st.columns(2): Esta línea está creando dos columnas en la interfaz de usuario de la aplicación web. 
    # La función st.columns toma un número entero como argumento que especifica el número de columnas que se deben crear. 
    # Las columnas creadas se asignan a las variables col1 y col2.


if pagina_seleccionada == "Inicio":

    # ---------- TÍTULO PRINCIPAL ----------
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>🎬 EMOTIONFILMS 🎬</h1>", unsafe_allow_html=True)

    # ---------- TEXTO DE PRESENTACIÓN ----------
    texto = (
        "¡Hola! Somos Micaela Hurtado, Valeria Esteban e Ivan Gonzales. Queremos darte la bienvenida a Emotionfilms, "
        "nuestra página web interactiva creada como parte del proyecto final del curso de Pensamiento Computacional "
        "para Comunicadores en la Facultad de Ciencias y Artes de la Comunicación."
    )

    st.markdown(
        f"<div style='text-align: justify; font-size: 15px;'>{texto}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h2 style='font-size: 35px; margin-top: 40px;'>¿Qué es Emotionfilms? 🤔</h2>",
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        respuesta = (
            "Emotionfilms está pensada para que no solo veas películas… sino que las sientas. Con una interfaz amigable y pensada para ti, podrás descubrir recomendaciones personalizadas que se ajustan a tus emociones del momento. Cada película viene acompañada de una ficha técnica completa: sinopsis, año de estreno, plataforma donde verla, tráiler y portada. ¿Poco tiempo? ¿Mucho tiempo? No importa. Puedes filtrar por duración y encontrar justo lo que te acomoda. Y para hacerlo aún más entretenido, añadimos un juego del ahorcado temático de películas, perfecto para descubrir nuevos títulos mientras te diviertes. En Emotionfilms, ¡tu emoción elige la película!"
        )

        st.markdown(
            f"<div style='text-align: justify; font-size: 15px;'>{respuesta}</div>",
            unsafe_allow_html=True
        )

    with col2:
        st.image("imagen1.jpg", use_container_width=True)  

    st.markdown(
        "<h2 style='font-size: 35px; margin-top: 40px;'>¿Por qué creamos Emotionfilms? 🎥</h2>",
        unsafe_allow_html=True
    )

    col3, col4 = st.columns([2, 1])

    with col3:
        tercer_texto = (
            "Sabemos que elegir una buena película puede volverse un caos: demasiadas opciones, demasiadas dudas y cero ganas de perder tiempo. Por eso, en nuestro proyecto queremos hacer que ese momento sea más fácil, más rápido y mucho más divertido. Emotionfilms te ofrece recomendaciones personalizadas que se adaptan a cómo te sientes en el instante, para que siempre encuentres la peli perfecta. Explora, juega y déjate sorprender. ¡Con Emotionfilms, descubrir nuevas películas nunca fue tan emocionante!"
        )

        st.markdown(
            f"<div style='text-align: justify; font-size: 15px;'>{tercer_texto}</div>",
            unsafe_allow_html=True
        )

    with col4:
        st.image("imagen3.jpeg", use_container_width=True)  

# -------------------- PÁGINA DE PELÍCULAS --------------------
elif pagina_seleccionada == "Películas":
    # Título de la página
    st.title("¿Qué quieres ver hoy?🍿")

    # Cargar base de datos
    df = pd.read_excel("peliculasfin.xlsx")

    # Crear columna Intervalo si no existe 
    if "Intervalo Duración" not in df.columns:
        df["Duración"] = df["Duración"].astype(str).str.extract(r"(\d+)").astype(float)

        def asignar_intervalo(minutos):
            if minutos < 90:
                return "Corta (<90 min)"
            elif 90 <= minutos <= 120:
                return "Media (90-120 min)"
            else:
                return "Larga (>120 min)"

        df["Intervalo Duración"] = df["Duración"].apply(asignar_intervalo)

    # ---------------------- FILTRO INICIAL ----------------------
    filtro = pd.Series([True] * len(df))

    # ---------------------- FILTRO EMOCIÓN ----------------------
    emocion = st.selectbox(
        "¿Qué emoción buscas?",
        ["Todas"] + sorted(df["Emociones"].dropna().unique().tolist())
    )
    if emocion != "Todas":
        filtro &= df["Emociones"] == emocion

    # ---------------------- FILTRO INTERVALO ----------------------
    intervalo = st.selectbox(
        "Duración",
        ["Todas"] + sorted(df["Intervalo Duración"].dropna().unique().tolist())
    )
    if intervalo != "Todas":
        filtro &= df["Intervalo Duración"] == intervalo

    # --- APLICAR FILTRO ---
    df_filtrado = df[filtro]

    # Mostrar resultados
    if df_filtrado.empty:
        st.warning("No se encontraron películas con esos filtros 😢")
    else:
        cols = st.columns(2) # Dividir en dos columnas
        col_idx = 0

        for idx, row in df_filtrado.iterrows():
            with cols[col_idx]:
                st.write("---")

                col_img, col_info = st.columns([1, 3])

                # Portada
                with col_img:
                    if pd.notna(row["Cover"]) and str(row["Cover"]).strip() != "":
                        st.image(row["Cover"], width=150)
                    else:
                        st.write("Sin imagen")

                # Info
                with col_info:
                    st.markdown(f"{row['Nombre']}")
                    st.write(f"**Año:** {row['Año']} • **Duración:** {row['Duración']}")
                    st.write(f"**Plataforma:** {row['Plataforma']}")
                    st.write(f"**Género:** {row['Género']}")
                    st.write(row["Sinopsis"])

                    # Links
                    if pd.notna(row["Trailer"]):
                        st.markdown(f"[Ver tráiler]({row['Trailer']})")
            col_idx = (col_idx + 1) % 2
            
# -------------------- PÁGINA DE JUEGOS --------------------
elif pagina_seleccionada == "Juegos":
    import random

    def pagina_juegos(df):

       # Inicializar variables de sesión
        if "pelicula" not in st.session_state:
            titulo = random.choice(df["Nombre"])
    
            # Convertimos el título a mayúsculas
            st.session_state.pelicula = titulo.upper()

            # Convertimos letras con tilde para que coincidan con el input del usuario
            reemplazos = str.maketrans("ÁÉÍÓÚÑ", "AEIOUN")
            st.session_state.pelicula_normalizada = st.session_state.pelicula.translate(reemplazos)

            # Progreso con guiones, pero manteniendo espacios tal cual
            st.session_state.progreso = [
                "_" if letra.isalpha() else letra
                for letra in st.session_state.pelicula
            ]
            st.session_state.vidas = 6
            st.session_state.letras_intentadas = []


        st.subheader("🎮 Ahorcado de Películas")

        # Mostrar estado del juego
        st.write("Película:", " ".join(st.session_state.progreso))
        st.write(f"Vidas restantes: ❤️ {st.session_state.vidas}")
        st.write("Letras usadas:", ", ".join(st.session_state.letras_intentadas))

        # Input del usuario
        intento = st.text_input("Ingresa una letra:", max_chars=1).upper()

        if st.button("Probar letra") and intento:
            if not intento.isalpha():
                st.warning("Ingresa SOLO una letra.")
            elif intento in st.session_state.letras_intentadas:
                st.warning("⚠ Ya intentaste esa letra.")
            else:
                st.session_state.letras_intentadas.append(intento)

                if intento in st.session_state.pelicula_normalizada:
                    st.success("¡Correcto!")
                    for i, letra in enumerate(st.session_state.pelicula_normalizada):
                        if letra == intento:
                            st.session_state.progreso[i] = st.session_state.pelicula[i]
                else:
                    st.error("Incorrecto ❌")
                    st.session_state.vidas -= 1


        # Resultado final
        if "_" not in st.session_state.progreso:
            st.success(f"🎉 ¡GANASTE! La película era: {st.session_state.pelicula}")

            if st.button("Jugar otra vez"):
                for key in ["pelicula", "progreso", "vidas", "letras_intentadas"]:
                    del st.session_state[key]
                st.rerun()

        elif st.session_state.vidas <= 0:
            st.error(f"💀 Te quedaste sin vidas. La película era: {st.session_state.pelicula}")

            if st.button("Intentar de nuevo"):
                for key in ["pelicula", "progreso", "vidas", "letras_intentadas"]:
                    del st.session_state[key]
                st.rerun()

    # EJECUTAR FUNCIÓN
    pagina_juegos(df) 

# -------------------- PÁGINA DE MAPA --------------------

else: 
    titulo = "¿SABES DÓNDE SE HICIERON LAS PELÍCULAS? ENTÉRATE ACÁ 🌍"
    st.markdown(f"<h1 style='text-align: center; font-size: 40px;'>{titulo}</h1>", unsafe_allow_html=True)

    mapa = folium.Map(location=[20,0], zoom_start=2)

    for _, row in base_datos.iterrows():
        popup_html = (
            f"<div style='font-size:16px;'>"
            f"<b style='font-size:20px;'>{row['Película']}</b><br>"
            f"<span style='font-size:17px;'>Producción: {row['Producción']}</span><br>"
            f"<img src='{row['Cover']}' width='200' style='border-radius: 10px; margin-top: 10px;'><br>"
            f"<span style='font-size:15px;'>Latitud: {row['Latitud']}</span><br>"
            f"<span style='font-size:15px;'>Longitud: {row['Longitud']}</span>"
            f"</div>"
        )
        popup = folium.Popup(popup_html, max_width=300)
        folium.Marker(
            location=[row["Latitud"], row["Longitud"]],
            popup=popup,
            icon=folium.Icon(color='red')
        ).add_to(mapa)

    # Mostrar mapa 
    map_html = mapa._repr_html_()
    # Mostrar en Streamlit
    html(map_html, height=500)


