package com.ejemploSpring.Ejercicio.dtos.detallePedido;

import com.ejemploSpring.Ejercicio.entities.DetallePedido;

import java.math.BigDecimal;

public record DetallePedidoDto(
        Long id,
        int cantidad,
        BigDecimal subtotal,
        Long productoId,
        String productoNombre
/*        Long pedidoId*/
) {


    public static DetallePedidoDto toDto(DetallePedido detalle) {
        return new DetallePedidoDto(
                detalle.getId(),
                detalle.getCantidad(),
                detalle.getSubtotal(),
                detalle.getProducto().getId(),
                detalle.getProducto().getNombre());
/*                detalle.getPedido().getId()*/

    }
}