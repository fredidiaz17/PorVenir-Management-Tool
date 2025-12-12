CREATE DATABASE IF NOT EXISTS tienda;
USE tienda;

CREATE TABLE `compania` (
  `id_compania` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(100)
);

CREATE TABLE `marca` (
  `id_marca` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(100),
  `descripcion` varchar(255),
  `id_compania` integer
);

CREATE TABLE `producto` (
  `id_producto` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(100),
  `cantidad_stock` decimal(10,2),
  `unidad_medida` enum('Gramos', 'Kilogramos', 'Libras', 'Litros', 'Mililitros', 'Unidades', 'Docenas', 'Paquetes'),
  `precio_compra` decimal(10,2),
  `precio_venta` decimal(10,2),
  `porcentaje_iva` decimal(5,2),
  `id_marca` integer
);

CREATE TABLE `preventista` (
  `id_preventista` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(100),
  `telefono` varchar(20),
  `id_compania` integer
);

CREATE TABLE `pedido` (
  `id_pedido` integer AUTO_INCREMENT PRIMARY KEY,
  `fecha_pedido` date,
  `estado` enum('Pendiente', 'En camino', 'Recibido', 'Rechazado', 'Cancelado'),
  `subtotal` decimal(10,2),
  `impuestos` decimal(10,2),
  `total` decimal(10,2),
  `id_preventista` integer
);

CREATE TABLE `detalle_pedido` (
  `id_pedido` integer,
  `id_producto` integer,
  `cantidad` decimal(10,2),
  `precio_unitario` decimal(10,2),
  `subtotal_linea` decimal(10,2),
  `iva_porcentaje` decimal(5,2),
  `iva_valor` decimal(10,2),
  `total_linea` decimal(10,2),
  PRIMARY KEY (`id_pedido`, `id_producto`)
);

CREATE TABLE `etiqueta` (
  `id_etiqueta` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre_etiqueta` varchar(50),
  `descripcion` text,
  `color_hex` varchar(9)
);

CREATE TABLE `producto_etiqueta` (
  `id_producto` integer,
  `id_etiqueta` integer,
  `estado` enum('Activo', 'Inactivo'),
  PRIMARY KEY (`id_producto`, `id_etiqueta`)
);

CREATE TABLE `oferta` (
  `id_oferta` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(100),
  `descripcion` text,
  `tipo_oferta` enum('Descuento', 'Combo', 'Otro'),
  `valor_descuento` decimal(10,2),
  `cantidad_minima` int,
  `producto_regalo` integer,
  `fecha_inicio` date,
  `fecha_fin` date,
  `estado` enum('Activa', 'Inactiva', 'Finalizada')
);

CREATE TABLE `oferta_producto` (
  `id_oferta` integer,
  `id_producto` integer,
  PRIMARY KEY (`id_oferta`, `id_producto`)
);

CREATE TABLE `oferta_etiqueta` (
  `id_oferta` integer,
  `id_etiqueta` integer,
  PRIMARY KEY (`id_oferta`, `id_etiqueta`)
);

CREATE TABLE `oferta_marca` (
  `id_oferta` integer,
  `id_marca` integer,
  PRIMARY KEY (`id_oferta`, `id_marca`)
);

CREATE TABLE `oferta_compania` (
  `id_oferta` integer,
  `id_compania` integer,
  PRIMARY KEY (`id_oferta`, `id_compania`)
);

CREATE TABLE `cliente` (
  `id_cliente` integer AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(50),
  `telefono` varchar(20)
);

CREATE TABLE `deuda` (
  `id_deuda` integer AUTO_INCREMENT PRIMARY KEY,
  `saldo_pendiente` decimal(10,2),
  `estado` boolean NOT NULL,
  `id_cliente` integer UNIQUE
);

CREATE TABLE `venta` (
  `id_venta` integer AUTO_INCREMENT PRIMARY KEY,
  `fecha` date,
  `medio_pago` enum('Efectivo', 'Digital', 'Mixto', 'Fiado', 'Otro'),
  `total` decimal(10,2),
  `id_cliente` integer
);

CREATE TABLE `detalle_venta` (
  `id_venta` integer,
  `id_producto` integer,
  `cantidad` decimal(10,2),
  `precio_venta` decimal(10,2),
  `descuento_manual` decimal(10,2),
  `subtotal` decimal(10,2),
  PRIMARY KEY (`id_venta`, `id_producto`)
);

ALTER TABLE `marca` ADD FOREIGN KEY (`id_compania`) REFERENCES `compania` (`id_compania`);

ALTER TABLE `producto` ADD FOREIGN KEY (`id_marca`) REFERENCES `marca` (`id_marca`);

ALTER TABLE `preventista` ADD FOREIGN KEY (`id_compania`) REFERENCES `compania` (`id_compania`);

ALTER TABLE `pedido` ADD FOREIGN KEY (`id_preventista`) REFERENCES `preventista` (`id_preventista`);

ALTER TABLE `detalle_pedido` ADD FOREIGN KEY (`id_pedido`) REFERENCES `pedido` (`id_pedido`);

ALTER TABLE `detalle_pedido` ADD FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

ALTER TABLE `producto_etiqueta` ADD FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

ALTER TABLE `producto_etiqueta` ADD FOREIGN KEY (`id_etiqueta`) REFERENCES `etiqueta` (`id_etiqueta`);

ALTER TABLE `oferta` ADD FOREIGN KEY (`producto_regalo`) REFERENCES `producto` (`id_producto`);

ALTER TABLE `oferta_producto` ADD FOREIGN KEY (`id_oferta`) REFERENCES `oferta` (`id_oferta`);

ALTER TABLE `oferta_producto` ADD FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);

ALTER TABLE `oferta_etiqueta` ADD FOREIGN KEY (`id_oferta`) REFERENCES `oferta` (`id_oferta`);

ALTER TABLE `oferta_etiqueta` ADD FOREIGN KEY (`id_etiqueta`) REFERENCES `etiqueta` (`id_etiqueta`);

ALTER TABLE `oferta_marca` ADD FOREIGN KEY (`id_oferta`) REFERENCES `oferta` (`id_oferta`);

ALTER TABLE `oferta_marca` ADD FOREIGN KEY (`id_marca`) REFERENCES `marca` (`id_marca`);

ALTER TABLE `oferta_compania` ADD FOREIGN KEY (`id_oferta`) REFERENCES `oferta` (`id_oferta`);

ALTER TABLE `oferta_compania` ADD FOREIGN KEY (`id_compania`) REFERENCES `compania` (`id_compania`);

ALTER TABLE `deuda` ADD FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`);

ALTER TABLE `venta` ADD FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`);

ALTER TABLE `detalle_venta` ADD FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`);

ALTER TABLE `detalle_venta` ADD FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`);
