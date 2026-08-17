package com.ejemploSpring.Ejercicio.dtos.pedido;

public record PedidoCreateConUsuario(
        Long usuarioId,
        PedidoCreate pedido
) {}
