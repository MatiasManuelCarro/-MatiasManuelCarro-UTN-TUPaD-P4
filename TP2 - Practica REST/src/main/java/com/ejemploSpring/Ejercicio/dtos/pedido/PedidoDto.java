package com.ejemploSpring.Ejercicio.dtos.pedido;

import com.ejemploSpring.Ejercicio.dtos.detallePedido.DetallePedidoDto;
import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.enums.Estado;
import com.ejemploSpring.Ejercicio.enums.FormaPago;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;

public record PedidoDto(
        Long id,
        LocalDate fecha,
        Estado estado,
        BigDecimal total,
        FormaPago formapago,
        List<DetallePedidoDto>detalles
) {

    public static PedidoDto toDto(Pedido pedido) {
        return new PedidoDto(
                pedido.getId(),
                pedido.getFecha(),
                pedido.getEstado(),
                pedido.getTotal(),
                pedido.getFormapago(),
                pedido.getDetallePedidos().stream()
                        .map(DetallePedidoDto::toDto)
                        .toList()
        );
    }
}
