"""
Script de verificación oficial para el caso de prueba 3x4.
Verifica que las funciones de logica.py cumplan con los resultados de referencia del profesor Alex.
"""

import sys

def ejecutar_pruebas():
    try:
        import logica
    except ImportError:
        print("[ERROR] No se pudo importar logica.py. Asegúrate de que el archivo existe.")
        return False

    matriz_prueba = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [2, 2, 2, 2]
    ]

    print("=" * 60)
    print("INICIANDO VERIFICACIÓN DEL CASO DE PRUEBA 3x4 (PROFESOR ALEX)")
    print("=" * 60)

    todas_pasaron = True

    # 1. Total por día: 10, 26 y 8 kWh
    totales_promedios = logica.calcular_totales_y_promedios(matriz_prueba)
    totales_dia = totales_promedios["total_por_dia"]
    totales_esperados = [10, 26, 8]
    if [round(x, 2) for x in totales_dia] == totales_esperados:
        print(f"[OK] Total por día: {totales_dia} coincide con {totales_esperados}")
    else:
        print(f"[FALLO] Total por día obtenido: {totales_dia}, esperado: {totales_esperados}")
        todas_pasaron = False

    # 2. Promedios por hora: 2.67, 3.33, 4.00 y 4.67 kWh
    promedios_hora = [round(x, 2) for x in totales_promedios["promedio_por_hora"]]
    promedios_esperados = [2.67, 3.33, 4.00, 4.67]
    if promedios_hora == promedios_esperados:
        print(f"[OK] Promedio por hora: {promedios_hora} coincide con {promedios_esperados}")
    else:
        print(f"[FALLO] Promedio por hora obtenido: {promedios_hora}, esperado: {promedios_esperados}")
        todas_pasaron = False

    # 3. Pico: día 2, hora 4, 8 kWh (En índices base 0: día 1, hora 3)
    pico = logica.encontrar_pico(matriz_prueba)
    dia_humano = pico["dia"] + 1
    hora_humano = pico["hora"] + 1
    valor_pico = pico["valor"]
    if dia_humano == 2 and hora_humano == 4 and valor_pico == 8:
        print(f"[OK] Pico: Día {dia_humano}, Hora {hora_humano}, Valor {valor_pico} kWh coincide con lo esperado")
    else:
        print(f"[FALLO] Pico obtenido: Día {dia_humano}, Hora {hora_humano}, Valor {valor_pico}. Esperado: Día 2, Hora 4, Valor 8")
        todas_pasaron = False

    # 4. Umbral 5 kWh: 3 celdas (día 2, horas 2, 3 y 4, con valores 6, 7 y 8)
    res_umbral_5 = logica.evaluar_umbral(matriz_prueba, 5.0)
    cant_5 = res_umbral_5["cantidad"]
    celdas_5 = res_umbral_5["horas_sobre_umbral"]
    # Convertimos a coordenadas 1-indexadas para contrastar con el enunciado
    celdas_5_humanas = [(c["dia"] + 1, c["hora"] + 1, c["valor"]) for c in celdas_5]
    celdas_5_esperadas = [(2, 2, 6), (2, 3, 7), (2, 4, 8)]

    if cant_5 == 3 and celdas_5_humanas == celdas_5_esperadas:
        print(f"[OK] Umbral 5 kWh: {cant_5} celdas {celdas_5_humanas} coincide con {celdas_5_esperadas}")
    else:
        print(f"[FALLO] Umbral 5 kWh obtenido: {cant_5} celdas {celdas_5_humanas}, esperado: 3 celdas {celdas_5_esperadas}")
        todas_pasaron = False

    # 5. Umbral 100 kWh: ninguna celda
    res_umbral_100 = logica.evaluar_umbral(matriz_prueba, 100.0)
    if res_umbral_100["cantidad"] == 0 and len(res_umbral_100["horas_sobre_umbral"]) == 0:
        print("[OK] Umbral 100 kWh: 0 celdas superan el umbral (correcto)")
    else:
        print(f"[FALLO] Umbral 100 kWh: se obtuvieron celdas {res_umbral_100}")
        todas_pasaron = False

    # 6. Proyección x0.5 (Ahorro 50%): el día 2 queda 2.5, 3.0, 3.5 y 4.0, y datos originales intactos
    copia_antes = [fila[:] for fila in matriz_prueba]
    res_proy = logica.proyectar_ahorro(matriz_prueba, 50.0)
    fila_2_proy = [round(x, 1) for x in res_proy["consumo_proyectado"][1]]
    esperado_fila_2 = [2.5, 3.0, 3.5, 4.0]

    datos_intactos = (matriz_prueba == copia_antes)

    if fila_2_proy == esperado_fila_2 and datos_intactos and res_proy["factor"] == 0.5:
        print(f"[OK] Proyección x0.5: Fila 2 proyectada {fila_2_proy} coincide con {esperado_fila_2} y la matriz original quedó intacta.")
    else:
        print(f"[FALLO] Proyección x0.5: Fila 2={fila_2_proy} (esperado {esperado_fila_2}), datos intactos={datos_intactos}")
        todas_pasaron = False

    print("=" * 60)
    if todas_pasaron:
        print(">> RESULTADO: ¡TODAS LAS PRUEBAS DEL PROFESOR PASARON CON ÉXITO! <<")
    else:
        print(">> RESULTADO: HUBO FALLOS EN LA VERIFICACIÓN <<")
    print("=" * 60)
    return todas_pasaron

if __name__ == "__main__":
    exito = ejecutar_pruebas()
    sys.exit(0 if exito else 1)
