CREATE DATABASE IF NOT EXISTS virtual_menu;

-- Usar la base de datos
USE virtual_menu;

-- Crear la tabla "menu"
CREATE TABLE IF NOT EXISTS menu (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100),
  precio DECIMAL(10, 2),
  descripcion VARCHAR(255),
  categoria VARCHAR(20)
);

-- Insertar datos de ejemplo
INSERT INTO menu (nombre, precio, descripcion, categoria)
VALUES
    ('Hamburguesa', 9.99, 'Deliciosa hamburguesa con queso', 'Comida Principal'),
    ('Pizza', 12.99, 'Pizza de pepperoni con masa crujiente', 'Comida Principal'),
    ('Papas Fritas', 3.99, 'Papas fritas doradas y crujientes', 'Acompañamiento'),
    ('Ensalada César', 6.99, 'Ensalada fresca con pollo a la parrilla', 'Acompañamiento'),
    ('Refresco', 1.99, 'Bebida refrescante de cola', 'Bebida'),
    ('Agua Mineral', 0.99, 'Agua purificada sin gas', 'Bebida'),
    ('Brownie', 4.99, 'Delicioso brownie de chocolate con nueces', 'Postre'),
    ('Helado de Vainilla', 3.99, 'Suave helado de vainilla con toppings', 'Postre');

USE virtual_menu;

SELECT * FROM menu;