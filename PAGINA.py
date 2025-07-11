import streamlit as st

# Generamos 3 páginas en la aplicación web de Streamlit.
# Generamos una página principal, otra donde contaran su experiencia aprendiendo a programar y una tercera donde presentarán sus gráficos.

# Creamos la lista de páginas
paginas = ["♡ Conoce a Taylor", "♡ Explora canciones", "♡ Videoclips", "♡ Original vs Taylor's Version", "♡ Sección Lúdica"]

import random
import pandas as pd

# Botón musical en la barra lateral
df_discografia = pd.read_excel("base de datos.xlsx")

# Elige una cancion aleatoria 
cancion_aleatoria = random.choice(df_discografia["Link_spotify"].dropna().tolist())
# Mostramos el botón que lleva directamente al link
st.sidebar.markdown(f"<a href='{cancion_aleatoria}' target='_blank'><button>🎧 Escucha una canción aleatoria</button></a>", unsafe_allow_html=True)

# Creamos botones de navegación tomando la lista de páginas
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# Generamos condicionales para mostrar el contenido de cada página
if pagina_seleccionada == "♡ Conoce a Taylor":

    # La función st.markdown permite centrar y agrandar la letra del título de la web en Streamlit.
    st.markdown("<h1 style='text-align: center;'>ANATOMÍA DE UN ÍCONO: Exploración de la discografía de Taylor Swift </h1>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # col1, col2 = st.columns(2): Esta línea está creando dos columnas en la interfaz de usuario de la aplicación web. 
    # La función st.columns toma un número entero como argumento que especifica el número de columnas que se deben crear. 
    # Las columnas creadas se asignan a las variables col1 y col2.

    import streamlit as st
    import time

    # Función para hacer efecto máquina de escribir con el texto del archivo
    def stream_biografia():
        with open("biografia.txt", "r", encoding="utf-8") as archivo:
            texto = archivo.read()
        for palabra in texto.split(" "):
            yield palabra + " "
            time.sleep(0.02)

    # Título de la sección
    st.markdown("<h3><em>¿Quién es Taylor Swift?</em></h3>", unsafe_allow_html=True)

    # Botón para activar la biografía
    if st.button("Descúbrelo"):
        st.image("taylor6.jpg", caption="Taylor Swift", use_container_width=True)
        st.write_stream(stream_biografia)

    # PASAMOS A COLOCAR INFORMACION DE LOS ALBUMES
    import pandas as pd
    df_discografia = pd.read_excel("base de datos.xlsx")

    # Lista de álbumes (sin los singles)
    lista_albumes = list(df_discografia["Álbum"].unique()) 
    lista_albumes.remove("single")

    # Año de los albumes
    años_por_album = df_discografia.groupby("Álbum")["Año"].first()[0:15] # con .first() tomamos el primer valor al que se asocie Album en la columna de año. Luego, para deshacernos de los singles delimitamos del [0:15]

    # Cantidad de canciones por álbum
    canciones_por_album = df_discografia.groupby('Álbum')['titulo'].count()
    
    # Portadas de álbumes
    portadas_albumes = list(df_discografia["Link_portada"].unique()) #Sin embargo, contara también los links de las portadas de los singles
    portadas_albumes= portadas_albumes[0:15] #Delimitamos hasta donde estén las portadas de los albumes que es el indice 14, pero aqui colocamos 15 para que cuente el 14

    # Reproducciones por álbum
    reproducciones_por_albumes = df_discografia.groupby('Álbum')['Reproducciones en Spotify'].sum()

    # Para poder dar como info la duración aproximada necesitaremos transformar el tiempo que tenemos en formato mm:ss a segundos en general
    def duracion_a_segundos(duracion_str):
        minutos, segundos = map(int, duracion_str.split(':'))
        return minutos * 60 + segundos

    # Creamos nueva columna con la duración en segundos
    df_discografia["Duracion_segundos"] = df_discografia["Duración"].apply(duracion_a_segundos)

    # Agrupamos
    duracion_por_album_segundos = df_discografia.groupby("Álbum")["Duracion_segundos"].sum()
#________

    # Procedemos a la presentación de los albumes
    import streamlit as st
    st.title("📀 Discografía de Taylor Swift")

    for i in range(len(lista_albumes)): # Primero creamos un bucle que iterara según la cantidad de albumes de nuestra lista, para ello empleamos range(len()) que crea la lista automaticamente
        nombre_album = lista_albumes[i] # Luego para obtener el nombre del album, lo obtendremos de la lista de albumes y para que vaya tomando uno a uno de la lista, usamos la variable iteradora i, en la primera vuelta tomará 0, y extraerá el valor del indice 0 de la lista. Así con todos los elementos.
        año_album = años_por_album.loc[nombre_album]
        cantidad_canciones = canciones_por_album.loc[nombre_album] # Para sacar la cantidad de canciones, iremos al df canciones_por_album y con .loc ubicaremos según el valor de la varibale anterior, de esta manera ira cambiando en cada iteración.
        portada_album = portadas_albumes[i] # Para la portada, se empleará la logica de nombre_album, pero ahora en la lista portadas_albumes
        reproducciones_por_album = reproducciones_por_albumes.loc[nombre_album]

        with st.container():
            col1, col2 = st.columns([2, 1])  # más espacio al texto
            with col1:
                st.markdown(f"""
                <h4><i><b>{nombre_album}</b></i></h4>
                <ul>
                    <li><b>Año:</b> {año_album}</li>
                    <li>Canciones: {cantidad_canciones}</li>
                    <li>📈 Reproducciones aproximadas: {reproducciones_por_album:,}</li>
                </ul>
                """, unsafe_allow_html=True)
        with col2:
            st.image(portada_album, width=200)

elif  pagina_seleccionada == "♡ Explora canciones":
    
    # Agregamos un título
    st.markdown("<h1 style='text-align: center;'>BUSCADOR DE CANCIONES</h1>", unsafe_allow_html=True)

    import pandas as pd
    df_discografia = pd.read_excel("base de datos.xlsx")

    # Traemos de vuelta la columna de Duracion_segundos
    def duracion_a_segundos(duracion_str):
        minutos, segundos = map(int, duracion_str.split(':'))
        return minutos * 60 + segundos

    df_discografia["Duracion_segundos"] = df_discografia["Duración"].apply(duracion_a_segundos)


    # RECONOCES los valores unicos que existen en la columna de Genero, para armar las opciones desplegables
    generos_encontrados= []

    # Recorremos cada fila del DataFrame con un bucle for y .iterrows()
    for i, fila in df_discografia.iterrows():
        texto_genero = str(fila["Genero"])  # Obtenemos todo el contenido de la columna "Genero" como un texto y lo guardamos en la variable texto_genero
        lista_generos = texto_genero.split(",")  # Ahora ese texto lo separamos con .split(), separará cada que encuentre una coma, eso lo almacenamos en la varibale lista_generos

    # Ahora, para cada genero en la lista, quitamos espacios con .strip() y lo pasamos a minúscula con .lower()
        for genero in lista_generos:
            genero_depurado = genero.strip().lower()
            generos_encontrados.append(genero_depurado) # Luego, agregamos ese genero ya depurado a la lista que creamos al inicio: generos_encontrados

    # Por ultimo, para que los generos no se repitan empleamos set() y todo ello lo guardamos en la varibale generos_unicos
    generos_lista = sorted(set(generos_encontrados))
    
    # Creamos dos columnas
    col1, col2 = st.columns(2)
    
    import streamlit as st

    with col1:
        generos_seleccionados = st.multiselect(
            "Selecciona tus géneros favoritos:",
            generos_lista,
            max_selections=2,
            accept_new_options=True
        )

        # Mostrar la selección
        st.markdown(f"Géneros seleccionados: {generos_seleccionados}")

    # AHORA CREAREMOS EL FILTRO DE DURACIÓN

    # Primero, con un bucle for clasificaremos las canciones en los rangos y crearemos una nueva columan en el df
    rangos_duracion= []

    for fila in df_discografia['Duracion_segundos']:
        if fila <= 180:
            rangos_duracion.append("corta")
        elif 180 < fila <= 270:
            rangos_duracion.append("media")
        else:
            rangos_duracion.append("larga")
    
    df_discografia["Rango_duracion"]= rangos_duracion


   # Estos rangos los creamos a partir de la duración promedio que es 4 minutos
    dic_rango_duracion = {
    "corta": "menor a 3 minutos",        
    "media": "entre 3 y 4 minutos y medio",      
    "larga": "mayor a 4 minutos y medio"
    }

    with col2: # Creamos el filtro de duración
        duracion_seleccionada = st.select_slider("Selecciona un rango",
            options=[
                "corta", 
                "media", 
                "larga"
            ],
        )
    
        st.write(f"⏱️La duración de tu canción será: {dic_rango_duracion[duracion_seleccionada]}")

    # Variable para verificar si hay resultados
    encontrado = False

    # Recorremos el DataFrame con un bucle
    for i in range(len(df_discografia)): # El bucle recorre cada fila del DataFrame
        titulo_cancion = df_discografia.loc[i, "titulo"] # Accede al valor de la columna "titulo" en la fila i
        portada_cancion = df_discografia.loc[i, "Link_portada"] # Guarda la portada por cancion
        album_cancion = df_discografia.loc[i, "Álbum"] # Guarda el album por cancion
        año_cancion = df_discografia.loc[i, "Año"] # Guarda el año por cancion
        link_spotify = df_discografia.loc[i, "Link_spotify"] # Guarda el link de spotify
        mv_cancion = df_discografia.loc[i, "Link_mv"] # Guarda el link del mv
        letras_cancion = df_discografia.loc[i, "Link_letras"] # Guarda las letras
        generos= df_discografia.loc[i, "Genero"]
        reproducciones = df_discografia.loc[i, "Reproducciones en Spotify"]
        duracion_cancion= df_discografia.loc[i, "Duración"]
        duracion_rango= df_discografia.loc[i, "Rango_duracion"]   # La duración la tenga en este formato 3:20 -> como lo convierto a segundos para generar el buscador

        #FILTRO DE GENERO
        coincide_genero= True
        for genero in generos_seleccionados:
            if genero not in str(generos).lower():
                coincide_genero= False
                break
        if coincide_genero:
            if duracion_rango == duracion_seleccionada:
                st.markdown(f"## {titulo_cancion}")
                st.markdown(f"Álbum: *{album_cancion}* ({año_cancion})")
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.image(portada_cancion, width=300)
                with col2:
                    st.markdown(f"<a href='{link_spotify}' target='_blank'><button>🎧 Escuchar en Spotify</button></a>", unsafe_allow_html=True)                    
                    st.markdown(f"<a href='{letras_cancion}' target='_blank'><button>📜 Ver Letra</button></a>", unsafe_allow_html=True)
                    if df_discografia.loc[i, "Video Musical"] == "True":
                        st.markdown(f"<a href='{mv_cancion}' target='_blank'><button>🎬 Ver MV</button></a></div>", unsafe_allow_html=True)
                    encontrado = True # Activa una variable booleana para marcar que sí hubo un resultado
    
    if not encontrado:
        st.warning("No hay canciones con esas características 😥")
    

elif pagina_seleccionada=="♡ Videoclips":
    
    # Agregamos un título para la página de gráficos
    st.markdown("<h1 style='text-align: center;'><em>EXPLORA</em> <span style='color: #d8a7b1;'>VIDEOCLIPS</span></h1>",  unsafe_allow_html=True)

    import pandas as pd
    import folium
    from streamlit_folium import st_folium
    import streamlit as st
   
    df_discografia = pd.read_excel("base de datos.xlsx")
    
    # Creamos el primer mapa
    mapa = folium.Map(location=[24.313986350161017, 22.920401024174712], zoom_start=2)

    # Recorremos las filas del DataFrame
    for _, fila in df_discografia.iterrows():
        lat = fila["Latitud_video"]
        lon = fila["Longitud_video"]
        nombre = fila["titulo"]
        año = fila["Año"]
        lugar = fila["Lugar de grabación"]
        dato = fila["Dato_lugar"]

        # Verificamos que haya coordenadas
        if pd.notna(lat) and pd.notna(lon):
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(
                    f"<b>{nombre}</b> ({año})<br><i>{lugar}</i><br><span style='color:#C71585'>{dato}</span>",
                    max_width=300
                ),
                icon=folium.Icon(color='beige', icon="info-sign")
            ).add_to(mapa)

    # Mostrar en tu app Streamlit
    st.subheader("📍 Lugares donde se filmaron sus videos musicales")
    st.markdown("Haz clic en los íconos para ver más información sobre cada videoclip.")
    st.toast("🎥 ¡Mira el video musical abajo!")
    # Visualiza el mapa en la app
    st_folium(mapa, width=700, height=500)

    st.header("🎬 Buscador de videoclips")
    busqueda = st.text_input("🔎 Escribe el nombre de la canción para ver su video musical: ").lower()

    # Variable para verificar si hay resultados
    if busqueda:
        encontrado = False

        # Recorremos el DataFrame con un bucle
        for i in range(len(df_discografia)):
            tiene_video=df_discografia.loc[i, "Video Musical"]
  
            if str(tiene_video).lower()== "true":
                nombre = df_discografia.loc[i, "titulo"] # Accede al valor de la columna "Drivers" en la fila i
                album= df_discografia.loc[i, "Álbum"]
                link_mv = df_discografia.loc[i, "Link_mv"] # Guarda el país (nacionalidad) del pilot
                fotografia_lugar= df_discografia.loc[i, "Fotografía_lugar"]
                bts= df_discografia.loc[i, "BTS"]

                if busqueda in nombre.lower():
                    st.subheader(f"{nombre}")
                    st.markdown(f"<em>➻Del album {album}</em>", unsafe_allow_html=True)
                    st.video(link_mv)
                    if pd.notna(fotografia_lugar):
                        st.image(fotografia_lugar, caption="📸 Lugar de grabación", use_container_width=True)

                    if pd.notna(bts):
                        st.markdown("🎬 **Behind the scenes:**")
                        st.video(bts)
                    encontrado = True # Activa una variable booleana para marcar que sí hubo un resultado

        # Si no se encontró ningún piloto
        if not encontrado:
            st.warning("😢 Esta canción no tiene video musical. Intenta con una que aparezca en el mapa.")

