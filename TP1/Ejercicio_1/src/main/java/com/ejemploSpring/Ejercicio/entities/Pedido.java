package com.ejemploSpring.Ejercicio.entities;

import com.ejemploSpring.Ejercicio.enums.Estado;
import com.ejemploSpring.Ejercicio.enums.FormaPago;
import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "pedidos")
@Getter
@Setter
@ToString
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
@NoArgsConstructor
@SuperBuilder
public class Pedido extends Base implements Calculable {
    private LocalDate fecha;
    @Enumerated(EnumType.STRING)
    private Estado estado;
    private BigDecimal total;
    @Enumerated(EnumType.STRING)
    private FormaPago formapago;
    //se elimina por correccion
/*    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;*/


    //se elimina para corregir direccion de relacion
/*    @Builder.Default
    @OneToMany(mappedBy = "pedido", cascade = CascadeType.ALL, orphanRemoval = true)*/
    @Builder.Default
    @OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)
    @JoinColumn(name = "pedido_id") // FK en detallePedido
    private Set<DetallePedido> detallePedidos = new HashSet<>();


    //Agregar detalle
    public void addDetallePedido(int cantidad, Producto producto) {

        boolean exists = detallePedidos.stream()
                .anyMatch(detallePedido -> detallePedido.getProducto().equals(producto));
        if (exists) return;

        DetallePedido detallePedido = DetallePedido.builder()
                .cantidad(cantidad)
                .producto(producto)
                .subtotal(producto.getPrecio().multiply(BigDecimal.valueOf(cantidad)))
                //.pedido(this)
                //se elimina pedido por correccion
                .build();

        detallePedidos.add(detallePedido);

    }

    //Buscar detalle por producto
    public DetallePedido findDetallePedidoByProducto(Producto producto) {
        return detallePedidos.stream()
                .filter(detallePedido -> detallePedido.getProducto().equals(producto))
                .findFirst()
                .orElse(null);
    }


    //Eliminar detalle por producto
    public void deleteDetalleByProducto(Producto producto) {
        detallePedidos.removeIf(d -> d.getProducto().equals(producto));
    }


    @Override
    public void calcularTotal() {
        BigDecimal totalFinal = detallePedidos.stream()
                .map(DetallePedido::getSubtotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        this.total = totalFinal;
        System.out.println("Total del pedido: " + totalFinal);
    }



}