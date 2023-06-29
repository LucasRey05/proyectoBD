import mysql.connector

# Establecer la conexión con la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restaurante"
)

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

# Clase para representar los empleados
class EmpleadosItem:
    def __init__(self, id, nombres, apellidos, cargo, salario, telefono, correo_electronico):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.cargo = cargo
        self.salario = salario
        self.telefono = telefono
        self.correo_electronico = correo_electronico

# Función para cargar los empleados de una categoría específica
def cargar_empleados(categoria):
    cursor = mydb.cursor()
    query = "SELECT id, nombres, apellidos, cargo, salario, telefono, correo_electronico FROM empleados WHERE cargo = %s"
    cursor.execute(query, (categoria,))
    empleados_items = []
    for id, nombres, apellidos, cargo, salario, telefono, correo_electronico in cursor:
        item = EmpleadosItem(id, nombres, apellidos, cargo, salario, telefono, correo_electronico)
        empleados_items.append(item)
    return empleados_items

# Función para mostrar los empleados de una categoría específica
def mostrar_empleados(empleados):
    print("---- Empleados ----")
    for i, item in enumerate(empleados):
        print(f"{i+1}. {item.nombres} {item.apellidos} - Cargo: {item.cargo} - Salario: {item.salario}")
    print()

# Función para agregar un empleado
def agregar_empleado():
    nombres = input("Ingrese los nombres del empleado: ")
    apellidos = input("Ingrese los apellidos del empleado: ")
    cargo = input("Ingrese el cargo del empleado: ")
    salario = float(input("Ingrese el salario del empleado: "))
    telefono = input("Ingrese el número de teléfono del empleado: ")
    correo_electronico = input("Ingrese el correo electrónico del empleado: ")

    cursor = mydb.cursor()
    query = "INSERT INTO empleados (nombres, apellidos, cargo, salario, telefono, correo_electronico) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (nombres, apellidos, cargo, salario, telefono, correo_electronico))
    mydb.commit()
    print("El empleado ha sido agregado.")

# Función para modificar un empleado
def modificar_empleado():
    id = int(input("Ingrese el ID del empleado que desea modificar: "))
    cargo = input("Ingrese el nuevo cargo del empleado: ")
    salario = float(input("Ingrese el nuevo salario del empleado: "))
    telefono = input("Ingrese el nuevo número de teléfono del empleado: ")
    correo_electronico = input("Ingrese el nuevo correo electrónico del empleado: ")

    cursor = mydb.cursor()
    query = "UPDATE empleados SET cargo = %s, salario = %s, telefono = %s, correo_electronico = %s WHERE id = %s"
    cursor.execute(query, (cargo, salario, telefono, correo_electronico, id))
    mydb.commit()
    print("El empleado ha sido modificado.")

# Función para eliminar un empleado
def eliminar_empleado():
    id = int(input("Ingrese el ID del empleado que desea eliminar: "))

    cursor = mydb.cursor()
    query = "DELETE FROM empleados WHERE id = %s"
    cursor.execute(query, (id,))
    mydb.commit()
    print("El empleado ha sido eliminado.")

# Función para mostrar los empleados de un cargo específico
def mostrar_empleados_cargo():
    cargo = input("Ingrese el cargo del empleado: ")
    empleados = cargar_empleados(cargo)
    mostrar_empleados(empleados)

# Función para mostrar todos los empleados
def mostrar_todos_empleados():
    cursor = mydb.cursor()
    cursor.execute("SELECT id, nombres, apellidos, cargo, salario, telefono, correo_electronico FROM empleados")
    empleados_items = []
    for id, nombres, apellidos, cargo, salario, telefono, correo_electronico in cursor:
        item = EmpleadosItem(id, nombres, apellidos, cargo, salario, telefono, correo_electronico)
        empleados_items.append(item)
    mostrar_empleados(empleados_items)


# Menú principal
while True:
    print("----- Menú Principal -----")
    print("1. Agregar elemento")
    print("2. Modificar elemento")
    print("3. Eliminar elemento")
    print("4. Mostrar elementos de una categoría")
    print("5. Mostrar todos los elementos")
    print("----- Menú Empleados -----")
    print("6. Agregar empleado")
    print("7. Modificar empleado")
    print("8. Eliminar empleado")
    print("9. Mostrar empleados de un cargo")
    print("10. Mostrar todos los empleados")
    print("11. Salir")

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
        agregar_empleado()
    elif opcion == 7:
        modificar_empleado()
    elif opcion == 8:
        eliminar_empleado()
    elif opcion == 9:
        mostrar_empleados_cargo()
    elif opcion == 10:
        mostrar_todos_empleados()
    elif opcion == 11:
        break
    else:
        print("Opción inválida. Intente nuevamente.")

# Cerrar la conexión con la base de datos
mydb.close()
