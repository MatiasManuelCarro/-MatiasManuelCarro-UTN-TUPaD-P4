package com.ejemploSpring.Ejercicio.dtos.producto;

import com.ejemploSpring.Ejercicio.entities.Categoria;
import com.ejemploSpring.Ejercicio.entities.Producto;

import java.math.BigDecimal;

public record ProductoCreate(
        String nombre,
        BigDecimal precio,
        String descripcion,
        int stock,
        String imagen,
        Boolean disponible,
        Long idCategoria
) {
    public Producto toEntity(Categoria categoria){
        return Producto.builder()
                .nombre(this.nombre)
                .precio(this.precio)
                .descripcion(this.descripcion)
                .stock(this.stock)
                .imagen(this.imagen)
                .disponible(this.disponible != null ? this.disponible : false)
                /*.categoria(categoria)*/
                .build();
    }
}
