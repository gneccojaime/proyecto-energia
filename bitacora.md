# Bitácora de Prompts y Comandos - Proyecto Final
**Materia:** Fundamentos de Programación e IA  
**Profesor:** Alex  

---

## Registro de Prompts

### Prompt 1
- **Fecha y Hora:** 2026-11-19 17:08:05
- **Texto original:**
```text
Hola, dile hola al mundo. Nuestro equipo ocupandote a ti como recurso vamos a trabajar en nuestro proyecto final de la materia de Fundamentos De Programacion e ia, saluda al profe Alex. La ia no tendra la ultima palabra antes de hacer algo pregunta. Sigue todas nuestras indicaciones y rublicas que te compartasmos ya que en base a eso se nos va a calificar. Recuerda que estamos empezando en esto. Guarda todos nuestros comandos o prompts tal y como se te envie en una bitacora.md, luego solo dejaremos los mas importantes. Estamos emocionados de trabajar juntos.
```

### Prompt 2
- **Fecha y Hora:** 2026-11-19 17:10:17
- **Texto original:**
```text
# Prompt: Proyecto 1 – Mapa de calor del consumo de un edificio

Vamos a construir el Proyecto 1 "Mapa de calor del consumo de un edificio" para la clase de Fundamentos de Programación de Ingeniería Energética. Un edificio registra el consumo (kWh) de cada hora durante 7 días, y el administrador de un edificio o campus necesita ver cuándo se gasta más energía y detectar horas anormales para actuar. La app debe quedar publicada en una página web.

## Regla de trabajo (la más importante)

Tú no tienes la última palabra: yo decido. Antes de crear, modificar o borrar un archivo, instalar algo o tomar una decisión de diseño, explícame qué vas a hacer y espera mi aprobación. Si algo es ambiguo, pregúntame en vez de asumir. Trabaja por etapas y no pases a la siguiente sin mi OK.

## Tecnología

- Python con Streamlit. La lógica va en `logica.py` y la interfaz en `app.py`.
- En `logica.py` usa solo lo visto en clase: funciones con return, listas, diccionarios, ciclos, condicionales, variables locales y JSON. Nada de pandas ni numpy en la lógica. Comenta el código en español y usa nombres claros, porque tengo que poder explicarlo.
- Para dibujar los gráficos, propónme una librería (Plotly, Altair u otra) y dime por qué. No agregues ninguna sin avisarme. Todas las dependencias van en `requirements.txt`.

## Estructura de la carpeta

`app.py`, `logica.py`, `requirements.txt`, `README.md`, `test_verificacion.py`, `datos/entrada.json`, `datos/salida.json`.

Usa rutas relativas para que funcione igual en mi computador y en el servidor.

## Datos de entrada (`datos/entrada.json`)

La app carga este archivo al iniciar y debe permitir cargar otro con la misma estructura. Estructura exacta:

```json
{
  "edificio": "Bloque A",
  "tarifa": 850,
  "consumo": [
    [1.2, 1.1, 1.0, "... 24 valores, uno por hora"],
    "... 7 filas en total"
  ]
}
```

- `"consumo"` es la matriz: cada fila es un día (fila 0 = Lunes ... fila 6 = Domingo) y cada columna es una hora (columna 0 = 0:00 ... columna 23 = 23:00). Valores en kWh.
- `"tarifa"` es el precio por kWh (850).
- Crea un `entrada.json` de ejemplo con datos realistas (bajo de madrugada, alto en horas laborales, un par de horas anormales).
- Al cargar un archivo, valida que tenga las tres claves, 7 filas, 24 valores por fila y solo números, y muestra un mensaje claro si falla.
- Las funciones de cálculo deben funcionar con CUALQUIER tamaño de matriz (no escribas 7 y 24 fijos), porque el caso de verificación usa 3×4. La validación de 7×24 va solo al cargar el archivo.

## Datos de salida (`datos/salida.json`)

Guarda el resumen con esta estructura:

```json
{
  "edificio": "Bloque A",
  "total_semana": 0.0,
  "total_por_dia": ["7 valores"],
  "promedio_por_hora": ["24 valores"],
  "pico": {"dia": 0, "hora": 0, "valor": 0.0},
  "umbral": {
    "valor_kwh": 0.0,
    "cantidad": 0,
    "horas_sobre_umbral": [{"dia": 0, "hora": 0, "valor": 0.0}]
  },
  "proyeccion": {
    "ahorro_porcentaje": 10,
    "factor": 0.9,
    "consumo_proyectado": ["matriz del mismo tamaño que la original"],
    "total_proyectado": 0.0,
    "ahorro_kwh": 0.0
  },
  "hora_mas_cara_por_dia": [{"dia": 0, "hora": 0, "kwh": 0.0, "costo": 0.0}]
}
```

- En la lógica, `"dia"` y `"hora"` son índices desde 0. La interfaz los traduce a nombre del día (Lunes...) y hora 0–23.
- `"costo"` = kwh × tarifa.

## Funcionalidad obligatoria (`logica.py`)

1. Cargar la matriz de consumo (7 días × 24 horas) desde un archivo .json.
2. Calcular el total por día y el promedio por hora.
3. Encontrar el pico de la semana (día, hora y valor) y las horas que superan un umbral elegido por el usuario.
4. Proyectar un escenario de ahorro (por ejemplo -10 %) sin perder los datos originales, y guardar el resumen en `datos/salida.json`.

Las funciones devuelven diccionarios y listas con las mismas claves que `salida.json` (por ejemplo, la función del pico devuelve `{"dia", "hora", "valor"}`), de modo que guardar el resumen sea armar un diccionario y usar `json.dump`. Antes de escribir cada función, dime su nombre, parámetros y qué devuelve, y espera mi OK.

## Visualizaciones obligatorias

### 1. Mapa de calor 7×24

- Cuadrícula de 7 filas (días) × 24 columnas (horas); cada celda con un color según el consumo (azul = bajo, rojo = alto).
- Ejes rotulados (Lunes a Domingo y 0 a 23 horas) y leyenda de la escala de color.
- Al pasar el cursor sobre una celda aparece el valor exacto en kWh.

### 2. Tarjetas de total, pico y promedio

- Tres tarjetas grandes: consumo total de la semana, pico (día, hora y kWh) y la hora con mayor promedio.
- Debajo, barras pequeñas con el total de cada día.
- Todo se actualiza cuando se cambia el archivo o se corrige un dato.

### 3. Umbral que resalta celdas

- Deslizador de umbral (kWh): las celdas que lo superan se resaltan con borde o color distinto.
- Un contador dice cuántas horas lo superan y una lista muestra día y hora.
- Con un umbral muy alto aparece el mensaje "Ninguna hora supera el umbral".

## Controles adicionales de la interfaz

- **Corregir un dato:** el usuario puede editar el valor de una celda (por ejemplo con una tabla editable) y todo se recalcula al instante, sin tocar la matriz original del archivo.
- **Porcentaje de ahorro:** deslizador (por ejemplo de 0 % a 50 %, con -10 % por defecto) que alimenta la proyección. Muestra el total original frente al proyectado; el original nunca cambia.

## Diseño (es un proyecto de DISEÑO)

- Prioriza que se vea profesional, con jerarquía clara: se entiende qué es lo más importante con solo mirar la pantalla.
- Colores con significado (no decorativos) y tema claro/oscuro.
- Textos y números legibles en proyector.
- Los controles responden al instante y no hay errores visuales ni textos cortados.

## Reto funcional

Marcar en el mapa la hora más cara de cada día.

## Caso de verificación (la app debe dar exactamente esto)

Matriz de 3 días × 4 horas: `[[1, 2, 3, 4], [5, 6, 7, 8], [2, 2, 2, 2]]`

- Total por día: 10, 26 y 8 kWh.
- Promedios (por hora): 2.67, 3.33, 4.00 y 4.67 kWh.
- Pico: día 2, hora 4, 8 kWh.
- Umbral 5 kWh: 3 celdas (día 2, horas 2, 3 y 4, con valores 6, 7 y 8).
- Umbral 100 kWh: ninguna celda.
- Proyección ×0.5: el día 2 queda 2.5, 3.0, 3.5 y 4.0, y los datos originales no cambian.

Estos resultados se verificaron con una solución de referencia: si la app da otros, hay un error de lógica.

El enunciado cuenta días y horas desde 1 en este caso, mientras que en la lógica los índices van desde 0: en el test compara índice + 1. Si la interfaz muestra algo distinto para el caso 3×4, consúltame antes de cambiarlo.

Escribe `test_verificacion.py` que compruebe todo esto y ejecútalo antes de entregarme cada etapa.

## Publicación en una página

- Prepara el proyecto para publicarlo en Streamlit Community Cloud: `requirements.txt` completo y rutas relativas.
- En el README explícame paso a paso cómo ejecutarlo en local y cómo subirlo (repositorio en GitHub y despliegue), sin dar nada por sabido.

## Entrega

La carpeta del proyecto ejecutable, con todo el código y `datos/` (entrada y salida en JSON).

---

Empieza proponiéndome un plan por etapas, con las preguntas que tengas, y no escribas código hasta que yo lo apruebe.

añade ala app tambien un apartado con los casos de prueba
```

