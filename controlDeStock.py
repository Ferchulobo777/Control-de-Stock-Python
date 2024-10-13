from rich import print
from rich.table import Table
from constantes import cian
from utils import sep, guion, espacio
from conexion_db import crear_conexion, cerrar_conexion
from servicios_db import crear_tabla_productos, agregar_producto, obtener_productos, actualizar_producto, eliminar_producto, buscar_producto_por_nombre

# Conectar a la base de datos
conexion = crear_conexion("products.db")

# Crear la tabla de productos si no existe
crear_tabla_productos(conexion)

# Definir el menú
menu = "Menu de Gestión de Productos"

# Definir el ancho total (por ejemplo, 60 caracteres)
ancho_total = 60

# Calcular el espacio que sobra para centrar el menú
menu_longitud = len(menu)
margen_lateral = (ancho_total - menu_longitud - 2) // 2  # Espacios a cada lado del menú (-2 para los asteriscos)

# Crear el separador (una línea completa de 'sep')
linea_separador = sep * ancho_total

def mostrar_menu():
    # Imprimir el menú con el separador
    print(f"[{cian}]{linea_separador}[/{cian}]")  # Separador superior
    print(f"[{cian}]{sep * margen_lateral} {menu} {sep * margen_lateral}[/{cian}]")  # Menú centrado con asteriscos
    print(f"[{cian}]{linea_separador}[/{cian}]\n")  # Separador inferior

    # Opciones del menú
    print(f"[{cian}]1. REGISTRO: Alta de productos nuevos[/{cian}]")
    print(f"[{cian}]2. VISUALIZACIÓN: Consulta de datos de los productos[/{cian}]")
    print(f"[{cian}]3. ACTUALIZACIÓN: Modificar la cantidad de stock de un producto[/{cian}]")
    print(f"[{cian}]4. ELIMINACIÓN: Dar de baja productos[/{cian}]")
    print(f"[{cian}]5. BUSCAR: Búsqueda por nombre del producto[/{cian}]")
    print(f"[{cian}]6. REPORTE DE BAJO STOCK: Lista de Productos con cantidad mínima o baja[/{cian}]")
    print(f"[{cian}]7. SALIR[/{cian}]")
    print(f"[{cian}]Por favor, selecciona una opción: [/{cian}]")

def visualizar_productos():
    """Visualizar los productos en la base de datos"""
    productos = obtener_productos(conexion)
    
    # Crear una tabla con Rich
    table = Table(title="Productos en la Base de Datos")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nombre", justify="left", style="magenta")
    table.add_column("Precio", justify="right", style="green")
    table.add_column("Cantidad", justify="right", style="yellow")

    if productos:
        for producto in productos:
            table.add_row(str(producto[0]), producto[1], f"${producto[2]:.2f}", str(producto[3]))
        print(table)
    else:
        print("No hay productos registrados.")

def registro_producto():
    """Registrar un producto nuevo"""
    name = input("Nombre del producto: ")
    price = float(input("Precio del producto: "))
    quantity = int(input("Cantidad del producto: "))
    agregar_producto(conexion, name, price, quantity)

def actualizar_stock():
    """Actualizar el stock de un producto"""
    product_id = int(input("ID del producto a actualizar: "))
    name = input("Nuevo nombre del producto: ")
    price = float(input("Nuevo precio del producto: "))
    quantity = int(input("Nueva cantidad del producto: "))
    actualizar_producto(conexion, product_id, name, price, quantity)

def eliminar_producto_db():
    """Eliminar un producto de la base de datos"""
    product_id = int(input("ID del producto a eliminar: "))
    eliminar_producto(conexion, product_id)

def buscar_producto():
    """Buscar un producto por nombre"""
    nombre = input("Introduce el nombre del producto que deseas buscar: ").strip()
    producto = buscar_producto_por_nombre(conexion, nombre)
    
    if producto:
        # Mostrar el producto encontrado en formato de tabla
        table = Table(title=f"Resultado de la búsqueda para '{nombre}'")
        table.add_column("ID", justify="center", style="cyan", no_wrap=True)
        table.add_column("Name", justify="left", style="magenta")  # Cambié "Nombre" por "Name"
        table.add_column("Precio", justify="right", style="green")
        table.add_column("Cantidad", justify="right", style="yellow")
        
        table.add_row(str(producto[0]), producto[1], f"${producto[2]:.2f}", str(producto[3]))
        print(table)
    else:
        print(f"No se encontró ningún producto con el nombre '{nombre}'.")


def reporte_bajo_stock(umbral=5):
    """Mostrar productos con stock menor o igual a un umbral definido"""
    productos = obtener_productos(conexion)
    
    # Crear una tabla para los productos con bajo stock
    table = Table(title=f"Productos con stock menor o igual a {umbral}")
    table.add_column("ID", justify="center", style="cyan", no_wrap=True)
    table.add_column("Nombre", justify="left", style="magenta")
    table.add_column("Stock", justify="right", style="yellow")

    productos_bajo_stock = [producto for producto in productos if producto[3] <= umbral]

    if productos_bajo_stock:
        for producto in productos_bajo_stock:
            table.add_row(str(producto[0]), producto[1], str(producto[3]))
        print(table)
    else:
        print(f"No hay productos con stock menor o igual a {umbral}.")

# Inicializar una variable para controlar la salida
salir = False

# Iniciar el bucle del menú
while not salir:
    mostrar_menu()

    try:
        seleccion = int(input())  # Convertir la entrada a entero

        # Manejar las diferentes opciones
        if seleccion == 1:
            print("Has seleccionado REGISTRO.")
            registro_producto()  # Registrar un producto nuevo
        elif seleccion == 2:
            print("Has seleccionado VISUALIZACIÓN.")
            visualizar_productos()  # Ver todos los productos
        elif seleccion == 3:
            print("Has seleccionado ACTUALIZACIÓN.")
            actualizar_stock()  # Actualizar un producto
        elif seleccion == 4:
            print("Has seleccionado ELIMINACIÓN.")
            eliminar_producto_db()  # Eliminar un producto
        elif seleccion == 5:
            print("Has seleccionado LISTADO.")
            buscar_producto()  # Listar todos los productos
        elif seleccion == 6:
            print("Has seleccionado REPORTE DE BAJO STOCK.")
            reporte_bajo_stock()
            # Lógica para reporte de bajo stock (puedes implementar esta función)
        elif seleccion == 7:
            print("Saliendo del programa.")
            salir = True  # Cambia la variable para salir del bucle
        else:
            print("Por favor, selecciona una opción válida entre 1 y 7.")
    except ValueError:
        print("No escribiste una opción válida. Por favor, ingresa un número.")

# Cerrar la conexión a la base de datos al salir
cerrar_conexion(conexion)
