# Primero, importamos la libreria streamlit para iniciar a programar
import streamlit as st 
import random # Para el boton musical que crearemos a continuacion
import pandas as pd # Para manipular la base de datos
import folium # Para el mapa
import plotly.express as px # Para los graficos
import plotly.graph_objects as go # Para los graficos

# Vamos a necesitar 5 paginas, para ello creamos una lista con el nombre de cada pagina y las guardamos en la varibale paginas
paginas = ["♡ Conoce a Taylor", "♡ Canciones", "♡ Videoclips", "♡ Original vs Taylor's Version", "♡ Sección Lúdica"]

# Importamos la base de datos y lo leemos con pandas, lo guardamos en la varibale df_discografia.
df_discografia = pd.read_excel("base de datos.xlsx")

# BOTON MUSICAL  
# Primeero, nos dirigimos a la columna "Link_spotify" de la base de datos df_discografia, tomamos todos los datos en ella y creamos una lista con .tolist()
# Luego, con random.choice (de la libreria random) elige una cancion al azar de la lista que creamos
# Esa canción se guarda en la variable cancion_aleatoria
cancion_aleatoria = random.choice(df_discografia["Link_spotify"].tolist()) 

# Vamos a mostrar esa cancion en la barra lateral por lo que agregamos .sidebar a st.markdown
# Generamos un buton que contenga el link que lleve a la cancion
st.sidebar.markdown(f"<a href='{cancion_aleatoria}' target='_blank'><button>🎧 Escucha una canción aleatoria</button></a>", unsafe_allow_html=True)

# Creamos botones de navegación tomando la lista de páginas
pagina_seleccionada = st.sidebar.selectbox('Selecciona una página', paginas)

# Generamos condicionales para mostrar el contenido de cada página
if pagina_seleccionada == "♡ Conoce a Taylor": # Si en el desplegable la pagina elegida es "♡ Conoce a Taylor" se muestra este contenido:

    # Con la función st.markdown mostramos el titulo de la primera pagina
    # Markdown nos permite darle más detalle al contenido. Lo alineamos al centro, con <em></em> ponemos en cursiva, luego agregamos un salto de linea <br> y para darle color a "Taylor Swift" agregamos <span style='color: #d8a7b1;'>
    st.markdown("<h1 style='text-align: center;'><em>ANATOMÍA DE UN ÍCONO:</em><br>Explorando la discografía de <br><span style='color: #d8a7b1;'>Taylor Swift</span></h1>", unsafe_allow_html=True)
    
    # Generamos dos columnas, la primera bajo la variable col1, y la segunda col2
    col1, col2 = st.columns(2)

    # BIOGRAFIA
    # Streamlit nos da una función que nos permite darle un efecto de maquina de escirbir a un texto, para ello importamos la libreria time
    import time
    def stream_biografia():
        with open("biografia.txt", "r", encoding="utf-8") as archivo: #Abrimos el archivo .txt que contiene la libreria en modo lectura "r"
            texto = archivo.read() # Guardamos el contenido del archivo en la variable texto
        for palabra in texto.split(" "): # Con .split() separar palabra por palabra y luego con un bucle iremos recorriendo cada una
            yield palabra + " " # Las palabras s iran escribiendo seguidas de un espacio, yield nos permite entregarlo todo de manera continua dandole el efecto que queremos
            time.sleep(0.02) # Establecemos el tiempo entre cada palabra

    # Le ponemos un titulo a la seccion empleando st.markdown, y en cursivas con <em></em>, le damos más tamaño con <h3></h3> 
    st.markdown("<h3><em>¿Quién es Taylor Swift?</em></h3>", unsafe_allow_html=True)

    # Generamos el boton para presentar la biografia. 
    if st.button("Descúbrelo"):  # Si se presiona este boton:
        st.image("taylor6.jpg", caption="Taylor Swift", use_container_width=True) # Se presenta la imagen de Taylor  
        st.write_stream(stream_biografia) # Y se ejecuta la funcion que definimos para el efecto de maquina de escirbir en la biografia

    # DISCOGRAFIA DE TAYLOR SWIFT
    # Creamos una lista de álbumes
    lista_albumes = list(df_discografia["Álbum"].unique()) # Tomamos los datos del df_discografia en la columna "Álbum", recogiendo solo los datos unicos con .unique()
    lista_albumes.remove("single") # Vamos a eliminar los singles para esta presentación con .remove()

    # Años de los albumes
    # Primero, con .groupby() agrupamos las filas del df segun la columna "Album"
    # Luego, dentro de cada grupo, selecciona la fila "Año" y toma el primer valor (.first()) que aparezca asociado al album-> como se repiten 
    # Finalmente, limitamos los resultados a los primeros 15 álbumes con [0:15], excluyendo así los singles
    años_por_album = df_discografia.groupby("Álbum")["Año"].first()[0:15] 

    # Cantidad de canciones por album 
    # Con .groupby() agrupamos los datos de la columna 'titulo' segun la columna 'Álbum', es decir, agrupamos todas las canciones que pertencen al mismo album.
    # Luego, con .count() cuenta cuántos canciones hay por cada álbum
    canciones_por_album = df_discografia.groupby('Álbum')['titulo'].count()

    # Portadas de los álbumes
    portadas_albumes = list(df_discografia["Link_portada"].unique()) # De la columna "Link_portada" del df_discografia toma los valor unicos pues las canciones que pertencen al mismo album comparten portada
    portadas_albumes= portadas_albumes[0:15] # Seleccionamos solo las primeras 15 portadas, el ultimo es el indice 14, pero en esta funcion si queremos llegar hasta el indice 14 debemos poner 15
    
    # Reproducciones por álbum
    # Tambien empleamos la funcion .groupby() en este caso le estamos diciendo-> agrupa las canciones por álbum y suma todas sus reproducciones (.sum())
    reproducciones_por_albumes = df_discografia.groupby('Álbum')['Reproducciones en Spotify'].sum()


    # Procedemos a la presentación de los albumes
    st.title("📀 Discografía de Taylor Swift")

    for i in range(len(lista_albumes)): # Primero creamos un bucle que iterara según la cantidad de albumes de nuestra lista_albumes, para ello empleamos range(len()) que crea la lista automaticamente
        nombre_album = lista_albumes[i] # Extraemos el nombre del álbum de lista_albumes y tomara el correspondiente al índice actual 'i'. Por ejemplo, si i = 0, se obtiene el primer álbum; si i = 1, el segundo, y así sucesivamente.
        año_album = años_por_album.loc[nombre_album]    # Buscamos el año de ese álbum en la serie 'años_por_album' usando .loc[nombre_album], lo que nos devuelve el año asociado a ese álbum.
        cantidad_canciones = canciones_por_album.loc[nombre_album] # Accedemos a la cantidad de canciones de ese álbum utilizando .loc sobre la serie'canciones_por_album', que ya contiene la cuenta agrupada por álbum
        portada_album = portadas_albumes[i] # Para la portada, se empleará la logica de nombre_album, pero ahora en la lista portadas_albumes
        reproducciones_por_album = reproducciones_por_albumes.loc[nombre_album]    # Finalmente, consultamos la cantidad total de reproducciones del álbum desde la serie 'reproducciones_por_albumes' usando el nombre del álbum como clave con .loc.

        with st.container():
            col1, col2 = st.columns([2, 1])  # Creamos dos columnas
            with col1: # En la primera columna irá lo siguiente: el nombre del álbum en negrita <b>, cursiva <i> con un tamaño mediano <h4>, ello como encabezado seguido de una lista <li>: el año de ese álbum, su número de canciones y reproducciones.
                st.markdown(f"""
                <h4><i><b>{nombre_album}</b></i></h4>
                <ul>
                    <li><b>Año:</b> {año_album}</li>
                    <li>Canciones: {cantidad_canciones}</li>
                    <li>📈 Reproducciones aproximadas: {reproducciones_por_album:,}</li>
                </ul>
                """, unsafe_allow_html=True)
        with col2: # En la segunda columna, colocamos la portada del album con st.image y definimos un tamaño de 200
            st.image(portada_album, width=200)
    #AQUI TERMINA EL CONTENIDO DE LA PAGINA 1

