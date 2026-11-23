# Proyecto 1: Mapa de Calor del Consumo Energetico de un Edificio

Materia: Fundamentos de Programacion e Inteligencia Artificial  
Carrera: Ingenieria Energetica  
Profesor: Alex  

---

## 1. Descripcion del Proyecto

Esta aplicacion web permite a administradores de edificios y campus universitarios monitorear el consumo de energia electrica (en kWh) registrado cada hora durante una semana completa (7 dias x 24 horas = 168 mediciones).

La herramienta ayuda a:
- Visualizar los patrones de consumo a traves de un mapa de calor interactivo.
- Identificar el pico maximo de demanda semanal (dia, hora y valor).
- Detectar anomalias y horas criticas que superan un umbral configurable.
- Identificar y marcar la hora mas costosa de cada dia segun la tarifa energetica.
- Simular escenarios de ahorro energetico porcentual sin alterar los registros originales.
- Editar valores en tiempo real para evaluar medidas correctivas de forma inmediata.
- Ejecutar y auditar casos de prueba oficiales de la catedra.

---

## 2. Estructura del Repositorio

El proyecto se organiza bajo una estructura modular con rutas relativas:

```text
Jueves_Proyecto_Final/
│
├── app.py                  # Interfaz grafica interactiva con Streamlit y Plotly
├── logica.py               # Modulo de calculos puros en Python (sin pandas/numpy)
├── test_verificacion.py    # Script de pruebas automatizadas del caso 3x4
├── requirements.txt        # Dependencias del proyecto (streamlit, plotly)
├── bitacora.md             # Registro de prompts e instrucciones del proyecto
├── README.md               # Documentacion completa de instalacion y uso
│
└── datos/
    ├── entrada.json        # Matriz de consumo semanal (7x24), tarifa y edificio
    └── salida.json         # Resumen analitico estructurado para exportacion
```

---

## 3. Requisitos Previos

- Python 3.9 o superior instalado en el sistema.
- Gestor de paquetes `pip` actualizado.
- Navegador web moderno (Google Chrome, Firefox, Edge o Safari).

---

## 4. Instalacion y Ejecucion en Entorno Local

Siga estos pasos desde su terminal o linea de comandos:

### Paso 1: Clonar o descargar la carpeta del proyecto
Abra la terminal y navegue hasta la carpeta del proyecto:
```bash
cd Jueves_Proyecto_Final
```

### Paso 2: (Opcional pero recomendado) Crear un entorno virtual
```bash
python -m venv venv
```
Activar en Windows:
```bash
.\venv\Scripts\activate
```
Activar en Linux/macOS:
```bash
source venv/bin/activate
```

### Paso 3: Instalar las dependencias
```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar las pruebas unitarias de verificacion
Antes de iniciar la aplicacion, verifique que la logica cumpla con los resultados de referencia del profesor Alex:
```bash
python test_verificacion.py
```
Debe obtener el mensaje: `>> RESULTADO: TODAS LAS PRUEBAS DEL PROFESOR PASARON CON EXITO! <<`.

### Paso 5: Iniciar la aplicacion web
```bash
streamlit run app.py
```
La aplicacion se abrira automaticamente en su navegador en `http://localhost:8501`.

---

## 5. Guia de Publicacion en la Nube (Streamlit Community Cloud)

Para publicar la aplicacion de manera gratuita y accesible desde cualquier navegador en internet, siga estos pasos:

### Paso 1: Subir el proyecto a GitHub
1. Inicie sesion en [GitHub](https://github.com/) y cree un nuevo repositorio publico (por ejemplo: `proyecto-consumo-edificio`).
2. En su terminal local, inicialice git y suba los archivos:
   ```bash
   git init
   git add .
   git commit -m "Entrega Proyecto 1 - Mapa de Calor de Consumo"
   git branch -M main
   git remote add origin https://github.com/SU_USUARIO/proyecto-consumo-edificio.git
   git push -u origin main
   ```

### Paso 2: Desplegar en Streamlit Community Cloud
1. Ingrese a [share.streamlit.io](https://share.streamlit.io/) e inicie sesion con su cuenta de GitHub.
2. Haga clic en el boton **"New app"**.
3. Complete los siguientes campos:
   - **Repository:** Seleccione su repositorio (`SU_USUARIO/proyecto-consumo-edificio`).
   - **Branch:** `main`.
   - **Main file path:** `app.py`.
4. Haga clic en **"Deploy"**.
5. En un par de minutos la aplicacion estara en linea con una URL publica que podra compartir con el profesor y su equipo.

---

## 6. Verificacion Oficial y Criterios Tecnicos

El archivo `logica.py` fue disenado estrictamente con los conceptos de la clase:
- Funciones modulares con valor de retorno (`return`).
- Estructuras nativas: listas anidadas, diccionarios y tipos basicos.
- Bucles tradicionales (`for`) y sentencias condicionales (`if/elif/else`).
- Manipulacion de archivos con el modulo estandar `json`.
- Cero uso de librerias avanzadas como Pandas o NumPy en la logica.
- Compatibilidad con matrices de cualquier tamano ($N \times M$).
