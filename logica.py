"""
Módulo de lógica para el análisis del consumo energético de un edificio.
Proyecto 1: Mapa de calor del consumo de un edificio.
Materia: Fundamentos de Programación e IA.

Este módulo implementa cálculos puros en Python (listas, diccionarios, ciclos,
condicionales y JSON), sin dependencias como pandas o numpy.
"""

import json


def cargar_datos(ruta_archivo, validar_7x24=True):
    """
    Carga y valida los datos de consumo desde un archivo JSON.

    Parámetros:
        ruta_archivo (str): Ruta relativa o absoluta del archivo JSON.
        validar_7x24 (bool): Si es True, exige que la matriz sea de 7 días x 24 horas.
                             Si es False, permite cualquier dimensión (ej. casos de prueba).

    Retorna:
        dict: Diccionario con las claves 'edificio', 'tarifa' y 'consumo'.

    Lanza:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si la estructura, claves o tipos de datos son inválidos.
    """
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        datos = json.load(archivo)

    # 1. Validar que sea un diccionario
    if not isinstance(datos, dict):
        raise ValueError("El archivo JSON debe contener un objeto/diccionario principal.")

    # 2. Validar que contenga las tres claves obligatorias
    claves_obligatorias = ["edificio", "tarifa", "consumo"]
    for clave in claves_obligatorias:
        if clave not in datos:
            raise ValueError(f"Falta la clave obligatoria '{clave}' en el archivo JSON.")

    # 3. Validar tarifa
    if not isinstance(datos["tarifa"], (int, float)) or datos["tarifa"] < 0:
        raise ValueError("La 'tarifa' debe ser un número positivo.")

    # 4. Validar matriz de consumo
    matriz = datos["consumo"]
    if not isinstance(matriz, list) or len(matriz) == 0:
        raise ValueError("El campo 'consumo' debe ser una lista de listas no vacía.")

    num_filas = len(matriz)
    if validar_7x24 and num_filas != 7:
        raise ValueError(f"La matriz debe tener 7 filas (días de la semana). Se recibieron {num_filas}.")

    for indice_fila, fila in enumerate(matriz):
        if not isinstance(fila, list):
            raise ValueError(f"La fila {indice_fila} no es una lista válida.")
        
        num_columnas = len(fila)
        if validar_7x24 and num_columnas != 24:
            raise ValueError(
                f"La fila {indice_fila} debe tener 24 valores (horas). Se recibieron {num_columnas}."
            )

        for indice_col, valor in enumerate(fila):
            if not isinstance(valor, (int, float)) or isinstance(valor, bool):
                raise ValueError(
                    f"Valor inválido en fila {indice_fila}, columna {indice_col}: '{valor}' no es numérico."
                )

    return datos


def calcular_totales_y_promedios(matriz_consumo):
    """
    Calcula el total general de consumo, el total por día y el promedio por cada hora.
    Funciona para matrices de cualquier dimensión (N filas x M columnas).

    Parámetros:
        matriz_consumo (list de list de float): Matriz con los valores de consumo.

    Retorna:
        dict: {
            "total_semana": float,
            "total_por_dia": list de float,
            "promedio_por_hora": list de float
        }
    """
    num_dias = len(matriz_consumo)
    num_horas = len(matriz_consumo[0]) if num_dias > 0 else 0

    total_general = 0.0
    totales_por_dia = []

    # Cálculo del total de cada día (fila)
    for fila in matriz_consumo:
        suma_dia = 0.0
        for valor in fila:
            suma_dia += valor
        totales_por_dia.append(round(suma_dia, 2))
        total_general += suma_dia

    # Cálculo del promedio de cada hora (columna)
    promedios_por_hora = []
    for col_idx in range(num_horas):
        suma_hora = 0.0
        for fila_idx in range(num_dias):
            suma_hora += matriz_consumo[fila_idx][col_idx]
        promedio = suma_hora / num_dias if num_dias > 0 else 0.0
        promedios_por_hora.append(round(promedio, 2))

    return {
        "total_semana": round(total_general, 2),
        "total_por_dia": totales_por_dia,
        "promedio_por_hora": promedios_por_hora
    }


def encontrar_pico(matriz_consumo):
    """
    Encuentra el consumo máximo registrado en toda la matriz, indicando día y hora.
    Los índices retornados parten desde 0.

    Parámetros:
        matriz_consumo (list de list de float): Matriz de consumo.

    Retorna:
        dict: {"dia": int, "hora": int, "valor": float}
    """
    if not matriz_consumo or not matriz_consumo[0]:
        return {"dia": 0, "hora": 0, "valor": 0.0}

    max_dia = 0
    max_hora = 0
    max_valor = matriz_consumo[0][0]

    for d_idx, fila in enumerate(matriz_consumo):
        for h_idx, valor in enumerate(fila):
            if valor > max_valor:
                max_valor = valor
                max_dia = d_idx
                max_hora = h_idx

    return {
        "dia": max_dia,
        "hora": max_hora,
        "valor": float(max_valor)
    }


