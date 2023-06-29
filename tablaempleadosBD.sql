CREATE DATABASE IF NOT EXISTS restaurante;

-- Usar la base de datos
USE restaurante;



-- Crear la tabla "empleados"
CREATE TABLE IF NOT EXISTS empleados (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombres VARCHAR(50),
  apellidos VARCHAR(50),
  cargo VARCHAR(50),
  salario DECIMAL(10, 2),
  telefono VARCHAR(20),
  correo_electronico VARCHAR(255)
);

-- Insertar datos de ejemplo
INSERT INTO empleados (nombres, apellidos, cargo, salario,telefono,correo_electronico)
VALUES
  ('Ana', 'Gomez', 'Camarero', 90000, '987654321', 'ana@gmail.com'),
  ('Pedro', 'Rodriguez', 'Chef', 150000, '654123987', 'pedro@gmail.com'),
  ('Laura', 'Lopez', 'Ayudante de cocina', 100000, '789456123', 'laura@gmail.com'),
  ('Carlos', 'Sanchez', 'Cajero', 95000, '159753852', 'carlos@gmail.com'),
  ('María', 'Fernández', 'Repartidor', 88000, '456789123', 'maria@gmail.com'),
  ('Sofia', 'Martinez', 'Mesero', 85000, '963852741', 'sofia@gmail.com'),
  ('Carmen', 'Ramirez', 'Chef', 120000, '258741369', 'carmen@gmail.com'),
  ('Javier', 'Ortiz', 'Camarero', 86000, '951357246', 'javier@gmail.com'),
  ('Patricia', 'Gutierrez', 'Ayudante de cocina', 91000, '753159246', 'patricia@gmail.com'),
  ('Ricardo', 'Vargas', 'Repartidor', 121000, '357951246', 'ricardo@gmail.com'),
  ('Isabel', 'Mendoza', 'Cajero', 81000, '951753246', 'isabel@gmail.com');




--USE restaurante;
SELECT * FROM empleados;