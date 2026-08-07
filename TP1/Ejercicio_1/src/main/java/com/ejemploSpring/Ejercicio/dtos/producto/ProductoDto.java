package com.ejemploSpring.Ejercicio.dtos.producto;

import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaDto;
import com.ejemploSpring.Ejercicio.entities.Categoria;
import com.ejemploSpring.Ejercicio.entities.Producto;

import java.math.BigDecimal;

public record ProductoDto(
    Long id,
    String nombre,
    BigDecimal precio,
    String descripcion,
    int stock,
    String imagen,
    Boolean disponible,
    CategoriaDto categoriaDto
){
    public static ProductoDto toDto(Producto producto){
        return new ProductoDto(
                producto.getId(),
                producto.getNombre(),
                producto.getPrecio(),
                producto.getDescripcion(),
                producto.getStock(),
                producto.getImagen(),
                producto.isDisponible(),
                //  Si producto.getCategoria es nulo, se devuelve nulo
                producto.getCategoria() != null ? CategoriaDto.toDto(producto.getCategoria()) : null
        );
    }
}