elif  pagina_seleccionada == "♡ Canciones":  # Si en el desplegable la página elegida es "♡ Canciones" se muestra este contenido:
    
    # Agregamos un título a la página que irá en el centro (<h1 style='text-align: center;'>) : <em> le da cursiva y con  <span style='color: #d8a7b1;'> le damos color a la palabra CANCIONES.
    st.markdown("<h1 style='text-align: center;'><em>DESCUBRE</em> <span style='color: #d8a7b1;'>CANCIONES</span></h1>",  unsafe_allow_html=True)

    # BUSCADOR DE CANCIONES SEGUN EL GENERO Y DURACION

    # Primero, para el filtro de género, necesitamos obtener los generos disponibles en las canciones. 
    generos_encontrados= [] # Creamos una lista vacia que almacenará los generos que encontremos

    # Recorremos cada fila del DataFrame con un bucle for y .iterrows()
    for i, fila in df_discografia.iterrows():
        texto_genero = str(fila["Genero"])  # Obtenemos todo el contenido de la columna "Genero" como un texto y lo guardamos en la variable texto_genero
        lista_generos = texto_genero.split(",")  # Ahora ese texto lo separamos con .split(), separará cada que encuentre una coma, eso lo almacenamos en la variable lista_generos

    # Ahora, con un bucle for para cada género en la lista_generos, quitamos espacios con .strip() y lo pasamos a minúscula con .lower(). 
        for genero in lista_generos:
            genero_depurado = genero.strip().lower()
            generos_encontrados.append(genero_depurado) # Luego, agregamos ese genero ya depurado a la lista que creamos al inicio: generos_encontrados

    # Por ultimo, para que los generos no se repitan empleamos set() y todo ello lo guardamos en la variable generos_lista
    generos_lista = sorted(set(generos_encontrados))
    
    # Ahora ya podemos crear la interfaz interactiva para que el usuario seleccione los generos deseados 
    col1, col2 = st.columns(2) # Creamos dos columnas (en uno ira la interfaz de genero y en la otra la de duracion)

    with col1: 
        generos_seleccionados = st.multiselect( # Esta funcion st.multiselect nos permite crear un menu desplegable
            "Selecciona tus géneros favoritos:", # Este será el texto visible arriba de la interfaz
            generos_lista,  # De esta lista sacará los generos a mostrarse en el desplegable
            max_selections=2, # La selección maxima será 2 géneros
            accept_new_options=False  # Desactivamos la opcion de agregar nuevas opciones
        )

        # Debajo mostramos la selección que hizo el usuario
        st.markdown(f"Géneros seleccionados: {generos_seleccionados}")

    
    # AHORA CREAREMOS EL FILTRO DE DURACIÓN

    # Definimos una función de conversión del formato mm:ss a segundos en general
    def duracion_a_segundos(duracion_str):
        minutos, segundos = map(int, duracion_str.split(':')) # convierte el texto duración_str en dos variables separadas-> el primero:minutos, el segundo:segundos
        return minutos * 60 + segundos # lo que devolverá será: la variable minutos multiplicada por 60, sumado con la variable segundos

    # Creamos una nueva columna "Duración_segundos" al df_discografia y su contenido sera la funcion que definimos aplicada a la columna "Duración"
    df_discografia["Duracion_segundos"] = df_discografia["Duración"].apply(duracion_a_segundos)

    # Primero, con un bucle for clasificaremos las canciones en los rangos y crearemos una nueva columan en el DataFrame
    rangos_duracion= [] # Creamos una lista vacia donde iremos almacenando los datos 

    for fila in df_discografia["Duracion_segundos"]: # Con un bucle for recorremos cada duracion en segunos de las canciones -> accedemos a través del df_discografia seleccionando la columna de Duracion_segundos
        if fila <= 180: # Si la canción de esa fila dura menos o igual a 180 segundos
            rangos_duracion.append("corta") # se agrega (.append()) la palabra corta a la lista vacia del i        
        elif 180 < fila <= 270: # Si la cancion de esa fila dura más de 180 segundos pero menos o igual a 270 segundos 
            rangos_duracion.append("media") # se agrega la palabra media a la lista
        else: # Con else cubrimos todos los demas casos que seria si la cancion dura más de 270 segundos
            rangos_duracion.append("larga") # Y a la lista agrega la palabra larga

    #Creamos una nueva columna en el df llamada Rango_duracion y ahi almacenamos los datos de la lista rangos_duracion
    df_discografia["Rango_duracion"]= rangos_duracion


   # Los rangos se crearon a partir de la duración promedio de una cancion que es 4 minutos
    dic_rango_duracion = { # Creamos un diccionario con cuanto equivale cada denominacion de rango
    "corta": "menor a 3 minutos",        
    "media": "entre 3 y 4 minutos y medio",      
    "larga": "mayor a 4 minutos y medio"
    }

    with col2: # Ahora si emplearemos la columna 2 para presentar la interfaz de duracion
        duracion_seleccionada = st.select_slider("Selecciona un rango:", # Creamos un slider con st.select_slider en el que el usuario elegira un rango
            options=[ # Establecemos las opciones
                "corta", 
                "media", 
                "larga"
            ],
        )
        # Y presentamos cuando durara la cancion aproximadamente ssegun el rango que elegió el usuario a partir del diccionario de equivalencias
        st.write(f"⏱️La duración de tu canción será: {dic_rango_duracion[duracion_seleccionada]}")

    # Procedemos a generar el buscador
    encontrado = False   # Variable para verificar si hay resultados

    # Recorremos el DataFrame con un bucle for
    for i in range(len(df_discografia)): # El bucle recorre cada fila del DataFrame
        titulo_cancion = df_discografia.loc[i, "titulo"] # Accede al valor de la columna "titulo" en la fila i del DataFrame. Guarda el nombre de la canción actual.
        portada_cancion = df_discografia.loc[i, "Link_portada"] # Guarda el link a la imagen de portada correspondiente a la canción en la fila i. Se toma de la columna "Link_portada".
        album_cancion = df_discografia.loc[i, "Álbum"] # Obtiene el nombre del álbum al que pertenece la canción, desde la columna "Álbum" de esa fila.
        año_cancion = df_discografia.loc[i, "Año"] # Extrae el año en que se lanzó la canción, desde la columna "Año".
        link_spotify = df_discografia.loc[i, "Link_spotify"] # Recupera el enlace directo a Spotify para la canción, desde la columna "Link_spotify".
        mv_cancion = df_discografia.loc[i, "Link_mv"] # Obtiene el link al video musical (MV) de la canción, desde la columna "Link_mv".
        letras_cancion = df_discografia.loc[i, "Link_letras"] # Obtiene el link hacia la página donde se encuentran las letras de la canción, desde "Link_letras".
        generos= df_discografia.loc[i, "Genero"] # Recupera la información de los géneros musicales asociados a esa canción, desde la columna "Genero". Este dato sirve para el filtro de género que el usuario seleccionó.
        reproducciones = df_discografia.loc[i, "Reproducciones en Spotify"] # Extrae el número total de reproducciones en Spotify que tiene esa canción, desde la columna "Reproducciones en Spotify"
        duracion_cancion= df_discografia.loc[i, "Duración"] # Toma la duración de la canción en formato string (por ejemplo, "3:20") desde la columna "Duración".
        duracion_rango= df_discografia.loc[i, "Rango_duracion"]   # Toma el valor de duración ya clasificado como "corta", "media" o "larga", según el tiempo en segundos. Este dato sirve para el filtro de duración que el usuario seleccionó.

        #FILTRO DE GENERO
        coincide_genero= True # Creamos una variable booleana que asumimos como verdadera al inicio. Nos servirá para verificar si la canción cumple con todos los géneros seleccionados.
        for genero in generos_seleccionados: # Iteramos por cada género que el usuario haya seleccionado en el filtro de géneros.
            if genero not in str(generos).lower(): # Si ese género seleccionado no está  en los géneros de la canción actual...
                coincide_genero= False # la varible booleana coincide_generos será False
                break # y es bucle se rompe.
        if coincide_genero:  # Si la canción sí coincide con los géneros seleccionados…
            if duracion_rango == duracion_seleccionada: # y la duración de rango de esa canción es igual a la seleccionada por el usuario...
                st.markdown(f"## {titulo_cancion}") # Mostramos el título de la canción en formato grande (##).
                st.markdown(f"Álbum: *{album_cancion}* ({año_cancion})") # Mostramos el nombre del álbum en cursiva y el año entre paréntesis.
                col1, col2 = st.columns([1, 2])  # Creamos dos columnas: la primera más pequeña para la portada y la segunda más grande para los botones de enlaces.
                with col1: # En la columna izquierda mostramos la imagen de la canción. Se fija el ancho a 300 píxeles.
                    st.image(portada_cancion, width=300)
                with col2: # En la otra columna...
                    st.markdown(f"<a href='{link_spotify}' target='_blank'><button>🎧 Escuchar en Spotify</button></a>", unsafe_allow_html=True) # Se crea un botón HTML que lleva al link de Spotify en una nueva pestaña.                    
                    st.markdown(f"<a href='{letras_cancion}' target='_blank'><button>📜 Ver Letra</button></a>", unsafe_allow_html=True) # Botón que abre la página con la letra de la canción.
                    if df_discografia.loc[i, "Video Musical"] == "True": # Verificamos si esa canción tiene video musical ( si la columna "Video Musical" dice "True").
                        st.markdown(f"<a href='{mv_cancion}' target='_blank'><button>🎬 Ver MV</button></a></div>", unsafe_allow_html=True) # Si sí tiene, mostramos el botón para ver el video musical.
                    encontrado = True # Activa la variable booleana para marcar que sí hubo un resultado
    
    if not encontrado: # Si ninguna canción pasó los filtros de género y duración:
        st.warning("No hay canciones con esas características 😥") # Mostramos un mensaje de advertencia visual en Streamlit.
    #AQUI TERMINA EL CONTENIDO DE LA PAGINA 2

