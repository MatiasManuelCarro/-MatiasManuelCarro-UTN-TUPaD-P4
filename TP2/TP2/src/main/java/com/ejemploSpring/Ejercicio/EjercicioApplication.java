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
}