### Prompt 3
- **Fecha y Hora:** 2026-11-19 17:13:04
- **Texto original:**
```text
Haz una barra lateral, donde podamos elegir entre nuestro administrador y los casos de prueba de nuestro profesor, vamos con la estapa 1. Me parece bien que uses a plothy con streamlit.
```

### Prompt 4
- **Fecha y Hora:** 2026-11-19 17:15:24
- **Texto original:**
```text
OK, continuemos con la etapa 2
```

### Prompt 5
- **Fecha y Hora:** 2026-11-19 17:18:17
- **Texto original:**
```text
SI, por favor no uses emojis.
```

### Prompt 6
- **Fecha y Hora:** 2026-11-19 17:20:55
- **Texto original:**
```text
Si
```

### Prompt 7
- **Fecha y Hora:** 2026-11-19 17:26:26
- **Texto original:**
```text
Si, ahora vamos a revisar y ver que erorres cometiste, que te falto y que vamos a mejorar. Espera el llamado.
```

### Prompt 8
- **Fecha y Hora:** 2026-11-19 17:44:20
- **Texto original:**
```text
La barra lateral mantenla
Gran acierto con la selección del tema.
Se ve demasiado crudo, no terminada de convencer entendemos que es una primera versión, en lógica fue un gran acierto, vamos a mejorar el apartado del diseño. para un tema oscuro nos gustaría elegirlo, con un sol, y que en el titulo donde dice gestión energética añade un fondo de día sencillo, usa un difuminado, para el fondo claro usa azul claro, amarrillo y verde, obviamente el fondo del cielo es mas claro que el del fondo, con el fondo blanco la barra lateral es blanca. Ahora el tema oscuro, la parte superior igual un  cielo estrellado de noche con la luna, y el fondo de todo el programa será un azul oscuro, recuerda el rojo cuando el consumo es alto, la barra lateral es de color negro al usar el tema oscuro. usa bordes redondeados. A cada item separaalo con un rectángulo con bordes redondedados de un tono diferente al de fondo, sigue siendo azul, donde dice esdificio seleccionado: bloque A igual una referecia visual de un edificion sencillo.
```