elif pagina_seleccionada=="♡ Videoclips": # Si en el desplegable la página elegida es "♡ Videoclips" se muestra este contenido:
    
    # Agregamos un título principal con estilos HTML: centrado, parte en cursiva<em> y parte en color rosa <span style='color: #d8a7b1;'>
    st.markdown("<h1 style='text-align: center;'><em>EXPLORA</em> <span style='color: #d8a7b1;'>VIDEOCLIPS</span></h1>",  unsafe_allow_html=True)
    
    # Para poder integrar mapas de Folium en Streamlit.
    from streamlit_folium import st_folium

    # Creamos el primer mapa con un zoom que nos permitirá ver la mayoría de datos.
    mapa = folium.Map(location=[24.313986350161017, 22.920401024174712], zoom_start=2)

    # Recorremos cada fila del DataFrame para añadir los videoclips al mapa
    for _, fila in df_discografia.iterrows():
        lat = fila["Latitud_video"] # Obtenemos la latitud del lugar de grabación de la columna del mismo nombre.
        lon = fila["Longitud_video"] # Obtenemos la longitud del lugar de grabación de la columna del mismo nombre.
        nombre = fila["titulo"] # Obtenemos el nombre de la canción de la columna "titulo".
        año = fila["Año"] # Obtenemos el año de la canción de la columna del mismo nombre.
        lugar = fila["Lugar de grabación"] # Obtenemos el lugar de grabación de la columna del mismo nomnre.
        dato = fila["Dato_lugar"] # Por último, obtenemos un dato adicional del lugar

        # # Verificamos que sí existan coordenadas para agregar el punto, pues no todas las canciones tienen video musical.
        if pd.notna(lat) and pd.notna(lon):
            folium.Marker(
                location=[lat, lon], # Posiciona el marcador con las variable lat y lon
                popup=folium.Popup( # Esta será la ventana emergente al hacer clic
                    f"<b>{nombre}</b> ({año})<br><i>{lugar}</i><br><span style='color:#d8a7b1'>{dato}</span>", # Título en negrita y año entre paréntesis, lugar de grabación en cursiva, información adicional en color rosa claro (#d8a7b1)
                    max_width=300
                ),
                icon=folium.Icon(color='pink', icon="info-sign") # Ícono rosa con símbolo de información
            ).add_to(mapa) # Y agregamos el marcador al mapa
    
    # Agregamos un subtítulo (st.subheader) para guiar al usuario sobre qué verá en el mapa
    st.subheader("📍 Lugares donde se filmaron sus videos musicales")
    st.markdown("Haz clic en los íconos para ver más información sobre cada videoclip.") # Instrucciones para el usuario
    st.toast("🎥 ¡Mira el video musical abajo!") # Con st.toast mostramos un aviso dinámico en la pantalla como un pop-up 
    st_folium(mapa, width=700, height=500) # Mostramos el mapa

    # Debajo del mapa interactivo colocaremos un buscador de videoclips para que la interacción sea completa
    st.header("🎬 Buscador de videoclips") # Colocamos un subtitulo
    # Presentamos un cuadro de texto con st.text_input para que el usuario escriba el nombre de la canción y con .lower() convierte el texto a minúsculas para facilitar la comparación
    busqueda = st.text_input("🔎 Escribe el nombre de la canción para ver su video musical: ").lower() 

    # Verificamos si se escribió algo en el cuadro de texto
    if busqueda:
        encontrado = False  # Variable para saber si se encontró alguna coincidencia, iniciamos con False

        # Recorremos todas las filas del DataFrame a partir de una list con la cantidad de filas del mismo
        for i in range(len(df_discografia)):
            tiene_video=df_discografia.loc[i, "Video Musical"] # Obtenemos si la canción tiene video musical (True/False) de la columna "Video Musical" del df_discografia
  
            if str(tiene_video).lower()== "true":  # Con esta condicional verificamos si sí tiene video. Convertimos a minuscula el contenido de la variable tiene_video para que coincida con "true"
                nombre = df_discografia.loc[i, "titulo"] # Accede al valor de la columna "titulo" en la fila i y guarda el nombre de la cancion
                album= df_discografia.loc[i, "Álbum"] # Accede al valor de la columna "Álbum" en la fila i y guarda el nombre del album al que pertenece
                link_mv = df_discografia.loc[i, "Link_mv"] # Guarda el link del video musical con la misma dinamica
                fotografia_lugar= df_discografia.loc[i, "Fotografía_lugar"] # Guarda la fotografía del lugar
                bts= df_discografia.loc[i, "BTS"] # Y guarda el link del Behind The Scenes
                
                if busqueda in nombre.lower(): # Comprobamos si el nombre buscado está en el título de la canción
                    st.subheader(f"{nombre}")  # Mostramos el nombre de la canción como subtítulo
                    st.markdown(f"<em>➻Del album {album}</em>", unsafe_allow_html=True) # Mostramos el álbum al que pertenece en cursiva 
                    st.video(link_mv) # Mostramos el videoclip
                    if pd.notna(fotografia_lugar): # Con pd.notna verificamos que haya contenido en la variable fotografia_lugar. Si hay fotografía del lugar, se muestra como imagen
                        st.image(fotografia_lugar, caption="📸 Lugar de grabación", use_container_width=True) # Agregamos un pequeño caption debajo de la fotografía

                    if pd.notna(bts): # Si hay detrás de cámaras (BTS), también se muestra el video
                        st.markdown("🎬 **Behind the scenes:**")
                        st.video(bts)
                    encontrado = True # Activa la variable booleana para marcar que sí hubo un resultado

        # Si no se encontró ninguna canción que cumpla con los filtros...
        if not encontrado: # Presentará un mensaje con formato de advertencia.
            st.warning("😢 Esta canción no tiene video musical. Intenta con una que aparezca en el mapa.")
    #AQUI TERMINA EL CONTENIDO DE LA PAGINA 3

