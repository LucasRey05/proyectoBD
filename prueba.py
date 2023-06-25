import mysql.connector

# Establecer la conexión con la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="virtual_menu"
)
4
# Clase para representar los elementos del menú
class MenuItem:
    def __init__(self, id, nombre, precio, descripcion, categoria):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.categoria = categoria

# Función para cargar los elementos del menú de una categoría específica
def cargar_menu(categoria):
    cursor = mydb.cursor()
    query = "SELECT id, nombre, precio, descripcion, categoria FROM menu WHERE categoria = %s"
    cursor.execute(query, (categoria,))
    menu_items = []
    for id, nombre, precio, descripcion, categoria in cursor:
        item = MenuItem(id, nombre, precio, descripcion, categoria)
        menu_items.append(item)
    return menu_items

# Función para mostrar los elementos del menú de una categoría específica
def mostrar_menu(menu):
    print("---- Menú ----")
    for i, item in enumerate(menu):
        print(f"{i+1}. {item.nombre} - $ {item.precio}")
    print()

# Función para agregar un elemento al menú
def agregar_elemento():
    nombre = input("Ingrese el nombre del elemento: ")
    precio = float(input("Ingrese el precio del elemento: "))
    descripcion = input("Ingrese la descripción del elemento: ")
    categoria = input("Ingrese la categoría del elemento: ")

    cursor = mydb.cursor()
    query = "INSERT INTO menu (nombre, precio, descripcion, categoria) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nombre, precio, descripcion, categoria))
    mydb.commit()
    print("El elemento ha sido agregado al menú.")

# Función para modificar un elemento del menú
def modificar_elemento():
    id = int(input("Ingrese el ID del elemento que desea modificar: "))
    nombre = input("Ingrese el nuevo nombre del elemento: ")
    precio = float(input("Ingrese el nuevo precio del elemento: "))
    descripcion = input("Ingrese la nueva descripción del elemento: ")
    categoria = input("Ingrese la nueva categoría del elemento: ")

    cursor = mydb.cursor()
    query = "UPDATE menu SET nombre = %s, precio = %s, descripcion = %s, categoria = %s WHERE id = %s"
    cursor.execute(query, (nombre, precio, descripcion, categoria, id))
    mydb.commit()
    print("El elemento ha sido modificado.")

# Función para eliminar un elemento del menú
def eliminar_elemento():
    id = int(input("Ingrese el ID del elemento que desea eliminar: "))

    cursor = mydb.cursor()
    query = "DELETE FROM menu WHERE id = %s"
    cursor.execute(query, (id,))
    mydb.commit()
    print("El elemento ha sido eliminado.")

# Función para mostrar los elementos del menú en una categoría específica
def mostrar_elementos_categoria():
    categoria = input("Ingrese la categoría que desea mostrar: ")
    menu = cargar_menu(categoria)
    mostrar_menu(menu)

# Función para mostrar todos los elementos del menú
def mostrar_todos_elementos():
    cursor = mydb.cursor()
    cursor.execute("SELECT id, nombre, precio, descripcion, categoria FROM menu")
    menu_items = []
    for id, nombre, precio, descripcion, categoria in cursor:
        item = MenuItem(id, nombre, precio, descripcion, categoria)
        menu_items.append(item)
    mostrar_menu(menu_items)

# Menú principal
while True:
    print("----- Menú Principal -----")
    print("1. Agregar elemento")
    print("2. Modificar elemento")
    print("3. Eliminar elemento")
    print("4. Mostrar elementos de una categoría")
    print("5. Mostrar todos los elementos")
    print("6. Salir")

    opcion = int(input("Ingrese una opción: "))

    if opcion == 1:
        agregar_elemento()
    elif opcion == 2:
        modificar_elemento()
    elif opcion == 3:
        eliminar_elemento()
    elif opcion == 4:
        mostrar_elementos_categoria()
    elif opcion == 5:
        mostrar_todos_elementos()
    elif opcion == 6:
        break
    else:
        print("Opción inválida. Intente nuevamente.")

# Cerrar la conexión con la base de datos
mydb.close()
