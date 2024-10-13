from sqlite3 import Error


def crear_tabla_productos(conexion):
    """Crear la tabla productos si no existe"""
    try:
        cursor = conexion.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS products(
                           product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           price REAL NOT NULL,
                           quantity INT NOT NULL
                           );
                           """)
        conexion.commit()
        print("Tabla 'products' creada correctamente.")
    except Error as e:
        print(f"Error al crear la tabla: {e}")

        
        
def agregar_producto(conexion, name, price, quantity):
    """Agregar un producto a la base de datos"""
    try:
        cursor = conexion.cursor()
        # Se debe pasar una tupla con los valores
        cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", 
                       (name, price, quantity))
        conexion.commit()
        print("Producto agregado correctamente.")    
    except Error as e:
        print(f"Error al agregar producto: {e}")

                   
        
def obtener_productos(conexion):
    """Obtener los productos de la base de datos"""
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM products")
        productos = cursor.fetchall()
        return productos
    except Error as e:
        print(f"Error al obtener productos: {e}")
        return []

   
def actualizar_producto(conexion, product_id, name, price, quantity):
    """Actualizar todos los campos de un producto excepto el id"""
    try:
        cursor = conexion.cursor()
        # Usar el nombre correcto de la tabla
        cursor.execute("""
            UPDATE products 
            SET name = ?, price = ?, quantity = ?
            WHERE product_id = ?
        """, (name, price, quantity, product_id))
        conexion.commit()  # Confirmar la transacción
        print("Producto actualizado correctamente.")
    except Error as e:
        print(f"Error al actualizar el producto: {e}")

def eliminar_producto(conexion, id_product):
    """Eliminar un producto de la base de Datos"""
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM products WHERE product_id = ?", (id_product,))
        conexion.commit()
        print("Producto eliminado correctamente.")
    except Error as e:
        print(f"Error al eliminar el producto: {e}")
        
def buscar_producto_por_nombre(conexion, nombre):
    """Buscar un producto por su campo 'name' sin distinguir mayúsculas o minúsculas"""
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)", (f"%{nombre}%",))
    return cursor.fetchone()             