"""
Aplicacion interactiva en Streamlit: Mapa de calor del consumo de un edificio.
Proyecto 1 - Fundamentos de Programacion e IA.
Diseno profesional con soporte integral y visual de Tema Claro (Dia) y Tema Oscuro (Noche).
"""

import json
import base64
import os
import streamlit as st
import plotly.graph_objects as go
import logica

# Configuracion de pagina de Streamlit
st.set_page_config(
    page_title="Gestion Energetica - Mapa de Calor",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constantes de etiquetas temporales
DIAS_SEMANA = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
HORAS_DIA = [f"{h:02d}:00" for h in range(24)]


def obtener_datos_base():
    """Carga los datos iniciales por defecto desde datos/entrada.json."""
    try:
        return logica.cargar_datos("datos/entrada.json", validar_7x24=True)
    except Exception as error:
        st.error(f"[ERROR] No se pudo cargar datos/entrada.json: {error}")
        return None


def aplicar_estilos_tema(es_modo_oscuro):
    """
    Aplica estilos CSS para controlar con precision la apariencia de la aplicacion
    segun el tema activo (Claro u Oscuro).
    """
    if es_modo_oscuro:
        css = """<style>
/* Ocultar elementos nativos de navegacion de Streamlit */
#MainMenu { visibility: hidden !important; }
.stDeployButton { display: none !important; }
footer { visibility: hidden !important; }

/* Barra superior de Streamlit integrada al fondo */
header[data-testid="stHeader"] {
    background-color: #0b132b !important;
    border-bottom: 1px solid #1c2541 !important;
}

/* Fondo principal de la aplicacion */
.stApp {
    background-color: #0b132b !important;
    color: #f8fafc !important;
}

/* Barra lateral en negro puro */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
    border-right: 1px solid #1c2541 !important;
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Tarjetas y contenedores redondeados */
.tarjeta-seccion {
    background-color: #131d36;
    border: 1px solid #273559;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}

.tarjeta-alerta {
    background-color: #131d36;
    border: 1px solid #273559;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
}

/* Componente de subida de archivos (File Uploader) en Modo Oscuro */
[data-testid="stFileUploader"],
[data-testid="stFileUploader"] section,
[data-testid="stFileUploadDropzone"],
[data-testid="stFileUploaderDropzone"],
div[data-testid="stFileUploader"] > section,
div[data-testid="stFileUploader"] section,
div[data-testid="stFileUploadDropzone"],
section[data-testid="stFileUploadDropzone"] {
    background-color: #0f182c !important;
    border: 1px dashed #38bdf8 !important;
    border-radius: 12px !important;
    color: #f8fafc !important;
}
[data-testid="stFileUploader"] *,
[data-testid="stFileUploadDropzone"] *,
[data-testid="stFileUploaderDropzone"] *,
section[data-testid="stFileUploadDropzone"] * {
    color: #94a3b8 !important;
    background-color: transparent !important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploadDropzone"] small,
section[data-testid="stFileUploadDropzone"] small {
    color: #64748b !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploadDropzone"] button,
section[data-testid="stFileUploadDropzone"] button {
    background-color: #1e293b !important;
    color: #38bdf8 !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploadDropzone"] button:hover,
section[data-testid="stFileUploadDropzone"] button:hover {
    background-color: #38bdf8 !important;
    color: #0b132b !important;
}

/* Archivo cargado en File Uploader - Modo Oscuro */
[data-testid="stFileUploaderFile"],
div[data-testid="stFileUploaderFile"] {
    background-color: #131d36 !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
    color: #f8fafc !important;
    padding: 8px 12px !important;
}
[data-testid="stFileUploaderFile"] svg,
div[data-testid="stFileUploaderFileData"] svg,
[data-testid="stFileUploaderFileData"] svg {
    color: #38bdf8 !important;
    fill: #38bdf8 !important;
    stroke: #38bdf8 !important;
}
[data-testid="stFileUploaderFile"] *,
div[data-testid="stFileUploaderFileData"] * {
    color: #e2e8f0 !important;
}
[data-testid="stFileUploaderDeleteBtn"] button,
[data-testid="stFileUploaderDeleteBtn"] svg {
    color: #f87171 !important;
    fill: #f87171 !important;
}

/* Alertas y avisos en Modo Oscuro */
[data-testid="stAlert"] {
    background-color: #0c281e !important;
    border: 1px solid #10b981 !important;
    border-radius: 10px !important;
    color: #a7f3d0 !important;
}
[data-testid="stAlert"] * {
    color: #a7f3d0 !important;
}
[data-testid="stAlert"] svg {
    color: #34d399 !important;
    fill: #34d399 !important;
}

/* Tablas con bordes redondeados y texto de alto contraste */
[data-testid="stTable"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #273559 !important;
}
table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: 100% !important;
    background-color: #131d36 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
}
th {
    background-color: #1c2541 !important;
    color: #38bdf8 !important;
    font-weight: 700 !important;
    padding: 12px 14px !important;
    border-bottom: 1px solid #273559 !important;
    text-align: left !important;
}
td {
    background-color: #131d36 !important;
    color: #f8fafc !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #1e293b !important;
}
tr:last-child td {
    border-bottom: none !important;
}

/* Botones en Modo Oscuro */
div.stButton > button {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid #38bdf8 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.3) !important;
}
div.stButton > button:hover {
    background-color: #38bdf8 !important;
    color: #0b132b !important;
}

/* Metricas e indicadores clave */
[data-testid="stMetric"] {
    background-color: #0f182c !important;
    border: 1px solid #273559 !important;
    border-radius: 12px !important;
    padding: 14px !important;
}
[data-testid="stMetricLabel"] {
    color: #94a3b8 !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: #38bdf8 !important;
}
[data-testid="stMetricDelta"] * {
    color: #38bdf8 !important;
    fill: #38bdf8 !important;
}
</style>"""
    else:
        css = """<style>
/* Ocultar elementos nativos de navegacion de Streamlit */
#MainMenu { visibility: hidden !important; }
.stDeployButton { display: none !important; }
footer { visibility: hidden !important; }

/* Barra superior de Streamlit integrada al fondo */
header[data-testid="stHeader"] {
    background-color: #f4f7fb !important;
    border-bottom: 1px solid #cbd5e1 !important;
}

/* Fondo principal de la aplicacion en Modo Claro */
.stApp {
    background-color: #f4f7fb !important;
    color: #0f172a !important;
}

/* Barra lateral en blanco puro */
[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #cbd5e1 !important;
}
[data-testid="stSidebar"] * {
    color: #0f172a !important;
}

/* Tarjetas y contenedores redondeados */
.tarjeta-seccion {
    background-color: #e6eef8;
    border: 1px solid #b8d0eb;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

.tarjeta-alerta {
    background-color: #e6eef8;
    border: 1px solid #b8d0eb;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 22px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.05);
}

/* Componente de subida de archivos (File Uploader) en Modo Claro */
[data-testid="stFileUploader"] {
    background-color: #f8fafc !important;
    border: 1px dashed #0284c7 !important;
    border-radius: 12px !important;
    padding: 10px !important;
}
[data-testid="stFileUploadDropzone"] {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border: none !important;
}
[data-testid="stFileUploadDropzone"] * {
    color: #334155 !important;
}
[data-testid="stFileUploadDropzone"] button {
    background-color: #0284c7 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
}

/* Archivo cargado en File Uploader - Modo Claro (Evita icono negro) */
[data-testid="stFileUploaderFile"],
div[data-testid="stFileUploaderFile"] {
    background-color: #ffffff !important;
    border: 1px solid #bae6fd !important;
    border-radius: 10px !important;
    color: #0c4a6e !important;
    padding: 8px 12px !important;
}
[data-testid="stFileUploaderFile"] svg,
div[data-testid="stFileUploaderFileData"] svg,
[data-testid="stFileUploaderFileData"] svg {
    color: #0284c7 !important;
    fill: #0284c7 !important;
    stroke: #0284c7 !important;
}
[data-testid="stFileUploaderFile"] *,
div[data-testid="stFileUploaderFileData"] * {
    color: #0f172a !important;
}
[data-testid="stFileUploaderDeleteBtn"] button,
[data-testid="stFileUploaderDeleteBtn"] svg {
    color: #dc2626 !important;
    fill: #dc2626 !important;
}

/* Alertas y avisos en Modo Claro */
[data-testid="stAlert"] {
    background-color: #ecfdf5 !important;
    border: 1px solid #6ee7b7 !important;
    border-radius: 10px !important;
    color: #065f46 !important;
}
[data-testid="stAlert"] * {
    color: #065f46 !important;
}
[data-testid="stAlert"] svg {
    color: #059669 !important;
    fill: #059669 !important;
}

/* Tablas con bordes redondeados y texto de alto contraste en Modo Claro */
[data-testid="stTable"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid #cbd5e1 !important;
}
table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    width: 100% !important;
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 12px !important;
}
th {
    background-color: #e2e8f0 !important;
    color: #0369a1 !important;
    font-weight: 700 !important;
    padding: 12px 14px !important;
    border-bottom: 1px solid #cbd5e1 !important;
    text-align: left !important;
}
td {
    background-color: #ffffff !important;
    color: #0f172a !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid #e2e8f0 !important;
}
tr:last-child td {
    border-bottom: none !important;
}

/* Botones en Modo Claro */
div.stButton > button {
    background-color: #0284c7 !important;
    color: #ffffff !important;
    border: 1px solid #0369a1 !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    padding: 9px 20px !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
}
div.stButton > button:hover {
    background-color: #0369a1 !important;
}

/* Metricas e indicadores clave en Modo Claro */
[data-testid="stMetric"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 14px !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-weight: 600 !important;
}
[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"] {
    color: #0369a1 !important;
}
[data-testid="stMetricDelta"] * {
    color: #0369a1 !important;
    fill: #0369a1 !important;
    font-weight: 600 !important;
}

/* Correccion de la tabla editable en Modo Claro */
[data-testid="stDataEditor"] {
    background-color: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 10px !important;
}
</style>"""

    st.markdown(css, unsafe_allow_html=True)


def obtener_paco_b64():
    """Retorna la imagen de Paco en base64 con fondo transparente para integrarla al diseño."""
    ruta_paco = os.path.join(os.path.dirname(__file__), "paco.png")
    if os.path.exists(ruta_paco):
        try:
            with open(ruta_paco, "rb") as f:
                return base64.b64encode(f.read()).decode("ascii")
        except Exception:
            return ""
    return ""


def renderizar_banner_paisaje_edificio(edificio, tarifa, es_modo_oscuro):
    """
    Renderiza el banner superior panoramico donde el edificio y Paco forman parte del paisaje
    bajo el cielo diurno o nocturno.
    Garantiza cero sangrias para evitar que Markdown interprete el texto como bloque de codigo.
    """
    paco_b64 = obtener_paco_b64()
    paco_banner_html = (
        f'<img src="data:image/png;base64,{paco_b64}" alt="Paco" '
        f'title="Paco - Administrador del Edificio" '
        f'style="height: 104px; width: auto; object-fit: contain; '
        f'filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));" />'
        if paco_b64 else ""
    )

    if es_modo_oscuro:
        html = f"""<div style="background: linear-gradient(135deg, #050b1a 0%, #0d1b3a 40%, #172554 85%, #1e1b4b 100%); border-radius: 16px; padding: 24px 28px; margin-bottom: 24px; border: 1px solid #2b3a67; box-shadow: 0 6px 20px rgba(0,0,0,0.5);"><div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 16px;"><div style="max-width: 58%;"><div style="display: inline-block; background-color: rgba(56, 189, 248, 0.15); border: 1px solid #38bdf8; border-radius: 20px; padding: 4px 14px; margin-bottom: 10px;"><span style="color: #38bdf8; font-size: 13px; font-weight: 700; letter-spacing: 0.5px;">EDIFICIO: {edificio.upper()} | TARIFA: ${tarifa:,.2f} COP / kWh</span></div><h1 style="color: #ffffff; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; line-height: 1.2;">Gestion Energetica: Mapa de Calor del Consumo</h1><p style="color: #93c5fd; margin: 8px 0 0 0; font-size: 14px; font-weight: 500;">Monitoreo continuo de demanda electrica, deteccion de anomalias horarias y proyeccion de eficiencia</p></div><div style="flex-shrink: 0; display: flex; align-items: flex-end; gap: 12px;">{paco_banner_html}<svg width="220" height="110" viewBox="0 0 220 110" fill="none"><path d="M42 16 C32 16 24 24 24 34 C24 44 32 52 42 52 C36 48 32 41 32 34 C32 27 36 20 42 16 Z" fill="#fde047" filter="drop-shadow(0 0 8px rgba(253, 224, 71, 0.7))" /><circle cx="70" cy="18" r="1.8" fill="#ffffff" opacity="0.9" /><circle cx="105" cy="12" r="1.4" fill="#ffffff" opacity="0.8" /><circle cx="85" cy="40" r="1.6" fill="#93c5fd" opacity="0.85" /><circle cx="15" cy="35" r="1.5" fill="#fde047" opacity="0.75" /><polygon points="120,22 121,25 125,25 122,27 123,31 120,29 117,31 118,27 115,25 119,25" fill="#ffffff" opacity="0.85" /><rect x="0" y="98" width="220" height="12" fill="#0c1322" /><rect x="110" y="45" width="38" height="53" fill="#172554" rx="1" /><rect x="116" y="52" width="6" height="6" fill="#3b82f6" opacity="0.5" /><rect x="126" y="52" width="6" height="6" fill="#3b82f6" opacity="0.5" /><rect x="136" y="52" width="6" height="6" fill="#3b82f6" opacity="0.5" /><rect x="116" y="65" width="6" height="6" fill="#3b82f6" opacity="0.5" /><rect x="126" y="65" width="6" height="6" fill="#3b82f6" opacity="0.5" /><rect x="136" y="65" width="6" height="6" fill="#3b82f6" opacity="0.5" /><rect x="145" y="28" width="65" height="70" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5" rx="2" /><line x1="177" y1="28" x2="177" y2="15" stroke="#38bdf8" stroke-width="1.5" /><circle cx="177" cy="14" r="2.5" fill="#ef4444" /><rect x="154" y="36" width="9" height="9" fill="#fde047" rx="1" filter="drop-shadow(0 0 3px rgba(253, 224, 71, 0.8))" /><rect x="173" y="36" width="9" height="9" fill="#fde047" rx="1" filter="drop-shadow(0 0 3px rgba(253, 224, 71, 0.8))" /><rect x="192" y="36" width="9" height="9" fill="#334155" rx="1" /><rect x="154" y="52" width="9" height="9" fill="#334155" rx="1" /><rect x="173" y="52" width="9" height="9" fill="#fde047" rx="1" filter="drop-shadow(0 0 3px rgba(253, 224, 71, 0.8))" /><rect x="192" y="52" width="9" height="9" fill="#fde047" rx="1" filter="drop-shadow(0 0 3px rgba(253, 224, 71, 0.8))" /><rect x="154" y="68" width="9" height="9" fill="#fde047" rx="1" filter="drop-shadow(0 0 3px rgba(253, 224, 71, 0.8))" /><rect x="173" y="68" width="9" height="9" fill="#334155" rx="1" /><rect x="192" y="68" width="9" height="9" fill="#fde047" rx="1" filter="drop-shadow(0 0 3px rgba(253, 224, 71, 0.8))" /><rect x="171" y="85" width="13" height="13" fill="#0284c7" rx="1" /></svg></div></div></div>"""
    else:
        html = f"""<div style="background: linear-gradient(120deg, #bae6fd 0%, #e0f2fe 35%, #fef3c7 70%, #dcfce7 100%); border-radius: 16px; padding: 24px 28px; margin-bottom: 24px; border: 1px solid #7dd3fc; box-shadow: 0 4px 14px rgba(37, 99, 235, 0.08);"><div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 16px;"><div style="max-width: 58%;"><div style="display: inline-block; background-color: rgba(2, 132, 199, 0.12); border: 1px solid #0284c7; border-radius: 20px; padding: 4px 14px; margin-bottom: 10px;"><span style="color: #0369a1; font-size: 13px; font-weight: 700; letter-spacing: 0.5px;">EDIFICIO: {edificio.upper()} | TARIFA: ${tarifa:,.2f} COP / kWh</span></div><h1 style="color: #0c4a6e; margin: 0; font-size: 26px; font-weight: 800; letter-spacing: -0.5px; line-height: 1.2;">Gestion Energetica: Mapa de Calor del Consumo</h1><p style="color: #0369a1; margin: 8px 0 0 0; font-size: 14px; font-weight: 500;">Monitoreo continuo de demanda electrica, deteccion de anomalias horarias y proyeccion de eficiencia</p></div><div style="flex-shrink: 0; display: flex; align-items: flex-end; gap: 12px;">{paco_banner_html}<svg width="220" height="110" viewBox="0 0 220 110" fill="none"><circle cx="45" cy="35" r="16" fill="#f59e0b" filter="drop-shadow(0 0 10px rgba(245, 158, 11, 0.5))" /><circle cx="45" cy="35" r="13" fill="#fbbf24" /><line x1="45" y1="14" x2="45" y2="8" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" /><line x1="45" y1="56" x2="45" y2="62" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" /><line x1="24" y1="35" x2="18" y2="35" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" /><line x1="66" y1="35" x2="72" y2="35" stroke="#f59e0b" stroke-width="2.5" stroke-linecap="round" /><path d="M72 48 C72 43 76 40 81 40 C83 36 87 34 91 34 C96 34 100 37 101 41 C105 41 108 44 108 48 C108 52 105 55 101 55 L77 55 C74 55 72 52 72 48 Z" fill="#ffffff" opacity="0.95" /><rect x="0" y="98" width="220" height="12" fill="#86efac" /><rect x="110" y="45" width="38" height="53" fill="#93c5fd" rx="1" /><rect x="116" y="52" width="6" height="6" fill="#ffffff" opacity="0.7" /><rect x="126" y="52" width="6" height="6" fill="#ffffff" opacity="0.7" /><rect x="136" y="52" width="6" height="6" fill="#ffffff" opacity="0.7" /><rect x="116" y="65" width="6" height="6" fill="#ffffff" opacity="0.7" /><rect x="126" y="65" width="6" height="6" fill="#ffffff" opacity="0.7" /><rect x="136" y="65" width="6" height="6" fill="#ffffff" opacity="0.7" /><rect x="145" y="28" width="65" height="70" fill="#ffffff" stroke="#0284c7" stroke-width="1.8" rx="2" /><line x1="177" y1="28" x2="177" y2="15" stroke="#0284c7" stroke-width="1.5" /><circle cx="177" cy="14" r="2.5" fill="#0284c7" /><rect x="154" y="36" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="173" y="36" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="192" y="36" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="154" y="52" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="173" y="52" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="192" y="52" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="154" y="68" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="173" y="68" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="192" y="68" width="9" height="9" fill="#bae6fd" rx="1" /><rect x="171" y="85" width="13" height="13" fill="#0284c7" rx="1" /></svg></div></div></div>"""
    
    st.markdown(html, unsafe_allow_html=True)


def crear_mapa_calor(matriz, dias_etiquetas, horas_etiquetas, horas_mas_caras, umbral_valor, es_modo_oscuro):
    """
    Construye la figura del mapa de calor interactivo con Plotly adaptada al tema activo.
    """
    num_filas = len(matriz)
    num_cols = len(matriz[0]) if num_filas > 0 else 0

    texto_hover = []
    for f in range(num_filas):
        fila_texto = []
        nombre_dia = dias_etiquetas[f] if f < len(dias_etiquetas) else f"Dia {f + 1}"
        for c in range(num_cols):
            etiqueta_hora = horas_etiquetas[c] if c < len(horas_etiquetas) else f"Hora {c}"
            valor = matriz[f][c]
            sobre = " (ALERTA: Sobre Umbral)" if valor > umbral_valor else ""
            fila_texto.append(
                f"Dia: {nombre_dia}<br>Hora: {etiqueta_hora}<br>Consumo: {valor:.2f} kWh{sobre}"
            )
        texto_hover.append(fila_texto)

    bg_grafico = "#131d36" if es_modo_oscuro else "#ffffff"
    color_texto = "#f8fafc" if es_modo_oscuro else "#0f172a"
    color_rejilla = "#273559" if es_modo_oscuro else "#e2e8f0"

    fig = go.Figure(
        data=go.Heatmap(
            z=matriz,
            x=horas_etiquetas[:num_cols],
            y=dias_etiquetas[:num_filas],
            colorscale="RdYlBu_r",
            hoverinfo="text",
            text=texto_hover,
            colorbar=dict(
                title=dict(text="kWh", font=dict(color=color_texto)),
                tickfont=dict(color=color_texto)
            )
        )
    )

    # Marcador tipo rombo para la hora mas cara de cada dia (Reto funcional)
    x_caras, y_caras, hover_caras = [], [], []
    for item in horas_mas_caras:
        d_idx = item["dia"]
        h_idx = item["hora"]
        if d_idx < num_filas and h_idx < num_cols:
            dia_nombre = dias_etiquetas[d_idx] if d_idx < len(dias_etiquetas) else f"Dia {d_idx + 1}"
            hora_nombre = horas_etiquetas[h_idx] if h_idx < len(horas_etiquetas) else f"Hora {h_idx}"
            x_caras.append(hora_nombre)
            y_caras.append(dia_nombre)
            hover_caras.append(
                f"Pico de costo diario: {dia_nombre}<br>"
                f"Hora: {hora_nombre}<br>"
                f"Consumo: {item['kwh']:.2f} kWh<br>"
                f"Costo: ${item['costo']:.2f}"
            )

    fig.add_trace(
        go.Scatter(
            x=x_caras,
            y=y_caras,
            mode="markers",
            marker=dict(
                symbol="diamond",
                size=13,
                color="#facc15" if es_modo_oscuro else "#1e293b",
                line=dict(color="#ffffff" if es_modo_oscuro else "#facc15", width=1.8)
            ),
            name="Hora mas cara",
            hoverinfo="text",
            hovertext=hover_caras
        )
    )

    fig.update_layout(
        title=dict(
            text="Matriz de Demanda Semanal 7x24 [Rombo: Hora mas cara de cada dia]",
            x=0.0,
            font=dict(color=color_texto, size=15)
        ),
        xaxis=dict(
            title=dict(text="Hora del dia", font=dict(color=color_texto)),
            tickangle=-45,
            tickfont=dict(color=color_texto),
            gridcolor=color_rejilla
        ),
        yaxis=dict(
            title=dict(text="Dia de la semana", font=dict(color=color_texto)),
            autorange="reversed",
            tickfont=dict(color=color_texto),
            gridcolor=color_rejilla
        ),
        paper_bgcolor=bg_grafico,
        plot_bgcolor=bg_grafico,
        margin=dict(l=40, r=40, t=50, b=40),
        height=480
    )

    return fig


def crear_grafico_barras_dias(totales_dia, dias_etiquetas, es_modo_oscuro):
    """Genera grafico de barras adaptado al tema actual."""
    etiquetas = dias_etiquetas[:len(totales_dia)]
    bg_grafico = "#131d36" if es_modo_oscuro else "#ffffff"
    color_texto = "#f8fafc" if es_modo_oscuro else "#0f172a"
    color_barra = "#38bdf8" if es_modo_oscuro else "#0284c7"
    color_rejilla = "#273559" if es_modo_oscuro else "#e2e8f0"

    fig = go.Figure(
        data=[
            go.Bar(
                x=etiquetas,
                y=totales_dia,
                text=[f"{v:.1f}" for v in totales_dia],
                textposition="auto",
                marker=dict(color=color_barra, line=dict(color=bg_grafico, width=1))
            )
        ]
    )
    fig.update_layout(
        title=dict(
            text="Consumo Total Acumulado por Dia (kWh)",
            font=dict(color=color_texto, size=14)
        ),
        xaxis=dict(tickfont=dict(color=color_texto), gridcolor=color_rejilla),
        yaxis=dict(title=dict(text="kWh", font=dict(color=color_texto)), tickfont=dict(color=color_texto), gridcolor=color_rejilla),
        paper_bgcolor=bg_grafico,
        plot_bgcolor=bg_grafico,
        margin=dict(l=20, r=20, t=40, b=20),
        height=260
    )
    return fig


def main():
    # Inicializacion de estados en session_state
    if "datos_actuales" not in st.session_state:
        st.session_state["datos_actuales"] = obtener_datos_base()

    if "matriz_editada" not in st.session_state and st.session_state["datos_actuales"]:
        st.session_state["matriz_editada"] = [
            fila[:] for fila in st.session_state["datos_actuales"]["consumo"]
        ]

    if "tema_activo" not in st.session_state:
        st.session_state["tema_activo"] = "oscuro"

    if "seccion_activa" not in st.session_state:
        st.session_state["seccion_activa"] = "admin"

    es_modo_oscuro = (st.session_state["tema_activo"] == "oscuro")
    aplicar_estilos_tema(es_modo_oscuro)

    # -------------------------------------------------------------
    # BARRA LATERAL CON SELECTORES VISUALES E ILUSTRACIONES VECTORIALES
    # -------------------------------------------------------------
    paco_b64 = obtener_paco_b64()
    if paco_b64:
        bg_card_paco = "#0f182c" if es_modo_oscuro else "#f0f9ff"
        border_card_paco = "#273559" if es_modo_oscuro else "#bae6fd"
        txt_title_paco = "#ffffff" if es_modo_oscuro else "#0c4a6e"
        txt_sub_paco = "#38bdf8" if es_modo_oscuro else "#0284c7"
        st.sidebar.markdown(
            f"""<div style="display: flex; align-items: center; gap: 12px; background-color: {bg_card_paco}; border: 1px solid {border_card_paco}; border-radius: 12px; padding: 10px 14px; margin-bottom: 16px; box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
                <img src="data:image/png;base64,{paco_b64}" alt="Paco" style="height: 50px; width: auto; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.25));" />
                <div>
                    <div style="font-size: 14px; font-weight: 800; color: {txt_title_paco};">Paco</div>
                    <div style="font-size: 11px; font-weight: 600; color: {txt_sub_paco};">Administrador del Edificio</div>
                </div>
            </div>""",
            unsafe_allow_html=True
        )

    st.sidebar.markdown("""<div style="font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #94a3b8; margin-bottom: 8px;">APARIENCIA VISUAL</div>""", unsafe_allow_html=True)

    # Visual del tema activo
    if es_modo_oscuro:
        st.sidebar.markdown("""<div style="display: flex; align-items: center; gap: 10px; background-color: #0f172a; border: 1px solid #38bdf8; border-radius: 10px; padding: 10px; margin-bottom: 10px;"><svg width="28" height="28" viewBox="0 0 24 24" fill="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" fill="#fde047" stroke="#facc15" stroke-width="1.5"/></svg><div><div style="font-size: 13px; font-weight: 700; color: #ffffff;">Tema Oscuro Activo</div><div style="font-size: 11px; color: #94a3b8;">Ambiente Nocturno</div></div></div>""", unsafe_allow_html=True)
        if st.sidebar.button("Cambiar a Tema Claro (Dia)"):
            st.session_state["tema_activo"] = "claro"
            st.rerun()
    else:
        st.sidebar.markdown("""<div style="display: flex; align-items: center; gap: 10px; background-color: #f0f9ff; border: 1px solid #0284c7; border-radius: 10px; padding: 10px; margin-bottom: 10px;"><svg width="28" height="28" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="5" fill="#f59e0b"/><line x1="12" y1="1" x2="12" y2="3" stroke="#f59e0b" stroke-width="2"/><line x1="12" y1="21" x2="12" y2="23" stroke="#f59e0b" stroke-width="2"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64" stroke="#f59e0b" stroke-width="2"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" stroke="#f59e0b" stroke-width="2"/><line x1="1" y1="12" x2="3" y2="12" stroke="#f59e0b" stroke-width="2"/><line x1="21" y1="12" x2="23" y2="12" stroke="#f59e0b" stroke-width="2"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36" stroke="#f59e0b" stroke-width="2"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" stroke="#f59e0b" stroke-width="2"/></svg><div><div style="font-size: 13px; font-weight: 700; color: #0c4a6e;">Tema Claro Activo</div><div style="font-size: 11px; color: #0369a1;">Ambiente Diurno</div></div></div>""", unsafe_allow_html=True)
        if st.sidebar.button("Cambiar a Tema Oscuro (Noche)"):
            st.session_state["tema_activo"] = "oscuro"
            st.rerun()

    st.sidebar.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #334155;'>", unsafe_allow_html=True)
    st.sidebar.markdown("""<div style="font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #94a3b8; margin-bottom: 8px;">MODULO DE NAVEGACION</div>""", unsafe_allow_html=True)

    # Botones con ilustraciones vectoriales de navegacion
    col_nav1, col_nav2 = st.sidebar.columns(2)
    with col_nav1:
        st.markdown("""<div style="text-align: center; margin-bottom: 4px;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg></div>""", unsafe_allow_html=True)
        if st.button("Panel Administrador", key="btn_nav_admin", use_container_width=True):
            st.session_state["seccion_activa"] = "admin"
            st.rerun()

    with col_nav2:
        st.markdown("""<div style="text-align: center; margin-bottom: 4px;"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>""", unsafe_allow_html=True)
        if st.button("Casos de Prueba", key="btn_nav_tests", use_container_width=True):
            st.session_state["seccion_activa"] = "tests"
            st.rerun()

    seccion = st.session_state["seccion_activa"]

    # -------------------------------------------------------------
    # VISTA 1: PANEL ADMINISTRADOR
    # -------------------------------------------------------------
    if seccion == "admin":
        datos = st.session_state.get("datos_actuales")
        if not datos:
            st.warning("No hay registros disponibles para mostrar.")
            return

        edificio = datos.get("edificio", "Bloque A")
        tarifa = float(datos.get("tarifa", 850.0))
        matriz_activa = st.session_state["matriz_editada"]

        # Renderizar el paisaje panoramico unificado con el edificio integrado
        renderizar_banner_paisaje_edificio(edificio, tarifa, es_modo_oscuro)

        # Opciones en la barra lateral
        st.sidebar.markdown("<hr style='margin: 16px 0; border: none; border-top: 1px solid #334155;'>", unsafe_allow_html=True)
        st.sidebar.markdown("""<div style="font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; color: #94a3b8; margin-bottom: 8px;">PARAMETROS DE CONTROL</div>""", unsafe_allow_html=True)

        archivo_subido = st.sidebar.file_uploader(
            "Cargar archivo JSON (7x24)",
            type=["json"],
            help="Estructura requerida: 'edificio', 'tarifa' y 'consumo' (7x24)."
        )

        if archivo_subido is not None:
            try:
                contenido = json.load(archivo_subido)
                datos_validados = logica.cargar_datos(contenido, validar_7x24=True)
                st.session_state["datos_actuales"] = datos_validados
                st.session_state["matriz_editada"] = [fila[:] for fila in datos_validados["consumo"]]
                if es_modo_oscuro:
                    st.sidebar.markdown(
                        f"""<div style="background-color: #0c281e; border: 1px solid #10b981; border-radius: 10px; padding: 10px 14px; margin: 10px 0; display: flex; align-items: center; gap: 8px;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                            <span style="color: #a7f3d0; font-size: 13px; font-weight: 700;">[OK] Archivo cargado: {datos_validados['edificio']}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )
                else:
                    st.sidebar.markdown(
                        f"""<div style="background-color: #ecfdf5; border: 1px solid #10b981; border-radius: 10px; padding: 10px 14px; margin: 10px 0; display: flex; align-items: center; gap: 8px;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#059669" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>
                            <span style="color: #065f46; font-size: 13px; font-weight: 700;">[OK] Archivo cargado: {datos_validados['edificio']}</span>
                        </div>""",
                        unsafe_allow_html=True
                    )
            except Exception as error_carga:
                if es_modo_oscuro:
                    st.sidebar.markdown(
                        f"""<div style="background-color: #2b1218; border: 1px solid #ef4444; border-radius: 10px; padding: 10px 14px; margin: 10px 0; color: #fca5a5; font-size: 13px;">
                            <strong>[ERROR de formato]:</strong> {error_carga}
                        </div>""",
                        unsafe_allow_html=True
                    )
                else:
                    st.sidebar.markdown(
                        f"""<div style="background-color: #fef2f2; border: 1px solid #f87171; border-radius: 10px; padding: 10px 14px; margin: 10px 0; color: #991b1b; font-size: 13px;">
                            <strong>[ERROR de formato]:</strong> {error_carga}
                        </div>""",
                        unsafe_allow_html=True
                    )

        max_consumo = max(max(fila) for fila in matriz_activa) if matriz_activa else 50.0
        val_defecto = min(25.0, max_consumo)

        umbral_usuario = st.sidebar.slider(
            "Umbral critico de consumo (kWh):",
            min_value=0.0,
            max_value=float(max(100.0, max_consumo + 15.0)),
            value=float(val_defecto),
            step=0.5
        )

        ahorro_porcentaje = st.sidebar.slider(
            "Meta de ahorro proyectado (%):",
            min_value=0.0,
            max_value=50.0,
            value=10.0,
            step=1.0
        )

        # Calculos en tiempo real con logica.py
        totales_promedios = logica.calcular_totales_y_promedios(matriz_activa)
        pico = logica.encontrar_pico(matriz_activa)
        res_umbral = logica.evaluar_umbral(matriz_activa, umbral_usuario)
        proyeccion = logica.proyectar_ahorro(matriz_activa, ahorro_porcentaje)
        horas_caras = logica.calcular_horas_mas_caras(matriz_activa, tarifa)

        # Tarjetas de metricas principales (KPIs)
        st.markdown('<div class="tarjeta-seccion">', unsafe_allow_html=True)
        st.markdown("#### Indicadores Clave de Demanda Energetica")
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)

        promedios_hora = totales_promedios["promedio_por_hora"]
        hora_mayor_prom = 0
        val_mayor_prom = promedios_hora[0] if promedios_hora else 0.0
        for h_i, prom_val in enumerate(promedios_hora):
            if prom_val > val_mayor_prom:
                val_mayor_prom = prom_val
                hora_mayor_prom = h_i

        with col_kpi1:
            st.metric(
                label="Consumo Total Semanal",
                value=f"{totales_promedios['total_semana']:,.2f} kWh",
                help="Suma acumulada de todas las mediciones horarias."
            )

        with col_kpi2:
            dia_pico_nombre = DIAS_SEMANA[pico["dia"]] if pico["dia"] < len(DIAS_SEMANA) else f"Dia {pico['dia'] + 1}"
            st.metric(
                label="Pico Maximo Registrado",
                value=f"{pico['valor']:.2f} kWh",
                delta=f"{dia_pico_nombre} a las {pico['hora']:02d}:00",
                delta_color="inverse",
                help="Hora con el mayor consumo puntual."
            )

        with col_kpi3:
            st.metric(
                label="Hora con Mayor Promedio",
                value=f"{val_mayor_prom:.2f} kWh",
                delta=f"Demanda media a las {hora_mayor_prom:02d}:00",
                delta_color="off",
                help="Hora con mayor gasto sistematico en la semana."
            )

        st.markdown("<br>", unsafe_allow_html=True)
        fig_barras = crear_grafico_barras_dias(totales_promedios["total_por_dia"], DIAS_SEMANA, es_modo_oscuro)
        st.plotly_chart(fig_barras, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Mapa de Calor 7x24
        st.markdown('<div class="tarjeta-seccion">', unsafe_allow_html=True)
        st.markdown("#### Mapa de Calor Semanal (7 Dias x 24 Horas)")
        fig_mapa = crear_mapa_calor(matriz_activa, DIAS_SEMANA, HORAS_DIA, horas_caras, umbral_usuario, es_modo_oscuro)
        st.plotly_chart(fig_mapa, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Seccion de Umbral con bordes redondeados y estilo unificado
        st.markdown('<div class="tarjeta-seccion">', unsafe_allow_html=True)
        st.markdown("#### Deteccion de Horas Criticas sobre el Umbral")
        if res_umbral["cantidad"] == 0:
            st.info(f"Ninguna hora supera el umbral configurado de {umbral_usuario:.2f} kWh.")
        else:
            color_resalte = "#38bdf8" if es_modo_oscuro else "#0284c7"
            st.markdown(
                f"<span style='color: {color_resalte}; font-weight: 700;'>Registro de horas criticas:</span> "
                f"Se detectaron <strong>{res_umbral['cantidad']} hora(s)</strong> que superan el umbral de "
                f"<strong>{umbral_usuario:.2f} kWh</strong>:",
                unsafe_allow_html=True
            )
            filas_umbral = []
            for item in res_umbral["horas_sobre_umbral"]:
                dia_nom = DIAS_SEMANA[item["dia"]] if item["dia"] < len(DIAS_SEMANA) else f"Dia {item['dia'] + 1}"
                filas_umbral.append({
                    "Dia": dia_nom,
                    "Hora": f"{item['hora']:02d}:00",
                    "Consumo (kWh)": f"{item['valor']:.2f}",
                    "Exceso (kWh)": f"+{item['valor'] - umbral_usuario:.2f}"
                })
            st.table(filas_umbral)
        st.markdown('</div>', unsafe_allow_html=True)

        # Seccion de Proyeccion
        st.markdown('<div class="tarjeta-seccion">', unsafe_allow_html=True)
        st.markdown(f"#### Simulacion de Eficiencia y Proyeccion de Ahorro ({ahorro_porcentaje:.0f}%)")
        col_proy1, col_proy2, col_proy3 = st.columns(3)
        costo_original = totales_promedios["total_semana"] * tarifa
        costo_proyectado = proyeccion["total_proyectado"] * tarifa
        ahorro_dinero = costo_original - costo_proyectado

        with col_proy1:
            st.metric(
                label="Consumo Proyectado",
                value=f"{proyeccion['total_proyectado']:,.2f} kWh",
                delta=f"-{proyeccion['ahorro_kwh']:,.2f} kWh ({ahorro_porcentaje:.0f}%)",
                delta_color="normal"
            )
        with col_proy2:
            st.metric(
                label="Costo Estimado Proyectado",
                value=f"${costo_proyectado:,.2f} COP",
                delta=f"-${ahorro_dinero:,.2f} COP",
                delta_color="normal"
            )
        with col_proy3:
            st.metric(
                label="Factor de Ajuste",
                value=f"{proyeccion['factor']:.4f}",
                help="Factor multiplicador aplicado a toda la matriz."
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Seccion de Edicion en Vivo
        st.markdown('<div class="tarjeta-seccion">', unsafe_allow_html=True)
        st.markdown("#### Correccion de Datos en Vivo")
        st.caption(
            "Cualquier celda editada recalcula al instante todos los indicadores, el mapa de calor "
            "y los ahorros. La matriz del archivo JSON original permanece inalterada."
        )

        col_b1, col_b2 = st.columns([1, 2])
        with col_b1:
            if st.button("Restablecer a valores originales"):
                st.session_state["matriz_editada"] = [
                    fila[:] for fila in st.session_state["datos_actuales"]["consumo"]
                ]
                st.rerun()

        with col_b2:
            if st.button("Guardar reporte actual en datos/salida.json"):
                resumen_salida = logica.generar_resumen_completo(
                    edificio=edificio,
                    tarifa=tarifa,
                    matriz_consumo=matriz_activa,
                    valor_umbral=umbral_usuario,
                    porcentaje_ahorro=ahorro_porcentaje
                )
                logica.guardar_resumen("datos/salida.json", resumen_salida)
                st.session_state["ultimo_resumen_guardado"] = resumen_salida
                st.success("[OK] Reporte guardado con exito en datos/salida.json")

            if "ultimo_resumen_guardado" in st.session_state:
                salida_bytes = json.dumps(st.session_state["ultimo_resumen_guardado"], indent=2, ensure_ascii=False).encode("utf-8")
                st.download_button(
                    label="Descargar datos/salida.json",
                    data=salida_bytes,
                    file_name="salida.json",
                    mime="application/json"
                )

        datos_tabla = {HORAS_DIA[h]: [matriz_activa[d][h] for d in range(7)] for h in range(24)}
        datos_tabla_con_dias = {"Dia": DIAS_SEMANA}
        datos_tabla_con_dias.update(datos_tabla)

        tabla_editada = st.data_editor(
            datos_tabla_con_dias,
            disabled=["Dia"],
            use_container_width=True,
            key="editor_matriz"
        )

        matriz_nueva = []
        for d in range(7):
            fila_nueva = []
            for h in range(24):
                col_nombre = HORAS_DIA[h]
                try:
                    valor_celda = float(tabla_editada[col_nombre][d])
                except (ValueError, TypeError):
                    valor_celda = float(matriz_activa[d][h])
                fila_nueva.append(valor_celda)
            matriz_nueva.append(fila_nueva)

        if matriz_nueva != st.session_state["matriz_editada"]:
            st.session_state["matriz_editada"] = matriz_nueva
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # VISTA 2: CASOS DE PRUEBA (PROFESOR ALEX)
    # -------------------------------------------------------------
    elif seccion == "tests":
        datos = st.session_state.get("datos_actuales")
        edificio = datos.get("edificio", "Bloque A") if datos else "Bloque A"
        tarifa = float(datos.get("tarifa", 850.0)) if datos else 850.0

        renderizar_banner_paisaje_edificio(edificio, tarifa, es_modo_oscuro)

        st.markdown('<div class="tarjeta-seccion">', unsafe_allow_html=True)
        st.markdown("### Auditoria y Verificacion de Resultados Oficiales")
        st.markdown(
            "Verificacion de referencia segun las especificaciones de evaluacion del profesor Alex "
            "empleando la matriz de prueba reducida (3 dias x 4 horas)."
        )

        matriz_test = [
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [2, 2, 2, 2]
        ]

        st.markdown("##### Matriz de Entrada de Verificacion (3x4):")
        st.table({
            "Dia": ["Dia 1", "Dia 2", "Dia 3"],
            "Hora 1 (0:00)": [1, 5, 2],
            "Hora 2 (1:00)": [2, 6, 2],
            "Hora 3 (2:00)": [3, 7, 2],
            "Hora 4 (3:00)": [4, 8, 2]
        })

        st.caption(
            "Correspondencia de indices: En logica.py los indices parten de 0. "
            "En la verificacion del enunciado se evalua con indice + 1 (1-indexado)."
        )

        st.markdown("---")

        if st.button("Ejecutar Verificacion Automatizada"):
            # 1. Totales por dia
            res_tot_prom = logica.calcular_totales_y_promedios(matriz_test)
            tot_obtenidos = [round(x, 2) for x in res_tot_prom["total_por_dia"]]
            tot_esperados = [10.0, 26.0, 8.0]
            ok_tot = (tot_obtenidos == tot_esperados)

            # 2. Promedios por hora
            prom_obtenidos = [round(x, 2) for x in res_tot_prom["promedio_por_hora"]]
            prom_esperados = [2.67, 3.33, 4.00, 4.67]
            ok_prom = (prom_obtenidos == prom_esperados)

            # 3. Pico
            pico_res = logica.encontrar_pico(matriz_test)
            dia_pico_h = pico_res["dia"] + 1
            hora_pico_h = pico_res["hora"] + 1
            val_pico = pico_res["valor"]
            ok_pico = (dia_pico_h == 2 and hora_pico_h == 4 and val_pico == 8.0)

            # 4. Umbral 5 kWh
            res_u5 = logica.evaluar_umbral(matriz_test, 5.0)
            cant_u5 = res_u5["cantidad"]
            celdas_u5 = [(c["dia"] + 1, c["hora"] + 1, c["valor"]) for c in res_u5["horas_sobre_umbral"]]
            esperadas_u5 = [(2, 2, 6.0), (2, 3, 7.0), (2, 4, 8.0)]
            ok_u5 = (cant_u5 == 3 and celdas_u5 == esperadas_u5)

            # 5. Umbral 100 kWh
            res_u100 = logica.evaluar_umbral(matriz_test, 100.0)
            ok_u100 = (res_u100["cantidad"] == 0 and len(res_u100["horas_sobre_umbral"]) == 0)

            # 6. Proyeccion x0.5
            res_proy = logica.proyectar_ahorro(matriz_test, 50.0)
            fila2_obtenida = [round(x, 1) for x in res_proy["consumo_proyectado"][1]]
            fila2_esperada = [2.5, 3.0, 3.5, 4.0]
            ok_proy = (fila2_obtenida == fila2_esperada and res_proy["factor"] == 0.5)

            resumen_pruebas = [
                {
                    "Criterio": "1. Total por dia",
                    "Esperado": str(tot_esperados),
                    "Obtenido": str(tot_obtenidos),
                    "Estado": "[OK] Superado" if ok_tot else "[FALLO]"
                },
                {
                    "Criterio": "2. Promedio por hora",
                    "Esperado": str(prom_esperados),
                    "Obtenido": str(prom_obtenidos),
                    "Estado": "[OK] Superado" if ok_prom else "[FALLO]"
                },
                {
                    "Criterio": "3. Pico de la matriz",
                    "Esperado": "Dia 2, Hora 4, 8.0 kWh",
                    "Obtenido": f"Dia {dia_pico_h}, Hora {hora_pico_h}, {val_pico:.1f} kWh",
                    "Estado": "[OK] Superado" if ok_pico else "[FALLO]"
                },
                {
                    "Criterio": "4. Umbral 5 kWh (3 celdas)",
                    "Esperado": "3 celdas: (2,2, 6), (2,3, 7), (2,4, 8)",
                    "Obtenido": f"{cant_u5} celdas: {celdas_u5}",
                    "Estado": "[OK] Superado" if ok_u5 else "[FALLO]"
                },
                {
                    "Criterio": "5. Umbral 100 kWh (0 celdas)",
                    "Esperado": "0 celdas",
                    "Obtenido": f"{res_u100['cantidad']} celdas",
                    "Estado": "[OK] Superado" if ok_u100 else "[FALLO]"
                },
                {
                    "Criterio": "6. Proyeccion factor 0.5 (Ahorro 50%)",
                    "Esperado": f"Fila 2: {fila2_esperada}",
                    "Obtenido": f"Fila 2: {fila2_obtenida}",
                    "Estado": "[OK] Superado" if ok_proy else "[FALLO]"
                }
            ]

            st.table(resumen_pruebas)

            if all([ok_tot, ok_prom, ok_pico, ok_u5, ok_u100, ok_proy]):
                st.success("[EXITO] Todas las pruebas oficiales del profesor Alex coinciden al 100%.")
            else:
                st.error("[ERROR] Se encontraron diferencias en las pruebas.")

        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
