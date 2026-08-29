package com.ejemploSpring.Ejercicio.dtos.categoria;

import com.ejemploSpring.Ejercicio.entities.Categoria;

public record CategoriaEdit(
        String nombre,
        String descripcion
) {
    public void applyTo(Categoria categoria){
        if(this.nombre != null){
            categoria.setNombre(this.nombre);
        }

        if(this.descripcion != null){
            categoria.setDescripcion(this.descripcion);
        }
    }
}
