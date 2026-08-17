package com.ejemploSpring.Ejercicio.dtos.pedido;

import com.ejemploSpring.Ejercicio.dtos.detallePedido.DetallePedidoCreate;
import com.ejemploSpring.Ejercicio.enums.Estado;
import com.ejemploSpring.Ejercicio.enums.FormaPago;

import java.time.LocalDate;
import java.util.List;

public record PedidoCreate(
        LocalDate fecha,
        Estado estado,
        FormaPago formapago,
        List<DetallePedidoCreate> detalles
) {}
