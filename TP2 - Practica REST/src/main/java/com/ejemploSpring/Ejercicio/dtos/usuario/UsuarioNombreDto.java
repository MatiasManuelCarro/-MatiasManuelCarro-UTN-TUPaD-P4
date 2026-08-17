package com.ejemploSpring.Ejercicio.dtos.usuario;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.enums.Rol;

public record UsuarioNombreDto(
        String nombre,
        String apellido
) {

    public static UsuarioNombreDto toDto(Usuario usuario) {
        return new UsuarioNombreDto(
                usuario.getNombre(),
                usuario.getApellido()
        );
    }
}