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
                    "123456",
                    Rol.USUARIO     // rol
            ));

            var u2 = usuarioService.save(new UsuarioCreate(
                    "David",
                    "Gómez",
                    "david@mail.com",
                    "1144444444",
                    "admin123",     // contrasenia
                    Rol.ADMIN       // rol
            ));

            // ============================
            // 2) CATEGORÍAS
            // ============================
            var c1 = categoriaService.save(new CategoriaCreate(
                    "Procesadores", "CPUs Intel y AMD"
            ));

            var c2 = categoriaService.save(new CategoriaCreate(
                    "Placas de Video", "GPUs para gaming y diseño"
            ));

            var c3 = categoriaService.save(new CategoriaCreate(
                    "Memorias RAM", "DDR4 y DDR5"
            ));

            // ============================
            // 3) PRODUCTOS
            // ============================
            productoService.save(new ProductoCreate("Intel Core i5 12400F", new BigDecimal("150000"), "6 núcleos", 20, "i5.jpg", true, c1.id()));
            productoService.save(new ProductoCreate("Intel Core i7 13700K", new BigDecimal("350000"), "16 núcleos", 15, "i7.jpg", true, c1.id()));
            productoService.save(new ProductoCreate("AMD Ryzen 5 5600X", new BigDecimal("180000"), "6 núcleos", 25, "r5600x.jpg", true, c1.id()));

            productoService.save(new ProductoCreate("NVIDIA RTX 4060", new BigDecimal("450000"), "8GB GDDR6", 10, "rtx4060.jpg", true, c2.id()));
            productoService.save(new ProductoCreate("NVIDIA RTX 4070", new BigDecimal("650000"), "12GB GDDR6X", 8, "rtx4070.jpg", true, c2.id()));
            productoService.save(new ProductoCreate("AMD RX 6600", new BigDecimal("300000"), "8GB GDDR6", 12, "rx6600.jpg", true, c2.id()));

            productoService.save(new ProductoCreate("Corsair Vengeance 16GB DDR4", new BigDecimal("80000"), "3200MHz", 30, "ram16.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("Kingston Fury 32GB DDR5", new BigDecimal("150000"), "5600MHz", 20, "ram32.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("G.Skill Trident Z 16GB DDR5", new BigDecimal("140000"), "6000MHz", 18, "tridentz.jpg", true, c3.id()));
            productoService.save(new ProductoCreate("Patriot Viper 8GB DDR4", new BigDecimal("40000"), "3000MHz", 40, "viper8.jpg", true, c3.id()));


            // ============================
            // 4) PEDIDOS
            // ============================

            // Pedido 1 - usuario 1
            pedidoService.save(
                    new PedidoEdit(LocalDate.now(), Estado.PENDIENTE, FormaPago.EFECTIVO, u1.id()),
                    List.of(
                            new DetallePedidoCreate(1, 1L), // Intel i5
                            new DetallePedidoCreate(1, 4L)  // RTX 4060
                    )
            );

            // Pedido 2 - usuario 1
            pedidoService.save(
                    new PedidoEdit(LocalDate.now().minusDays(1), Estado.CONFIRMADO, FormaPago.TARJETA, u1.id()),
                    List.of(
                            new DetallePedidoCreate(2, 7L), // Corsair 16GB DDR4
                            new DetallePedidoCreate(1, 2L)  // Intel i7
                    )
            );

            // Pedido 3 - usuario 2
            pedidoService.save(
                    new PedidoEdit(LocalDate.now().minusDays(2), Estado.TERMINADO, FormaPago.TRANSFERENCIA, u2.id()),
                    List.of(
                            new DetallePedidoCreate(1, 5L), // RTX 4070
                            new DetallePedidoCreate(2, 10L) // Patriot 8GB DDR4
                    )
            );

            System.out.println(">>> Datos iniciales cargados correctamente (Hardware).");
        };
    }
}