elif pagina_seleccionada==  "♡ Original vs Taylor's Version": # Si en el desplegable la página elegida es "♡ Original vs Taylor's Version" se muestra este contenido:
     
    # Agregamos un título centrado, con una parte en cursiva y otra a color , como las anteriores.
    st.markdown("<h1 style='text-align: center;'><em>ORIGINAL</em> <span style='color: #9A717B;'>vs</span> <span style='color: #d8a7b1;'>TAYLOR'S VERSION</span></h1>", unsafe_allow_html=True)
    # Subtítulo para indicar que se debe seleccionar una era a comparar
    st.subheader("🌷 Elige la era a comparar:")

    # Inicializamos la variable que almacenará la era seleccionada
    era_seleccionada = None
    # Dividimos la interfaz en 4 columnas para colocar los botones de selección
    col1, col2, col3, col4 = st.columns(4)

    # Cada botón representa una era-> la cual tiene un álbum de versión original y otro álbum de versión regrabada.
    # Si se presiona el botón, se guarda su valor en 'era_seleccionada'
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
    
    # Ahora vamos a preparar los datos que se presentarán en la comparación
    
    # Para que la comparación sea más visual en la primera parte se presenta el nombre de los álbumes a comparar y la imagen de sus portadas    
    # Recuperamos listas que ya se usaron en la primera página
    # LISTA DE ALBUMES
    lista_albumes= list(df_discografia["Álbum"].unique())
    lista_albumes.remove("single")
    # PORTADAS DE LOS ALBUMES
    portadas_albumes= list(df_discografia["Link_portada"].unique()) 
    portadas_albumes= portadas_albumes[0:15] 
    
    # Creamos un nuevo DataFrame con columnas 'Álbum' y 'Link_portada' para emparejar cada álbum con su imagen, utilizando las listas anteriores
    df_albumes_portadas = pd.DataFrame({
        "Álbum": lista_albumes, # La lista_albumes será la columna "Álbum"
        "Link_portada": portadas_albumes # Y la lista portada_albumes la columna "Link_portada"
    })
    
    # Presentamos el nombre del album y su portada
    # Verificamos que se haya seleccionado una era antes de continuar. Si la variable era_seleccionada no es None:
    if era_seleccionada is not None:
        col1, col2 = st.columns([1, 1])  # Dividimos la sección en dos columnas: ambos con el mismo espacio 1-1
        for _,fila in df_albumes_portadas.iterrows(): # Con un bucle for recorremos cada fila del df_albumes_portadas
            album= str(fila["Álbum"]).strip().lower() # Obtenemos el nombre del álbum en minúsculas y sin espacios para facilitar la comparación
            portada= fila["Link_portada"] # Obtenemos el link de la portada del álbum
            if era_seleccionada.lower() == album: # Si el nombre del álbum coincide con la era seleccionada (caso versión original)
                with col1: # La versión original ocupará la columna 1
                    # Mostramos el nombre de la era en cursiva, alineado a la izquierda
                    st.markdown(f""" 
                    <div style='text-align: center;'> 
                        <h3><em>{era_seleccionada}</em></h3>
                        <img src="{portada}" width="250">
                    </div>
                """, unsafe_allow_html=True)
                
            elif f"{era_seleccionada} (Taylor's Version)".lower() == album: # Con elif verificamos si el nombre del álbum coincide con la versión Taylor's Version  
                with col2: # La versión regrabada irá en la columna 2
                    # Mostramos el nombre de la versión regrabada, centrado y sin cursiva
                    st.markdown(f""" 
                    <div style='text-align: center;'>
                        <h3>{era_seleccionada} (Taylor's Version)</h3>
                        <img src="{portada}" width="250">
                    </div>
                """, unsafe_allow_html=True)


    # La segunda parte de la comparación presenta los gráficos comparativos de las reproducciones aproximadas en Spotify
    # Diseñaremos un código que nos permita generar los gráficos según cambie la elección del usuario
    if era_seleccionada is not None: # Verificamos que sí se haya elegido una era
        # Creamos una lista vacía para guardar las filas del DataFrame que coincidan con la era seleccionada
        filas_filtradas = []
        for i, fila in df_discografia.iterrows(): # Recorremos cada fila del df_discografia
            album= str(fila["Álbum"]).strip() # Bajo la variable album obtenemos el nombre del álbum sin espacios extras y en str para evitar confusiones pues uno de los álbumes se llama 1989
            if album == era_seleccionada or album== f"{era_seleccionada} (Taylor's Version)": # Si el álbum coincide con la era original o con la versión Taylor's Version...
                filas_filtradas.append(fila) # Agregamos esa fila a la lista filtrada
        
        # Creamos un nuevo DataFrame solo con las filas correspondientes a la era seleccionada
        df_era_seleccionada = pd.DataFrame(filas_filtradas)
    
        # HASTA AQUÍ: Ya tenemos el DataFrame separado por era (original y TV)
        # Creamos listas vacías para clasificar canciones y sus reproducciones 
        canciones_originales = [] # Canciones del álbum original
        canciones_regrabadas = [] # Canciones regrabadas (TV)
        reproducciones_originales = [] # Reproducciones de las originales
        reproducciones_regrabadas = [] # Reproducciones de las regrabadas
        canciones_vault = [] # Canciones "from the vault" (inéditas)  incluidas en el TV
        reproducciones_vault = [] # Reproducciones del vault

        # Recorremos cada fila (.iterrows()) del DataFrame de la era seleccionada
        for _, fila in df_era_seleccionada.iterrows():
            titulo = str(fila['titulo']).strip() # Obtenemos el título de la canción sin espacios extra y como string (canciones como 22)
            album = str(fila['Álbum']).strip() # Obtenemos el nombre del álbum sin espacios extra y como string (album como 1989)
            reproducciones = int(fila['Reproducciones en Spotify']) # Obtenemos reproducciones convertidas a número entero int

            if album == era_seleccionada: # Si el album al que pertenece esa canción es de la versión original...
                canciones_originales.append(titulo) # Añadimos el nombre de la canciones a la lista de originales
                reproducciones_originales.append(reproducciones) # También añadimos sus reproducciones a las originales
            elif album == f"{era_seleccionada} (Taylor's Version)": # Si esa canción pertenece a la versión Taylor's Version del álbum: haremos dos divisiones más...
                if "(from the vault)" in titulo.lower():  # Si es una canción del vault (contiene "from the vault" en el título)
                    canciones_vault.append(titulo) # Su nombre se va a la lista de vault
                    reproducciones_vault.append(reproducciones) # Y sus reproducciones a la lista de vault también
                else: # Si no es vault, entonces es una canción regrabada
                    canciones_regrabadas.append(titulo)  # Su nombre a la lista de regrabadas
                    reproducciones_regrabadas.append(reproducciones) # Y sus reproducciones a la lista de regrabadas

        # PASAMOS LOS DATOS A DATAFRAMES NUEVOS PARA CONSTRUIR EL GRÁFICO
        df_version_original= pd.DataFrame({'Canciones_og': canciones_originales, 'Reproducciones_og': reproducciones_originales}) # Creamos un DataFrame con las canciones originales y sus reproducciones
        df_version_regrabada= pd.DataFrame({'Canciones_tv': canciones_regrabadas, 'Reproducciones_tv': reproducciones_regrabadas}) # Creamos un DataFrame con las canciones regrabadas (Taylor's Version) y sus reproducciones tambien
        df_vault= pd.DataFrame({'Canciones_ftv': canciones_vault, 'Reproducciones_ftv': reproducciones_vault}) # Por último, creamos un DataFrame con las canciones inéditas  "From The Vault" junto a sus reproducciones

        # LIMPIAMOS LOS DATAFRAMES PARA COMBINARLOS CORRECTAMENTE
        
        # En el df_version regrabada creamos una nueva columnas llamada "Canciones_og", tomando base la columna existente "Canciones_tv" pero quitando la parte " (Taylor's Version)" de los títulos 
        df_version_regrabada["Canciones_og"] = df_version_regrabada["Canciones_tv"].str.replace(" \(Taylor's Version\)", "", regex=True)
        # En las canciones del vault, eliminamos ambas etiquetas: " (Taylor's Version)" y " (From The Vault)"
        df_vault["Canciones_ftv"] = df_vault["Canciones_ftv"].str.replace(" \(Taylor's Version\)", "", regex=True).replace(" \(From The Vault\)", "", regex=True)
        # Luego nos aseguramos de eliminar espacios sobrantes en los titulos de las canciones que podrían dificultar su combinación a continuación
        df_version_original["Canciones_og"] = df_version_original["Canciones_og"].astype(str).str.strip()
        df_version_regrabada["Canciones_og"] = df_version_regrabada["Canciones_og"].astype(str).str.strip()

        # COMBINAMOS LOS DOS DATAFRAMES DE LAS VERSIONES ORIGINALS Y REGRABADAS
        df_comparacion = pd.merge( # Usamos la función pd.merge de pandas que unirá los dfs
            df_version_original, # Este será el df base 
            df_version_regrabada[['Canciones_og', 'Reproducciones_tv']], # Aqui seleccionamos dos columnas del df_versión_regrabada que emplearemos, la Canciones_og que tiene los nombres sin (Taylor's Version)-> que permitirá coincidir los datos, y la columna de Reproducciones_tv
            on='Canciones_og' # Con esto le indicamos que la columna común para coincidir los datos será Canciones_og
        )

        # AHORA SI PODEMOS CREAR LOS GRAFICOS CON PLOTLY EXPRESS

        # Iniciamos con el grafico comparativo de reproducciones del album original y del album regrabado
        # Creamos una variable que contenga una lista de canciones que serán las etiquetas del eje X        
        canciones = df_comparacion['Canciones_og']

        # Colocamos en otras dos variables las reproducciones de la versión original y de la versión regrabada, estas serán las barras dobles que irán juntas por canción 
        reproducciones_og = df_comparacion['Reproducciones_og']
        reproducciones_tv = df_comparacion['Reproducciones_tv']

        # Creamos un diccionario de colores para cada era, diferenciando original y Taylor's Version, y así los colroes del grafico vaya variando
        colores_eras = {
            "Fearless": {
                "original": "#d6b751", 
                "tv": "#8a6434"         
            },
            "Speak Now": {
                "original": "#b495c8",  
                "tv": "#5d3a73"         
            },
            "Red": {
                "original": "#e63946",  
                "tv": "#a4161a"         
            },
            "1989": {
                "original": "#add8e6",  
                "tv": "#2f8dd9"         
            }
        }

        # Creamos el gráfico
        fig = go.Figure()

        # Ahora añadimos la primera barra: que será la versión original
        fig.add_trace(go.Bar(
            x=canciones,  # Llamamos a la variable canciones que creamos al inicio para que sean las barras del eje x
            y=reproducciones_og,   # llamamos a la variable reproduciones_og que serán los valores en el eje y
            name='Versión original',  # Este nombre nos guiará en la leyenda: le ponemos la etiqueta Versión original
            marker_color=colores_eras[era_seleccionada]["original"]  #Le ponemos un color diferenciador desde el diccionario de colores creado, tomando el correspondiente a la versión original
        ))

        # Ahora añadimos la segunda barra: que será la versión regrabada (Taylor's Version)
        fig.add_trace(go.Bar(
            x=canciones,  # La misma variable para el eje x
            y=reproducciones_tv, # Pero ahora colocamos en el eje y las reproduccciones de la version regrabada: reproducciones_tv
            name= "Taylor's Version", # El nombre que nos guiará en la leyenda será Taylor's Version
            marker_color=colores_eras[era_seleccionada]["tv"] # Le ponemos un color diferenciador desde el diccionario, tomando el correspondiente a la versión tv
        ))

        # Ajustamos el diseño del gráfico
        fig.update_layout(
            title=(f"🌟 Comparación de reproducciones: {era_seleccionada} vs {era_seleccionada} (Taylor's Version)"), # Le ponemos un titulo
            xaxis_title="Canción", # título del eje X
            yaxis_title="Reproducciones en Spotify", # título del eje Y
            barmode='group', # el modo de visualización: barras agrupadas
            xaxis_tickangle=-45, # la inclinación de las etiquetas del eje X
            template='plotly_white', # un fondo blanco
            legend_title_text='Versión',  # el título de la leyenda
            height=600 # y por último le damos un tamaño de 600 pixeles
        )

        # Mostrar el gráfico
        st.plotly_chart(fig, use_container_width=True)

        # Continuamos con el segundo gráfico: Reproducciones de las canciones "From the vault"
        # Usaremos esta libreria que importamos al inicio import plotly.graph_objects as go 

        fig = px.bar( 
            df_vault,# Usamos el DataFrame que contiene solo las canciones inéditas: from the vault
            x="Canciones_ftv", # El eje X será el nombres de las canciones del vault
            y="Reproducciones_ftv",  # El eje Y será el número de reproducciones en Spotify de esas canciones
            title=f"🌟 Reproducciones de las canciones 'From The Vault' de {era_seleccionada}", # Le ponemos un titulo que ira cambiando según la era seleccionada
            labels={"Canciones_ftv": "Canción", "Reproducciones_ftv": "Reproducciones en Spotify"}, # Etiquetas para los ejes
            color_discrete_sequence=[colores_eras[era_seleccionada]["tv"]]  # Color de las barras según la era en su versión regrabada que tomaremos desde el diccionario de colores que creamos

        )
        # Ajustamos detalles de diseño del gráfico
        fig.update_layout(
            title_font_size=24, # El tamaño del título del gráfico
            xaxis_tickangle=-45  # Inclinamos las etiquetas del eje X para que no se sobrepongan
        )
        # Mostramos el grafico
        st.plotly_chart(fig, use_container_width=True)
    #AQUI TERMINA EL CONTENIDO DE LA PAGINA 4

