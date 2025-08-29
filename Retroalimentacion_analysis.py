import json
from datetime import datetime

def filtrar_mensajes_por_rango_fechas(data: list, fecha_inicio: str, fecha_fin: str) -> list:
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError as e:
        raise ValueError(f"Error en el formato de fecha. Use 'YYYY-MM-DD'. Detalle: {e}")

    mensajes_filtrados = []
    for mensaje in data:
        try:
            fecha_mensaje_str = mensaje.get('fecha', '').split('T')[0]
            autor_mensaje_str = mensaje.get('autor', '')
            fecha_mensaje_dt = datetime.strptime(fecha_mensaje_str, '%Y-%m-%d')
        except (KeyError, ValueError):
            continue  # Ignora mensajes sin fecha o con formato incorrecto

        if fecha_inicio_dt <= fecha_mensaje_dt <= fecha_fin_dt and autor_mensaje_str == "iriaec.":
            mensajes_filtrados.append(mensaje)

    return mensajes_filtrados

def guardar_json_en_archivo(data: list, nombre_archivo: str):
    try:
        with open(nombre_archivo, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)
        print(f"Los datos se han guardado exitosamente en '{nombre_archivo}'.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")


fecha_de_inicio = '2025-02-01'
fecha_de_fin = '2025-04-30'
nombre_archivo_salida = 'retroalimentacion_P2.json'

f = open('retroalimentacion_mensajes.json')
data = json.load(f)

# Usa las funciones
mensajes_filtrados = filtrar_mensajes_por_rango_fechas(data, fecha_de_inicio, fecha_de_fin)

guardar_json_en_archivo(mensajes_filtrados, nombre_archivo_salida)


def conteo_retroalimentacion(nombre_archivo_entrada: str, nombre_archivo_salida: str):
    try:
        with open(nombre_archivo_entrada, 'r', encoding='utf-8') as file:
            mensajes = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{nombre_archivo_entrada}' no se encontró.")
        return False
    except json.JSONDecodeError:
        print(f"Error: El archivo '{nombre_archivo_entrada}' no es un JSON válido.")
        return False

    conteo_semanal = {}
    for mensaje in mensajes:
        fecha_str = mensaje.get('fecha')
        if not fecha_str:
            continue
        
        try:
            fecha_mensaje = datetime.fromisoformat(fecha_str.split('T')[0])
            # La semana ISO 8601 (del 1 al 52/53) y el año
            semana_iso = fecha_mensaje.isocalendar()[1]
            year = fecha_mensaje.year
            
            clave_semana = f"Semana {year}-{semana_iso:02d}"
            
            conteo_semanal[clave_semana] = conteo_semanal.get(clave_semana, 0) + 1
            
        except (ValueError, IndexError):
            # Ignorar mensajes con fechas inválidas
            continue

    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as outfile:
            json.dump(conteo_semanal, outfile, indent=4, ensure_ascii=False)
        print(f"Conteo semanal guardado exitosamente en '{nombre_archivo_salida}'.")
        return True
    except Exception as e:
        print(f"Error al guardar el archivo de salida: {e}")
        return False

conteo_retroalimentacion("retroalimentacion_P2.json", "conteo_retroalimentacion_P2.json")