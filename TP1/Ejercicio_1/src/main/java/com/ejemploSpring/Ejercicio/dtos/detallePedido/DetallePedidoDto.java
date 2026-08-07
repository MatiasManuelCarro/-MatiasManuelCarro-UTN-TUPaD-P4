package com.ejemploSpring.Ejercicio.dtos.detallePedido;

import com.ejemploSpring.Ejercicio.entities.DetallePedido;

public record DetallePedidoDto(
        Long id,
        int cantidad,
        Double subtotal,
        Long productoId,
        String productoNombre,
        Long pedidoId
) {


    public static DetallePedidoDto toDto(DetallePedido detalle) {
        return new DetallePedidoDto(
                detalle.getId(),
                detalle.getCantidad(),
                detalle.getSubtotal(),
                detalle.getProducto().getId(),
                detalle.getProducto().getNombre(),
                detalle.getPedido().getId()
        );
    }
}