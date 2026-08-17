package com.ejemploSpring.Ejercicio.dtos.usuario;

import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.enums.Rol;

public record UsuarioDto(
        Long id,
        String nombre,
        String apellido,
        String mail,
        String celular,
        Rol rol
) {

    public static UsuarioDto toDto(Usuario usuario) {
        return new UsuarioDto(
                usuario.getId(),
                usuario.getNombre(),
                usuario.getApellido(),
                usuario.getMail(),
                usuario.getCelular(),
                usuario.getRol()
        );
    }
}