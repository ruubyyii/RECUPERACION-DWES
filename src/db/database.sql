DROP DATABASE IF EXISTS tienda_examen;
CREATE DATABASE tienda_examen;
USE tienda_examen;

CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255),
    fullname VARCHAR(50)
);

CREATE TABLE productos (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    precio FLOAT UNSIGNED,
    imagen VARCHAR(255),
    descripcion VARCHAR(255),
    user_id INT UNSIGNED,
    FOREIGN KEY (user_id) REFERENCES users(id)
);