### Prompt 9
- **Fecha y Hora:** 2026-11-19 17:45:13
- **Texto original:**
```text
ok
```

### Prompt 10
- **Fecha y Hora:** 2026-11-19 18:09:20
- **Texto original:**
```text
Nos gusto mucho esta nueva versión, sigue viendo muy plana, el  panel de admistrador esta muy bueno, hay unas cositas al usar el modo oscuro
 donde esta parámetros de control en la ventana lateral
el cuadarado que adentro tiene upload, y 200MB per file • JSON, no cambia y se ve muy mal
la parte superior en los dos modos se ve blanca y al usar el modo oscuro se ve terrible, cambia el icono del edificio, quitalo de hay y ubicalo en el apartado del cielo de noche y dia, ósea que se vea en el paisaje. En la tabla Deteccion de Horas Criticas sobre el Umbral, usa bordes redondeados, al usar el modo oscuro no se ve ningún dato en la tabla. en el apartado de correcion de datos en vivo, en el botón de restablecer a valores predeterminados no y se ve ni tampoco el de guardar reporte actual en datos/salida. json no ser ve al usar el tema oscuro. tampoco al usar el casos de prueba la tabla al usar el modo oscuro no se ve , ni el botón de ejecutar, ni tampoco la tabla de verificación se ve al usar el tema oscuro, la barra lateral también mejorala, los ítems dentro de rectángulos con bordes redondos y un pequeña referencia visual de un sol y luna sencillo al elegir el tema, en navegación una referencia visual de un panel de administración y en casos de prueba pues una lupa. en la parte superior derecha al usar los 3 puntos y cambiar el tema daña todo el diseño de la pagina con los colores arregla eso que sea un solo panel para elegir el tema
```

### Prompt 11
- **Fecha y Hora:** 2026-11-19 18:10:34
- **Texto original:**
```text
ok empieza
```

