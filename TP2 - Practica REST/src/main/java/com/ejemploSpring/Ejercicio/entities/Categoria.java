package com.ejemploSpring.Ejercicio.entities;

import jakarta.persistence.*;
import lombok.*;
import lombok.experimental.SuperBuilder;

import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "categorias")
@SuperBuilder
@Getter
@Setter
@ToString(callSuper = true, exclude = "productos")
@EqualsAndHashCode(callSuper = false, of = {"nombre"})
@AllArgsConstructor
@NoArgsConstructor
public class Categoria extends Base {
    @Column(unique = true)
    private String nombre;
    private String descripcion;
    //Eliminado para complir las relaciones
/*    @OneToMany(mappedBy = "categoria", cascade = CascadeType.ALL, orphanRemoval = true)*/
@OneToMany
@JoinColumn(name = "categoria_id") // FK en producto
    @Builder.Default
    private Set<Producto> productos = new HashSet<>();
    @Builder.Default
    private Boolean eliminado = false; //valor por defecto


    //helper para mantener la bidireccionalidad - eliminado para cumplir la relacion
/*    public void addProducto(Producto producto) {
        productos.add(producto);
        producto.setCategoria(this);
    }*/
}



