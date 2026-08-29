package com.ejemploSpring.Ejercicio.dtos.categoria;
import com.ejemploSpring.Ejercicio.entities.Categoria;

public record CategoriaCreate(
        String nombre,
        String descripcion) {


    public Categoria toEntity(){
//        return new Categoria(this.nombre,this.descripcion);
            return Categoria.builder()
                    .nombre(this.nombre)
                    .descripcion(this.descripcion)
                    .build();
        }
    }

