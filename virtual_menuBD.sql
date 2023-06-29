CREATE DATABASE IF NOT EXISTS restaurante;

-- Usar la base de datos
USE restaurante;

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
    ('Helado de Vainilla', 3.99, 'Suave helado de vainilla con toppings', 'Postre'),
    ('Pollo a la Parrilla', 10.99, 'Pollo jugoso a la parrilla con hierbas', 'Comida Principal'),
    ('Tacos', 8.99, 'Tacos de carne con salsa picante', 'Comida Principal'),
    ('Arroz Blanco', 2.99, 'Arroz blanco cocido al vapor', 'Acompañamiento'),
    ('Ensalada de Frutas', 5.99, 'Ensalada fresca con frutas de temporada', 'Acompañamiento'),
    ('Jugo de Naranja', 2.49, 'Jugo de naranja recién exprimido', 'Bebida'),
    ('Tarta de Manzana', 4.49, 'Tarta de manzana casera con canela', 'Postre'),
    ('Flan', 3.49, 'Flan cremoso con caramelo', 'Postre'),
    ('Cerveza', 2.99, 'Cerveza rubia fría', 'Bebida'),
    ('Cheesecake', 4.99, 'Cheesecake cremoso con salsa de frutas', 'Postre'),
    ('Mousse de Chocolate', 3.99, 'Mousse de chocolate con crema batida', 'Postre');

--USE restaurante;
SELECT * FROM menu;