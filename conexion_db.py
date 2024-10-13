# Conexion de base de datos
import sqlite3
from sqlite3 import Error


ruta_db = "/productos.db"

def crear_conexion(ruta_db):
    """Crear una conexión a la base de datos SQLite especificada por la ruta_db"""
    conexion = None
    try:
        conexion = sqlite3.connect(ruta_db)
        print(f"conexion establecida con exito a la base de datos {ruta_db}")
    except Error as e:
        print(f"No se pudo establecer la conexion con la base de datos {e}")
    return conexion

def cerrar_conexion(conexion):
    """Cerrar la conexión a la base de datos SQLite"""
    if conexion:
        conexion.close()
        print("Conexión cerrada")        
    