### Prompt 12
- **Fecha y Hora:** 2026-11-19 18:37:11
- **Texto original:**
```text
e ve mejor pero hay demasiados errores. Al tener activado el tema oscuro. En la barra lateral. En el apartado de APARIENCIA VISUAL. En tema oscuro se ve (Noche-Luna) y no un visual de la luna, en tema claro igual aparece (Dia-Noche) y no un visual. En NAVEGACION, en el botón de administrador de edificio aparece[Panel] y no un visual. en casos de prueba aparece[lupa] y no un visual.
Ahora al usar el tema claro igual, en el cuadrado para Cargar archivo JSON (7x24) su fondo sigue negro y no cambia al elegir otro tema
 en el apartado de pruebas  debajo del titulo igual código y no un visual.
la tabla Auditoria y Verificacion de Resultados Oficiales se ve bien

 
al usar el tema claro
En el panel administrativo debajo del titulo se ve es código y no el visual del cielo con el edificio

Indicadores Clave de Demanda Energetica
se ve bien
y el resto del panel administrativo al usar el tema oscuro se ve bien

ahora el panel administrativo al usar el tema claro

debajo del titulo
Gestion Energetica: Mapa de Calor del Consumo 
Monitoreo continuo de demanda electrica, deteccion de anomalias horarias y proyeccion de eficiencia

se ve un código no un visual
en ndicadores Clave de Demanda Energetica
el item miércoles alas 14:00 no cambia al tema claro
ni tampoco el item demanada media ala 14:00 no cambia a tema claro

en Simulacion de Eficiencia y Proyeccion de Ahorro (10%)
el item -196,43kwh(10%) no cambia a l tema claro y el item -$165,265.50cop no cambia al tema claro 

en Correccion de Datos en Vivo

la tabla no cambia a tema claro Se ve mejor pero hay demasiados errores. Al tener activado el tema oscuro. En la barra lateral. En el apartado de APARIENCIA VISUAL. En tema oscuro se ve (Noche-Luna) y no un visual de la luna, en tema claro igual aparece (Dia-Noche) y no un visual. En NAVEGACION, en el botón de administrador de edificio aparece[Panel] y no un visual. en casos de prueba aparece[lupa] y no un visual.
Ahora al usar el tema claro igual, en el cuadrado para Cargar archivo JSON (7x24) su fondo sigue negro y no cambia al elegir otro tema
 en el apartado de pruebas  debajo del titulo igual código y no un visual.
la tabla Auditoria y Verificacion de Resultados Oficiales se ve bien

 
al usar el tema claro
En el panel administrativo debajo del titulo se ve es código y no el visual del cielo con el edificio

Indicadores Clave de Demanda Energetica
se ve bien
y el resto del panel administrativo al usar el tema oscuro se ve bien

ahora el panel administrativo al usar el tema claro

debajo del titulo
Gestion Energetica: Mapa de Calor del Consumo 
Monitoreo continuo de demanda electrica, deteccion de anomalias horarias y proyeccion de eficiencia

se ve un código no un visual
en ndicadores Clave de Demanda Energetica
el item miércoles alas 14:00 no cambia al tema claro
ni tampoco el item demanada media ala 14:00 no cambia a tema claro

en Simulacion de Eficiencia y Proyeccion de Ahorro (10%)
el item -196,43kwh(10%) no cambia a l tema claro y el item -$165,265.50cop no cambia al tema claro 

en Correccion de Datos en Vivo

la tabla no cambia a tema claro debajo del titulo hay código y no un visual

en el apartado de pruebas al usar el tema claro

en el apartado de pruebas al usar el tema claroS
```

### Prompt 13
- **Fecha y Hora:** 2026-11-19 18:38:16
- **Texto original:**
```text
si
```

### Prompt 14
- **Fecha y Hora:** 2026-11-19 18:57:40
- **Texto original:**
```text
todo esta guardado?, puedo cerrar visual?
```

### Prompt 15
- **Fecha y Hora:** 2026-11-23 17:35:24
- **Texto original:**
```text
AL usar el modo claro. En el apartado de panel administrativo, todo se ve muy bien, elimina la barra roja que esta debajo del mapa de calor, no se que significa eso. Al usar el tema oscuro todo se ve muy bien, en el panel administrativo, en la barra lateral donde dice parámetros de control al usar el tena oscuro el cuadrado donde se dice upload y 200MB per file . JSON, no cambia en consideración del tema oscuro
```
