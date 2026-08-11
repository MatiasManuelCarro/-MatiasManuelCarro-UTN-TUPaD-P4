package com.ejemploSpring.Ejercicio.entities;

import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;

@Entity
@Table(name = "detalle_pedidos")
@Getter
@Setter
@EqualsAndHashCode(callSuper = false, of = {"producto"})
@NoArgsConstructor
@AllArgsConstructor
@SuperBuilder
public class DetallePedido extends Base {

    private int cantidad;
    private BigDecimal subtotal;

    @ManyToOne
    @JoinColumn(name = "producto_id")
    private Producto producto;
    //Se elimina para cumplir con la direccionalidad
/*    @ManyToOne
    @JoinColumn(name = "pedido_id", nullable = false)
    private Pedido pedido;*/

    public DetallePedido(int cantidad, BigDecimal subtotal) {
        this.cantidad = cantidad;
        this.subtotal = subtotal;

    }
}