def evaluar_umbral(matriz_consumo, valor_umbral):
    """
    Identifica todas las horas en las que el consumo supera estrictamente un umbral.

    Parámetros:
        matriz_consumo (list de list de float): Matriz de consumo.
        valor_umbral (float): Valor límite en kWh.

    Retorna:
        dict: {
            "valor_kwh": float,
            "cantidad": int,
            "horas_sobre_umbral": [{"dia": int, "hora": int, "valor": float}, ...]
        }
    """
    horas_sobre_umbral = []

    for d_idx, fila in enumerate(matriz_consumo):
        for h_idx, valor in enumerate(fila):
            if valor > valor_umbral:
                horas_sobre_umbral.append({
                    "dia": d_idx,
                    "hora": h_idx,
                    "valor": float(valor)
                })

    return {
        "valor_kwh": float(valor_umbral),
        "cantidad": len(horas_sobre_umbral),
        "horas_sobre_umbral": horas_sobre_umbral
    }


def proyectar_ahorro(matriz_consumo, porcentaje_ahorro):
    """
    Genera una proyección de consumo reduciendo el consumo original según un porcentaje.
    Garantiza que la matriz original no se modifique.

    Parámetros:
        matriz_consumo (list de list de float): Matriz de consumo original.
        porcentaje_ahorro (float): Porcentaje de ahorro deseado (ej. 10 para 10%).

    Retorna:
        dict: {
            "ahorro_porcentaje": float,
            "factor": float,
            "consumo_proyectado": list de list de float,
            "total_proyectado": float,
            "ahorro_kwh": float
        }
    """
    factor = round(1.0 - (porcentaje_ahorro / 100.0), 4)
    matriz_proyectada = []
    total_original = 0.0
    total_proyectado = 0.0

    for fila in matriz_consumo:
        fila_proyectada = []
        for valor in fila:
            total_original += valor
            valor_proy = round(valor * factor, 2)
            fila_proyectada.append(valor_proy)
            total_proyectado += valor_proy
        matriz_proyectada.append(fila_proyectada)

    ahorro_kwh = round(total_original - total_proyectado, 2)

    return {
        "ahorro_porcentaje": float(porcentaje_ahorro),
        "factor": factor,
        "consumo_proyectado": matriz_proyectada,
        "total_proyectado": round(total_proyectado, 2),
        "ahorro_kwh": ahorro_kwh
    }


def calcular_horas_mas_caras(matriz_consumo, tarifa):
    """
    Determina para cada día cuál fue la hora de mayor consumo y su costo asociado.

    Parámetros:
        matriz_consumo (list de list de float): Matriz de consumo.
        tarifa (float): Costo por kWh.

    Retorna:
        list de dict: [{"dia": int, "hora": int, "kwh": float, "costo": float}, ...]
    """
    horas_caras = []

    for d_idx, fila in enumerate(matriz_consumo):
        if not fila:
            continue
        hora_max = 0
        valor_max = fila[0]
        for h_idx, valor in enumerate(fila):
            if valor > valor_max:
                valor_max = valor
                hora_max = h_idx

        costo = round(valor_max * tarifa, 2)
        horas_caras.append({
            "dia": d_idx,
            "hora": hora_max,
            "kwh": float(valor_max),
            "costo": costo
        })

    return horas_caras


def generar_resumen_completo(edificio, tarifa, matriz_consumo, valor_umbral=25.0, porcentaje_ahorro=10.0):
    """
    Ensambla la estructura completa requerida para 'datos/salida.json'.

    Parámetros:
        edificio (str): Nombre del edificio o bloque.
        tarifa (float): Precio por kWh.
        matriz_consumo (list de list de float): Matriz de consumo.
        valor_umbral (float): Umbral para resaltar horas críticas.
        porcentaje_ahorro (float): Porcentaje de ahorro para la proyección.

    Retorna:
        dict: Diccionario listo para guardar en JSON según la especificación del proyecto.
    """
    totales_promedios = calcular_totales_y_promedios(matriz_consumo)
    pico = encontrar_pico(matriz_consumo)
    umbral = evaluar_umbral(matriz_consumo, valor_umbral)
    proyeccion = proyectar_ahorro(matriz_consumo, porcentaje_ahorro)
    horas_mas_caras = calcular_horas_mas_caras(matriz_consumo, tarifa)

    return {
        "edificio": edificio,
        "total_semana": totales_promedios["total_semana"],
        "total_por_dia": totales_promedios["total_por_dia"],
        "promedio_por_hora": totales_promedios["promedio_por_hora"],
        "pico": pico,
        "umbral": umbral,
        "proyeccion": proyeccion,
        "hora_mas_cara_por_dia": horas_mas_caras
    }


def guardar_resumen(ruta_archivo, datos_resumen):
    """
    Guarda los resultados del análisis en un archivo JSON con formato ordenado.

    Parámetros:
        ruta_archivo (str): Ruta donde se guardará el archivo JSON.
        datos_resumen (dict): Datos que serán serializados.

    Retorna:
        bool: True si la operación fue exitosa.
    """
    with open(ruta_archivo, "w", encoding="utf-8") as archivo:
        json.dump(datos_resumen, archivo, indent=2, ensure_ascii=False)
    return True
