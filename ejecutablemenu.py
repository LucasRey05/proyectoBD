import tkinter as tk
import mysql.connector

# Establecer la conexión con la base de datos
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="virtual_menu"
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
    menu_text.delete("1.0", tk.END)
    menu_text.insert(tk.END, "---- Menú ----\n")
    for i, item in enumerate(menu):
        menu_text.insert(tk.END, f"{i+1}. {item.nombre} - $ {item.precio}\n")
    menu_text.insert(tk.END, "\n")

# Función para agregar un elemento al menú
def agregar_elemento():
    nombre = nombre_entry.get()
    precio = float(precio_entry.get())
    descripcion = descripcion_entry.get()
    categoria = categoria_entry.get()

    cursor = mydb.cursor()
    query = "INSERT INTO menu (nombre, precio, descripcion, categoria) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (nombre, precio, descripcion, categoria))
    mydb.commit()
    status_label.config(text="El elemento ha sido agregado al menú.")

# Función para modificar un elemento del menú
def modificar_elemento():
    id = int(id_entry.get())
    nombre = nombre_entry.get()
    precio = float(precio_entry.get())
    descripcion = descripcion_entry.get()
    categoria = categoria_entry.get()

    cursor = mydb.cursor()
    query = "UPDATE menu SET nombre = %s, precio = %s, descripcion = %s, categoria = %s WHERE id = %s"
    cursor.execute(query, (nombre, precio, descripcion, categoria, id))
    mydb.commit()
    status_label.config(text="El elemento ha sido modificado.")

# Función para eliminar un elemento del menú
def eliminar_elemento():
    id = int(id_entry.get())

    cursor = mydb.cursor()
    query = "DELETE FROM menu WHERE id = %s"
    cursor.execute(query, (id,))
    mydb.commit()
    status_label.config(text="El elemento ha sido eliminado.")

# Función para mostrar los elementos del menú en una categoría específica
def mostrar_elementos_categoria():
    categoria = categoria_entry.get()
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

# Crear la ventana principal
window = tk.Tk()
window.title("Virtual Menu")

# Crear los widgets
id_label = tk.Label(window, text="ID:")
id_entry = tk.Entry(window)
nombre_label = tk.Label(window, text="Nombre:")
nombre_entry = tk.Entry(window)
precio_label = tk.Label(window, text="Precio:")
precio_entry = tk.Entry(window)
descripcion_label = tk.Label(window, text="Descripción:")
descripcion_entry = tk.Entry(window)
categoria_label = tk.Label(window, text="Categoría:")
categoria_entry = tk.Entry(window)
agregar_button = tk.Button(window, text="Agregar", command=agregar_elemento)
modificar_button = tk.Button(window, text="Modificar", command=modificar_elemento)
eliminar_button = tk.Button(window, text="Eliminar", command=eliminar_elemento)
mostrar_categoria_button = tk.Button(window, text="Mostrar elementos de una categoría", command=mostrar_elementos_categoria)
mostrar_todos_button = tk.Button(window, text="Mostrar todos los elementos", command=mostrar_todos_elementos)
status_label = tk.Label(window, text="")
menu_text = tk.Text(window)

# Posicionar los widgets en la ventana
id_label.grid(row=0, column=0, sticky="E")
id_entry.grid(row=0, column=1)
nombre_label.grid(row=1, column=0, sticky="E")
nombre_entry.grid(row=1, column=1)
precio_label.grid(row=2, column=0, sticky="E")
precio_entry.grid(row=2, column=1)
descripcion_label.grid(row=3, column=0, sticky="E")
descripcion_entry.grid(row=3, column=1)
categoria_label.grid(row=4, column=0, sticky="E")
categoria_entry.grid(row=4, column=1)
agregar_button.grid(row=5, column=0, columnspan=2)
modificar_button.grid(row=6, column=0, columnspan=2)
eliminar_button.grid(row=7, column=0, columnspan=2)
mostrar_categoria_button.grid(row=8, column=0, columnspan=2)
mostrar_todos_button.grid(row=9, column=0, columnspan=2)
status_label.grid(row=10, column=0, columnspan=2)
menu_text.grid(row=11, column=0, columnspan=2)

# Menú principal
menu_text.insert(tk.END, "----- Menú Principal -----\n")
menu_text.insert(tk.END, "1. Agregar elemento\n")
menu_text.insert(tk.END, "2. Modificar elemento\n")
menu_text.insert(tk.END, "3. Eliminar elemento\n")
menu_text.insert(tk.END, "4. Mostrar elementos de una categoría\n")
menu_text.insert(tk.END, "5. Mostrar todos los elementos\n")
menu_text.insert(tk.END, "6. Salir\n")

# Función para manejar la opción seleccionada del menú principal
def seleccionar_opcion():
    opcion = int(opcion_entry.get())

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
        window.destroy()
    else:
        status_label.config(text="Opción inválida. Intente nuevamente.")

opcion_label = tk.Label(window, text="Opción:")
opcion_entry = tk.Entry(window)
opcion_button = tk.Button(window, text="Seleccionar", command=seleccionar_opcion)

opcion_label.grid(row=12, column=0, sticky="E")
opcion_entry.grid(row=12, column=1)
opcion_button.grid(row=13, column=0, columnspan=2)

# Ejecutar la ventana
window.mainloop()

# Cerrar la conexión con la base de datos
mydb.close()
