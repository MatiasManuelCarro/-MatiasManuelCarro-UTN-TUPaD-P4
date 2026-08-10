package com.ejemploSpring.Ejercicio.dtos.pedido;

import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.enums.Estado;
import com.ejemploSpring.Ejercicio.enums.FormaPago;

import java.time.LocalDate;

public record PedidoEdit(
        LocalDate fecha,
        Estado estado,
        FormaPago formapago,
        Long usuarioId
) {

    public void applyTo(Pedido pedido, Usuario usuario) {

        if (this.fecha != null) {
            pedido.setFecha(this.fecha);
        }

        if (this.estado != null) {
            pedido.setEstado(this.estado);
        }

        if (this.formapago != null) {
            pedido.setFormapago(this.formapago);
        }

/*        if (this.usuarioId != null && usuario != null) {
            pedido.setUsuario(usuario);
        }*/
    }


}