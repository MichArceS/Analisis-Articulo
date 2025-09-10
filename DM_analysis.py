import os
import json
from datetime import datetime

def GetAll():
    with open("DM.json", 'r') as f:
        data = json.load(f)

    final_dict = {}

    for key in data:
        id_canal = data[key]
        for subdir, dirs, files in os.walk("Mensajes_Iria\\"):
            tmp = subdir.split("\\")[-1][1:]
            if str(id_canal) == tmp:
                with open(subdir + "\messages.json", 'r', encoding='utf-8') as f_2:
                    data_2 = json.load(f_2)
                    for element in data_2:
                        tmp_dict = {}
                        tmp_dict["Timestamp"] = element["Timestamp"]
                        tmp_dict["Content"] = element["Contents"]
                        final_dict[element["ID"]] = tmp_dict

    print(len(final_dict))

    with open("DM_messages.json", "w") as json_file:
        json.dump(final_dict, json_file, indent=4) # indent for pretty-printing


def filtrar_mensajes_dm_por_rango(archivo_entrada: str, archivo_salida: str, fecha_inicio: str, fecha_fin: str):
    try:
        # Cargar los datos del archivo JSON
        with open(archivo_entrada, 'r', encoding='utf-8') as file:
            mensajes_dm = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_entrada}' no se encontró.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo '{archivo_entrada}' no es un JSON válido.")
        return

    # Convertir las cadenas de fecha a objetos datetime
    try:
        fecha_inicio_dt = datetime.strptime(fecha_inicio, '%Y-%m-%d')
        fecha_fin_dt = datetime.strptime(fecha_fin, '%Y-%m-%d')
    except ValueError as e:
        print(f"Error en el formato de fecha. Use 'YYYY-MM-DD'. Detalle: {e}")
        return

    mensajes_filtrados = {}

    # Iterar sobre los valores del diccionario
    for mensaje_id, mensaje_data in mensajes_dm.items():
        # Obtener y parsear la fecha del mensaje
        # El formato de la fecha es 'YYYY-MM-DD HH:MM:SS'
        fecha_mensaje_str = mensaje_data.get('Timestamp', '').split(' ')[0]
        
        try:
            fecha_mensaje_dt = datetime.strptime(fecha_mensaje_str, '%Y-%m-%d')
        except (ValueError, KeyError):
            # Ignorar mensajes sin fecha o con formato incorrecto
            continue

        # Verificar si la fecha está dentro del rango
        if fecha_inicio_dt <= fecha_mensaje_dt <= fecha_fin_dt:
            mensajes_filtrados[mensaje_id] = mensaje_data

    # Guardar los mensajes filtrados en un nuevo archivo JSON
    try:
        with open(archivo_salida, 'w', encoding='utf-8') as outfile:
            json.dump(mensajes_filtrados, outfile, indent=4, ensure_ascii=False)
        print(f"Se encontraron {len(mensajes_filtrados)} mensajes en el rango de fechas.")
        print(f"Los mensajes filtrados se han guardado exitosamente en '{archivo_salida}'.")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")

archivo_de_entrada = 'DM_messages.json'
archivo_de_salida = 'DM_messages_filtrado.json'

# Define el rango de fechas que deseas
fecha_de_inicio_filtro = '2025-02-01'
fecha_de_fin_filtro = '2025-04-30'

#filtrar_mensajes_dm_por_rango(archivo_de_entrada, archivo_de_salida, fecha_de_inicio_filtro, fecha_de_fin_filtro)

def CountDM(json_DMs):
     with open(json_DMs, 'r', encoding='utf-8') as file:
            mensajes_dm = json.load(file)
            print (len(mensajes_dm))

def contar_mensajes_por_semana_desde_json(nombre_archivo_entrada: str, nombre_archivo_salida: str):
    try:
        with open(nombre_archivo_entrada, 'r', encoding='utf-8') as file:
            mensajes = json.load(file)
    except FileNotFoundError:
        print(f"Error: El archivo de entrada '{nombre_archivo_entrada}' no se encontró.")
        return
    except json.JSONDecodeError:
        print(f"Error: El archivo '{nombre_archivo_entrada}' no es un JSON válido.")
        return

    conteo_semanal = {}
    for mensaje_id, mensaje_data in mensajes.items():
        # Extrae la fecha de la clave 'Timestamp', que tiene el formato 'YYYY-MM-DD HH:MM:SS'
        fecha_str = mensaje_data.get('Timestamp', '').split(' ')[0]
        
        try:
            fecha_mensaje = datetime.strptime(fecha_str, '%Y-%m-%d')
            # Obtiene el número de semana ISO (1 a 52/53)
            semana_iso = fecha_mensaje.isocalendar()[1]
            year = fecha_mensaje.year
            
            # Crea una clave única para la semana y el año
            clave_semana = f"Semana {year}-{semana_iso:02d}"
            
            # Incrementa el contador para la semana correspondiente
            conteo_semanal[clave_semana] = conteo_semanal.get(clave_semana, 0) + 1
            
        except (ValueError, IndexError):
            # Ignora los mensajes con fechas inválidas o sin la clave 'Timestamp'
            continue

    # Guarda el resultado del conteo en el nuevo archivo JSON
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as outfile:
            json.dump(conteo_semanal, outfile, indent=4, ensure_ascii=False)
        print(f"Conteo semanal guardado exitosamente en '{nombre_archivo_salida}'.")
    except Exception as e:
        print(f"Error al guardar el archivo de salida: {e}")

archivo_entrada = 'DM/DM_messages_filtrado_P2.json'
archivo_salida = 'conteo_mensajes_MD_semanal_P2.json'

# Llama a la función para realizar el conteo y guardar el resultado
contar_mensajes_por_semana_desde_json(archivo_entrada, archivo_salida)