package com.ejemploSpring.Ejercicio.dtos.categoria;

import com.ejemploSpring.Ejercicio.entities.Categoria;

public record CategoriaDto(
        Long id,
        String nombre,
        String descripcion,
        Boolean eliminado
) {
    public static CategoriaDto toDto(Categoria categoria){
        return new CategoriaDto(
                categoria.getId(),
                categoria.getNombre(),
                categoria.getDescripcion(),
                categoria.getEliminado()
        );
    }
}
