#def mostrar_menu():
opcion=0    
while opcion != 5:
        print("Bienvenido al Menu virtual")
        print("----------- MENÚ ---------")
        print("1. Comida Principal")
        print("2. Acompañamiento")
        print("3. Bebida")
        print("4. Postre")
        print("5. Salir")

        opcion = int(input("Indica el número de opción a seleccionar: "))


if opcion == 1:
    print("Seleccionó opción de SALIR, Adios.")    
elif opcion == 2:
     print("Seleccionó opción de SALIR, Adios.") 
elif opcion == 3:
     print("Seleccionó opción de SALIR, Adios.")
else:
    print("Opción inválida.Por favor, selecciona una opción válida.")    




class ComidaPrincipal:
    def __init__(self, nombre, precio, descripcion):
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion



    def __str__(self):
        return f"Su plato sera {self.nombre}, este cuesta {self.precio}, {self.descripcion}."
    
plato1 = ComidaPrincipal("Hamburguesa", "$3000", "Hamburguesa con queso")
plato2 = ComidaPrincipal("Milanesa", "$2400", "Milanga napolitana")
plato3 = ComidaPrincipal("Pizza", "$1500", "Pizzita con quesito")

print(plato1)
print(plato2)
print(plato3)
