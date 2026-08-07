package com.ejemploSpring.Ejercicio.dtos.pedido;

import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.enums.Estado;
import com.ejemploSpring.Ejercicio.enums.FormaPago;

import java.math.BigDecimal;
import java.time.LocalDate;

public record PedidoDto(
        Long id,
        LocalDate fecha,
        Estado estado,
        BigDecimal total,
        FormaPago formapago,
        String usuarioNombre
) {

    public static PedidoDto toDto(Pedido pedido) {
        return new PedidoDto(
                pedido.getId(),
                pedido.getFecha(),
                pedido.getEstado(),
                pedido.getTotal(),
                pedido.getFormapago(),
                pedido.getUsuario().getNombre());
    }
}