else: # Como última opcion, sino se eligió ninguna de las páginas anteriores, la unica restante es "♡ Conoce a Taylor"
    
    st.title("🌟🎤 Bienvenid@ al Juego del Ahorcado (Taylor's Version) 🎤🌟") # Colocamos un título de bienvenida

    # Traemos la LISTA DE ALBUMES que ya habiamos empleado
    lista_albumes= list(df_discografia["Álbum"].unique())
    lista_albumes.remove("single") # Quitamos los singles de la lista, para solo jugar con los nombres de los álbumes=eras
    # Selecionamos solo los albumes de nombre unico, es decir no tomaremos en cuenta los (Taylor's Version) pues llevan el mismo nombre
    albumes_juego= lista_albumes[0:11]

    albumes_minuscula = []  # Lista donde almacenaremos los álbumes en minúsculas y sin espacios

    for album in albumes_juego: # Con un bucle for iteramos por todos los albumes en la lista albumes_juego
        album_minuscula = str(album).lower().strip().replace(" ", "") # Tratando todo los albumes como string convertimos a minúscula, quitamos espacios antes y despues, y con replace() tambien los espacios dentro del nombre del album (Por ejemplo: Taylor Swift -> taylorswift)
        albumes_minuscula.append(album_minuscula)  # Lo agregamos a la nueva lista
    
    # INICIALIZAMOS VARIABLES DE SESIÓN. 
    # Utilizaremos st.session_state-> que nos permitirá guardas datos entre interacciones que el usuario vaya haciendo en el usuario. Esto nos permitirá ejecutar el juego correctamente.
    if "palabra_secreta" not in st.session_state: # Verifica si ya existe una palabra secreta guardada. Si no hay...
        st.session_state.palabra_secreta = random.choice(albumes_minuscula) # Con random.choice, selecciona una era secreta aleatoriamente de la lista albumes_minuscula
        st.session_state.letras_adivinadas = [] # Crea una lista vacia que irá guardando las letras que el usuario va adivinando
        st.session_state.intentos = 0 # Se define que al iniciar el juego los intentos del usuario son todavia 0
        st.session_state.intentos_maximos = 5 # Establece que los intentos máximos son 5
        st.session_state.terminado = False # Esto marca que el juego todavia no ha terminado
    
    # Traemos los valores creados con st.session_state y los iremos guardando el varibales para facilitar usarlos en el codigo. 
    palabra = st.session_state.palabra_secreta  # aqui guardamos la palabra secreta
    letras_adivinadas = st.session_state.letras_adivinadas # aqui las letras adivinidas
    intentos = st.session_state.intentos # aqui el numero de intentos
    intentos_maximos = st.session_state.intentos_maximos # y aqui los intentos maximos

    progreso = "" # Con esta variable se irá mostrando el progreso: vaya adivinando una letra o todavia le falte
    for letra in palabra: # Este bucle for recorre cada letra de la palabra secreta
        if letra in letras_adivinadas: # Con if verifica si la letra ya fue adivinada: esta en la lista de letras_adivinadas 
            progreso += f"{letra} " # Si adivinó la letra, la va completando en la palabra secreta
        else:
            progreso += "_ "  # Si no la adivino, deja el espacio en _
    # Con st.markdown se muestra 1) primero cuantas letras tiene la palabra (len()) y cual es su progreso almacenado en la variable "progreso"
    st.markdown(f"🔮 Tu era misteriosa tiene {len(palabra)} letras: {progreso.strip()}")

    # Input para el jugador
    if not st.session_state.terminado: # Si el juego aún NO ha terminado...
        intento = st.text_input("Adivina una letra:", max_chars=1).lower() # Se muestra un input de texto para que el usuario vaya agregando letras, las cuales las pasando a minuscula y así puedan coincidir con la palabra

        if intento: # Si se ingresó algo en el input...
            if len(intento) != 1: # Si la cantidad de letras del intento es diferente de 1...
                st.warning("🚫 Ingresa solo UNA letra.") # da un mensaje en formato advertencia 
            elif intento in letras_adivinadas: # Si el intento ya está en las letras adivinadas...
                st.info("🔁 Ya intentaste con esa letra.") # da este mensaje
            else:  # Agrega la letra a letras_adivinadas, sea correcta o no
                letras_adivinadas.append(intento)

                if intento in palabra: # Si el intento si estaba en la palabra se da un mensaje de felicitaciones
                    st.success("🎯 ¡Sí! Esa letra está en la era.")
                else: # Si el intento no estaba en la palabra...
                    st.session_state.intentos += 1 # se aumenta uno a la variable intentos
                    st.error(f"💔 Letra incorrecta. Te quedan {intentos_maximos - st.session_state.intentos} intento(s)...") # y se da un mensaje informando cuantos intentos quedan

        # Verificamos si ganó
        if all(letra in letras_adivinadas for letra in palabra): # Si están todas las letras de la palabra secreta...
            st.balloons() # con st.ballons se lanzan globos
            st.success(f"🎉 ¡Felicidades, Swiftie! Adivinaste la era secreta: {palabra.upper()} 🎉") # se da un mensaje de felicitaciones
            st.markdown("""<div style="text-align: center;"><img src="https://i.pinimg.com/originals/c7/00/fb/c700fb31450511f5b5dd1e3739fc486e.gif" width="300"></div>""",unsafe_allow_html=True) # y agregamos un gif        
            st.session_state.terminado = True # por ultimo, marcamos el juego como terminado

        # Verificamos si perdió
        if st.session_state.intentos >= intentos_maximos: # Si el número de intentos es mayor igual al numero de intentos maximos...
            st.error(f"☠️ Se acabaron los intentos. La era secreta era: {palabra.upper()}") # se da un mensaje de derrota y se informa cual era la palabra secreta
            st.markdown("""<div style="text-align: center;"><img src="https://media.tenor.com/9NceTmMh1_AAAAAM/girl-woman.gif" width="300"></div>""",unsafe_allow_html=True) # agregamos un gif
            st.session_state.terminado = True # y el juego se marca como terminado 

    # Por último, se entrega un mensaje final, según la era secreta
    if st.session_state.terminado: # Si el juego terminó
        mensajes_eras = { # Creamos un diccionario con un mensaje por cada era
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

        st.markdown("📝 Mensaje especial de la era:") # Un texto que señale el mensaje
        # Y con formato de información (azul), se obtiene el mensaje del diccionario, dependiendo de la palabra secreta
        st.info(mensajes_eras.get(palabra))
        
        # Finalmente, añadimos un botón para reiniciar
        if st.button("🔄 Jugar otra vez"):
            for key in ["palabra_secreta", "letras_adivinadas", "intentos", "terminado"]:
                del st.session_state[key]# Esto borra todos los datos almacenados en la variables y el juego vuelve a iniciar.
                #AQUI TERMINA EL CONTENIDO DE LA PAGINA 5
            
