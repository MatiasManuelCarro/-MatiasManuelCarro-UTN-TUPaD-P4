package com.ejemploSpring.Ejercicio.dtos.producto;

import com.ejemploSpring.Ejercicio.entities.Categoria;
import com.ejemploSpring.Ejercicio.entities.Producto;

import java.math.BigDecimal;

public record ProductoEdit(
        String nombre,
        BigDecimal precio,
        String descripcion,
        Integer stock,
        String imagen,
        Boolean disponible,
        Long idCategoria
) {
    public void applyTo(Producto producto, Categoria categoria){
        if (this.nombre != null) {
            producto.setNombre(this.nombre);
        }
        if (this.precio != null) {
            producto.setPrecio(this.precio);
        }
        if (this.descripcion != null) {
            producto.setDescripcion(this.descripcion);
        }
        if (this.stock != null) {
            producto.setStock(this.stock);
        }
        if (this.imagen != null) {
            producto.setImagen(this.imagen);
        }
        if (this.disponible != null) {
            producto.setDisponible(this.disponible);
        }
/*        if (categoria != null) {
            producto.setCategoria(categoria);
        }*/
    }
}
