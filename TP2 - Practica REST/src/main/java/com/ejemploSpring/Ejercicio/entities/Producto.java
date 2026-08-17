package com.ejemploSpring.Ejercicio.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.math.BigDecimal;

@Entity
@Table(name = "productos")
@Getter
@Setter
@ToString
@EqualsAndHashCode(callSuper = false , of = {"nombre", "precio"})
@SuperBuilder
@NoArgsConstructor
@AllArgsConstructor
public class Producto extends Base {
    @Column(unique = true)
    private String nombre;
    private BigDecimal precio;
    private String descripcion;
    private int stock;
    private String imagen;
    private boolean disponible;
    //Eliminado para cumplir las relaciones
/*    @ManyToOne
    @JoinColumn(name = "categoria_id")
    private Categoria categoria;

    //Redundante
    @Column(name = "ELIMINADO")
    @Builder.Default
    private Boolean eliminado = false; //valor por defecto

 */

}