package com.ejemploSpring.Ejercicio;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
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
            // 1) USUARIOS
            // ============================
            UsuarioDto u1 = usuarioService.save(new UsuarioCreate(
                    "Matías",
                    "Carro",
                    "matias@mail.com",
                    "1155555555",
                    "123456",       // contrasenia
                    Rol.USUARIO     // rol
            ));

            var u2 = usuarioService.save(new UsuarioCreate(
                    "Ana",
                    "Gómez",
                    "ana@mail.com",
                    "1144444444",
                    "admin123",     // contrasenia
                    Rol.ADMIN       // rol
            ));

            // ============================
            // 2) CATEGORÍAS
            // ============================
            var c1 = categoriaService.save(new CategoriaCreate(
                    "Bebidas", "Gaseosas, jugos y agua"
            ));

            var c2 = categoriaService.save(new CategoriaCreate(
                    "Snacks", "Papas, maní y otros"
            ));

            var c3 = categoriaService.save(new CategoriaCreate(
                    "Lácteos", "Productos derivados de la leche"
            ));

            // ============================
            // 3) PRODUCTOS (10)
            // ============================
            productoService.save(new ProductoCreate("Coca Cola", new BigDecimal("1200"), "Gaseosa 1.5L", 50, "coca.jpg", true, c1.id()));
            productoService.save(new ProductoCreate("Pepsi", new BigDecimal("1100"), "Gaseosa 1.5L", 40, "pepsi.jpg", true, c1.id()));
            productoService.save(new ProductoCreate("Agua Mineral", new BigDecimal("800"), "Agua 2L", 60, "agua.jpg", true, c1.id()));

            productoService.save(new ProductoCreate("Papas Lays", new BigDecimal("900"), "Papas clásicas", 30, "lays.jpg", true, c2.id()));
            productoService.save(new ProductoCreate("Maní Salado", new BigDecimal("700"), "Maní 200g", 25, "mani.jpg", true, c2.id()));
            productoService.save(new ProductoCreate("Doritos", new BigDecimal("950"), "Nachos queso", 20, "doritos.jpg", true, c2.id()));

            productoService.save(new ProductoCreate("Leche Entera", new BigDecimal("1000"), "Leche 1L", 45, "leche.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("Yogur Frutilla", new BigDecimal("850"), "Yogur 200g", 35, "yogur.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("Queso Cremoso", new BigDecimal("1800"), "Queso 500g", 15, "queso.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("Manteca", new BigDecimal("950"), "Manteca 200g", 20, "manteca.jpg", true, c3.id()));

            // ============================
            // 4) PEDIDOS (3)
            // ============================

            // Pedido 1 - usuario 1
            var pedido1 = pedidoService.save(
                    new PedidoEdit(LocalDate.now(), Estado.PENDIENTE, FormaPago.EFECTIVO, u1.id()),
                    List.of(
                            new DetallePedidoCreate(2, 1L), // Coca Cola
                            new DetallePedidoCreate(1, 4L)  // Lays
                    )
            );

            // Pedido 2 - usuario 1
            var pedido2 = pedidoService.save(
                    new PedidoEdit(LocalDate.now().minusDays(1), Estado.CONFIRMADO, FormaPago.TARJETA, u1.id()),
                    List.of(
                            new DetallePedidoCreate(3, 7L), // Leche
                            new DetallePedidoCreate(2, 8L)  // Yogur
                    )
            );

            // Pedido 3 - usuario 2
            var pedido3 = pedidoService.save(
                    new PedidoEdit(LocalDate.now().minusDays(2), Estado.TERMINADO, FormaPago.TRANSFERENCIA, u2.id()),
                    List.of(
                            new DetallePedidoCreate(1, 9L), // Queso
                            new DetallePedidoCreate(2, 10L) // Manteca
                    )
            );

            System.out.println(">>> Datos iniciales cargados correctamente.");
        };
    }
}
