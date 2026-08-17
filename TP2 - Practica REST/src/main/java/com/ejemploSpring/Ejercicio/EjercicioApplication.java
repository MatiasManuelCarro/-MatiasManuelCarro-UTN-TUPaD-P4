package com.ejemploSpring.Ejercicio;

import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.service.CategoriaService;
import com.ejemploSpring.Ejercicio.service.PedidoService;
import com.ejemploSpring.Ejercicio.service.ProductoService;
import com.ejemploSpring.Ejercicio.service.UsuarioService;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaCreate;
import com.ejemploSpring.Ejercicio.dtos.detallePedido.DetallePedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoEdit;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioCreate;
import com.ejemploSpring.Ejercicio.enums.Estado;
import com.ejemploSpring.Ejercicio.enums.FormaPago;
import com.ejemploSpring.Ejercicio.enums.Rol;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

@SpringBootApplication
public class EjercicioApplication {

    public static void main(String[] args) {
        SpringApplication.run(EjercicioApplication.class, args);
    }

    @Bean
    public CommandLineRunner initData(
            UsuarioService usuarioService,
            CategoriaService categoriaService,
            ProductoService productoService,
            PedidoService pedidoService
    ) {
        return args -> {

            // ============================
            // 1) USUARIOS (5)
            // ============================
            UsuarioDto u1 = usuarioService.save(new UsuarioCreate(
                    "Matías", "Carro", "matias@mail.com", "1155555555", "123456", Rol.USUARIO
            ));

            UsuarioDto u2 = usuarioService.save(new UsuarioCreate(
                    "Ana", "Gómez", "ana@mail.com", "1144444444", "abc123", Rol.USUARIO
            ));

            UsuarioDto u3 = usuarioService.save(new UsuarioCreate(
                    "Luis", "Pérez", "luis@mail.com", "1133333333", "pass123", Rol.USUARIO
            ));

            UsuarioDto u4 = usuarioService.save(new UsuarioCreate(
                    "Carla", "Sosa", "carla@mail.com", "1122222222", "qwerty", Rol.USUARIO
            ));

            UsuarioDto u5 = usuarioService.save(new UsuarioCreate(
                    "Jorge", "Ramírez", "jorge@mail.com", "1111111111", "jorgepass", Rol.ADMIN
            ));


            // ============================
            // 2) CATEGORÍAS (insumos de computación)
            // ============================
            var c1 = categoriaService.save(new CategoriaCreate(
                    "Periféricos", "Teclados, mouse, auriculares"
            ));

            var c2 = categoriaService.save(new CategoriaCreate(
                    "Almacenamiento", "Discos SSD, HDD, memorias"
            ));

            var c3 = categoriaService.save(new CategoriaCreate(
                    "Componentes", "Placas de video, motherboards, procesadores"
            ));

            var c4 = categoriaService.save(new CategoriaCreate(
                    "Monitores", "Pantallas LED, IPS, 144Hz"
            ));

            var c5 = categoriaService.save(new CategoriaCreate(
                    "Accesorios", "Cables, adaptadores, soportes"
            ));


            // ============================
            // 3) PRODUCTOS (10)
            // ============================
            productoService.save(new ProductoCreate("Teclado Mecánico Redragon", new BigDecimal("25000"), "Switch Red", 30, "teclado.jpg", true, c1.id()));
            productoService.save(new ProductoCreate("Mouse Logitech G203", new BigDecimal("18000"), "RGB 8000 DPI", 40, "mouse.jpg", true, c1.id()));
            productoService.save(new ProductoCreate("Auriculares HyperX Cloud II", new BigDecimal("45000"), "Sonido 7.1", 20, "auriculares.jpg", true, c1.id()));

            productoService.save(new ProductoCreate("SSD Kingston 480GB", new BigDecimal("32000"), "SATA 3", 50, "ssd.jpg", true, c2.id()));
            productoService.save(new ProductoCreate("Memoria RAM 16GB DDR4", new BigDecimal("28000"), "3200MHz", 35, "ram.jpg", true, c2.id()));

            productoService.save(new ProductoCreate("Motherboard ASUS B450", new BigDecimal("65000"), "AM4", 15, "mother.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("Placa de Video GTX 1660", new BigDecimal("180000"), "6GB GDDR5", 10, "gtx1660.jpg", true, c3.id()));

            productoService.save(new ProductoCreate("Monitor Samsung 24\"", new BigDecimal("90000"), "IPS 75Hz", 25, "monitor.jpg", true, c4.id()));
            productoService.save(new ProductoCreate("Cable HDMI 2.0", new BigDecimal("5000"), "1.8m", 100, "hdmi.jpg", true, c5.id()));
            productoService.save(new ProductoCreate("Soporte para Notebook", new BigDecimal("15000"), "Ajustable", 60, "soporte.jpg", true, c5.id()));


            // ============================
            // 4) PEDIDOS (10)
            // ============================

            // Pedido 1 - Usuario 1
            Pedido p1 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.EFECTIVO,
                    List.of(new DetallePedidoCreate(1, 1L), new DetallePedidoCreate(1, 4L))
            ));
            pedidoService.asignarPedido(u1.id(), p1);

            // Pedido 2 - Usuario 2
            Pedido p2 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.TARJETA,
                    List.of(new DetallePedidoCreate(2, 2L))
            ));
            pedidoService.asignarPedido(u2.id(), p2);

            // Pedido 3 - Usuario 3
            Pedido p3 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.TRANSFERENCIA,
                    List.of(new DetallePedidoCreate(1, 3L), new DetallePedidoCreate(1, 5L))
            ));
            pedidoService.asignarPedido(u3.id(), p3);

            // Pedido 4 - Usuario 4
            Pedido p4 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.EFECTIVO,
                    List.of(new DetallePedidoCreate(1, 6L))
            ));
            pedidoService.asignarPedido(u4.id(), p4);

            // Pedido 5 - Usuario 5
            Pedido p5 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.TARJETA,
                    List.of(new DetallePedidoCreate(1, 7L))
            ));
            pedidoService.asignarPedido(u5.id(), p5);

            // Pedido 6 - Usuario 1
            Pedido p6 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.TRANSFERENCIA,
                    List.of(new DetallePedidoCreate(2, 8L))
            ));
            pedidoService.asignarPedido(u1.id(), p6);

            // Pedido 7 - Usuario 2
            Pedido p7 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.EFECTIVO,
                    List.of(new DetallePedidoCreate(3, 9L))
            ));
            pedidoService.asignarPedido(u2.id(), p7);

            // Pedido 8 - Usuario 3
            Pedido p8 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.TARJETA,
                    List.of(new DetallePedidoCreate(1, 10L))
            ));
            pedidoService.asignarPedido(u3.id(), p8);

            // Pedido 9 - Usuario 4
            Pedido p9 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.TRANSFERENCIA,
                    List.of(new DetallePedidoCreate(1, 2L), new DetallePedidoCreate(1, 5L))
            ));
            pedidoService.asignarPedido(u4.id(), p9);

            // Pedido 10 - Usuario 5
            Pedido p10 = pedidoService.save(new PedidoCreate(
                    LocalDate.now(), Estado.PENDIENTE, FormaPago.EFECTIVO,
                    List.of(new DetallePedidoCreate(2, 1L), new DetallePedidoCreate(1, 7L))
            ));
            pedidoService.asignarPedido(u5.id(), p10);


            System.out.println(">>> Datos iniciales cargados correctamente.");
        };
    }


}