elif pagina_seleccionada==  "♡ Original vs Taylor's Version":
    
    # Importamos las librerias que necesitamos 
    import streamlit as st
    import pandas as pd
    import plotly.graph_objects as go

    # Traemos el df_discografia para poner crear los
    df_discografia = pd.read_excel("base de datos.xlsx")

    # Recuperamos las portadas de álbumes
    portadas_albumes = list(df_discografia["Link_portada"].unique()) #Sin embargo, contara también los links de las portadas de los singles
    portadas_albumes= portadas_albumes[0:15]

    era_seleccionada = None
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("Fearless", use_container_width=True):
            era_seleccionada = "Fearless"

    with col2:
        if st.button("Speak Now", use_container_width=True):
            era_seleccionada = "Speak Now"

    with col3:
        if st.button("Red", use_container_width=True):
            era_seleccionada = "Red"

    with col4:
        if st.button("1989", use_container_width=True):
            era_seleccionada = "1989"
    
    #Ya tengo los botones 
    # Ahora quiero entrar al df y extraer un df ssegun la accion
    if era_seleccionada is not None:
        filas_filtradas = []
        for i, fila in df_discografia.iterrows():
            album= str(fila["Álbum"]).strip()
            if album == era_seleccionada or album== f"{era_seleccionada} (Taylor's Version)":
                filas_filtradas.append(fila)
       

        df_era_seleccionada = pd.DataFrame(filas_filtradas)
        st.markdown(f"### Canciones de {era_seleccionada} y su Taylor's Version")
        st.dataframe(df_era_seleccionada)
        st.markdown(f"### GRAFICO COMPARTIVO {era_seleccionada} ERA")

        # HASTA ACA YA TENEMOS EL DF SEPARADO SEGUN UNA SOLA ERA CON DF_ERA_SELECCIONADA
        # AHORA TOCA PASAR LO DE COLAB

        canciones_originales = []
        canciones_regrabadas = []
        reproducciones_originales = []
        reproducciones_regrabadas = []
        canciones_vault = []
        reproducciones_vault = []

        # ITERAMOS SOBRE LAS FILAS FILTRADAS
        for _, fila in df_era_seleccionada.iterrows():
            titulo = str(fila['titulo']).strip()
            album = str(fila['Álbum']).strip()
            reproducciones = int(fila['Reproducciones en Spotify'])

            if album == era_seleccionada:
                canciones_originales.append(titulo)
                reproducciones_originales.append(reproducciones)
            elif album == f"{era_seleccionada} (Taylor's Version)":
                if "(from the vault)" in titulo.lower():
                    canciones_vault.append(titulo)
                    reproducciones_vault.append(reproducciones)
                else:
                    canciones_regrabadas.append(titulo)
                    reproducciones_regrabadas.append(reproducciones)

        # Pasamos los datos a un data frame nuevo, para luego hacer el grafico
        df_version_original= pd.DataFrame({'Canciones_og': canciones_originales, 'Reproducciones_og': reproducciones_originales})
        df_version_regrabada= pd.DataFrame({'Canciones_tv': canciones_regrabadas, 'Reproducciones_tv': reproducciones_regrabadas})
        df_vault= pd.DataFrame({'Canciones_ftv': canciones_vault, 'Reproducciones_ftv': reproducciones_vault})

        # LIMPIAMOS LOS DFS
        # Necesitamos quitar el (Taylor's Version) del df_version_regrabada, para poder combinar los data frames después
        # Eliminamos espacios al inicio y al final de los nombres de canciones para que puedan coincidir al combinar los dataframes

        df_version_regrabada["Canciones_og"] = df_version_regrabada["Canciones_tv"].str.replace(" \(Taylor's Version\)", "", regex=True)

        df_version_original["Canciones_og"] = df_version_original["Canciones_og"].astype(str).str.strip()
        df_version_regrabada["Canciones_og"] = df_version_regrabada["Canciones_og"].astype(str).str.strip()

        # COMBINAMOS LOS DOS DATAFRAMES PRINCIPALES
        df_comparacion = pd.merge(
            df_version_original,
            df_version_regrabada[['Canciones_og', 'Reproducciones_tv']],
            on='Canciones_og'
        )

        st.write("▶️ DataFrame comparativo", df_comparacion)

        # AHORA SI PODEMOS CREAR LOS GRAFICOS-> CON PLOTLY EXPRESS

        import plotly.graph_objects as go # https://plotly.com/python/bar-charts/

        # Creamos una variable que contenga una lista de canciones-> las cuales luego usaremos como las etiquetas del eje x para cada una de las barras dobles
        canciones = df_comparacion['Canciones_og']

        # En otras dos variables, colocamos las reproducciones tanto de la version original como la versión regrabada -> estas dos variable serán las barras dobles
        reproducciones_og = df_comparacion['Reproducciones_og']
        reproducciones_tv = df_comparacion['Reproducciones_tv']
        # Diccionario de colores por era
        colores_eras = {
            "Fearless": {
                "original": "#d6b751",  # dorado
                "tv": "#8a6434"         # bronce oscuro
            },
            "Speak Now": {
                "original": "#b495c8",  # lila suave
                "tv": "#5d3a73"         # púrpura profundo
            },
            "Red": {
                "original": "#e63946",  # rojo vibrante
                "tv": "#a4161a"         # rojo oscuro
            },
            "1989": {
                "original": "#add8e6",  # celeste
                "tv": "#2f8dd9"         # azul acero
            }
        }


        # Creamos el gráfico
        fig = go.Figure()

        # Ahora creamos la primera barra: que será la versión original
        fig.add_trace(go.Bar(
            x=canciones,  # llamamos a la variable que creamos al inicio para que sean las barras del eje x
            y=reproducciones_og,   # llamamos a la variable reproduciones_og que serán los valores en el eje y
            name='Versión original',  # Este nombre nos guiará en la leyenda: le ponemos la etiqueta Versión original
            marker_color=colores_eras[era_seleccionada]["original"]  #Le ponemos un color diferenciador
        ))

        # Ahora creamos la segunda barra: que será la versión regrabada (Taylor's Version)
        fig.add_trace(go.Bar(
            x=canciones,
            y=reproducciones_tv,
            name= "Taylor's Version",
            marker_color=colores_eras[era_seleccionada]["tv"] # Le ponemos un color caracteristico
        ))

        # Diseño
        fig.update_layout(
            title=(f"Comparación de reproducciones: {era_seleccionada} vs {era_seleccionada} (Taylor's Version)"),
            xaxis_title="Canción",
            yaxis_title="Reproducciones en Spotify",
            barmode='group',
            xaxis_tickangle=-45,
            template='plotly_white',
            legend_title_text='Versión'
        )

        # Mostrar el gráfico en Streamlit
        st.plotly_chart(fig, use_container_width=True)


elif pagina_seleccionada == "♡ Sección Lúdica":
    
    st.title("🌟🎤 Bienvenid@ al Juego del Ahorcado (Taylor's Version) 🎤🌟")
    # Traemos el df_discografia para poner crear los
    import pandas as pd
    import random

    df_discografia = pd.read_excel("base de datos.xlsx")

    # LISTA DE ALBUMES
    lista_albumes= list(df_discografia["Álbum"].unique())
    lista_albumes.remove("single")

    # Selecionamos solo los albumes de nombre unico, es decir no tomaremos en cuenta los (Taylor's Version) pues llevan el mismo nombre
    albumes_juego= lista_albumes[0:11]

    albumes_minuscula = []

    for album in albumes_juego:
        album_minuscula = str(album).lower().strip().replace(" ", "")   # Convertimos el álbum a minúscula
        albumes_minuscula.append(album_minuscula)  # Lo agregamos a la nueva lista
    
    # Trabajaremos con la lista que ya creamos -> albumes_minuscula
        
    if "palabra_secreta" not in st.session_state:
        st.session_state.palabra_secreta = random.choice(albumes_minuscula)
        st.session_state.letras_adivinadas = []
        st.session_state.intentos = 0
        st.session_state.intentos_maximos = 5
        st.session_state.terminado = False

    palabra = st.session_state.palabra_secreta
    letras_adivinadas = st.session_state.letras_adivinadas
    intentos = st.session_state.intentos
    intentos_maximos = st.session_state.intentos_maximos

    # Mostrar progreso
    progreso = ""
    for letra in palabra:
        if letra in letras_adivinadas:
            progreso += f"{letra} "
        else:
            progreso += "_ "
    st.markdown(f"🔮 Tu era misteriosa tiene {len(palabra)} letras: {progreso.strip()}")

    # Input del jugador
    if not st.session_state.terminado:
        intento = st.text_input("Adivina una letra:", max_chars=1).lower()

        if intento:
            if len(intento) != 1:
                st.warning("🚫 Ingresa solo UNA letra.")
            elif intento in letras_adivinadas:
                st.info("🔁 Ya intentaste con esa letra.")
            else:
                letras_adivinadas.append(intento)

                if intento in palabra:
                    st.success("🎯 ¡Sí! Esa letra está en la era.")
                else:
                    st.session_state.intentos += 1
                    st.error(f"💔 Letra incorrecta. Te quedan {intentos_maximos - st.session_state.intentos} intento(s)...")

        # Verificar si ganó
        if all(letra in letras_adivinadas for letra in palabra):
            st.balloons()
            st.success(f"🎉 ¡Felicidades, Swiftie! Adivinaste la era secreta: {palabra.upper()} 🎉")
            st.markdown("""<div style="text-align: center;"><img src="https://i.pinimg.com/originals/c7/00/fb/c700fb31450511f5b5dd1e3739fc486e.gif" width="300"></div>""",unsafe_allow_html=True)            
            st.session_state.terminado = True

        # Verificar si perdió
        if st.session_state.intentos >= intentos_maximos:
            st.error(f"☠️ Se acabaron los intentos. La era secreta era: {palabra.upper()}")
            st.markdown("""<div style="text-align: center;"><img src="https://media.tenor.com/9NceTmMh1_AAAAAM/girl-woman.gif" width="300"></div>""",unsafe_allow_html=True)            
            st.session_state.terminado = True

    # Mensaje final
    if st.session_state.terminado:
        mensajes_eras = {
            "taylorswift": "🌟 Debut vibes: cuando todo empezó y aún cantaba sobre teardrops on my guitar.",
            "fearless": "💛 Fearless es para los valientes enamorados... ¡You belong with me!",
            "speaknow": "💜 ¡Speak Now o calla para siempre! Una era llena de cuentos de hadas y guitarrazos.",
            "red": "❤️ RED: porque nada es más intenso que estar en un romance rojo y trágico.",
            "1989": "💙 ¡Welcome to New York! Estás en la era pop brillante y elegante.",
            "reputation": "🖤 Look what you made me do... acertaste en la era más oscura y poderosa.",
            "lover": "💕 Lover: puro romance pastel y confesiones en colores rosa.",
            "folklore": "🌲 folklore: susurros de piano, bosques, y cardigan mojados por la lluvia.",
            "midnights": "🌌 Midnights: pensamientos brillantes a las 3am.",
            "evermore": "🍂 evermore: melodías tristes, cuentos eternos.",
            "thetorturedpoetsdepartment": "🤍 The Tortured Poets Department: poesía y corazones rotos."
        }

        st.markdown("📝 Mensaje especial de la era:")
        st.info(mensajes_eras.get(palabra, "✨ Era desconocida pero siempre mágica."))
        
        # Botón para reiniciar
        if st.button("🔄 Jugar otra vez"):
            for key in ["palabra_secreta", "letras_adivinadas", "intentos", "terminado"]:
                del st.session_state[key]
            