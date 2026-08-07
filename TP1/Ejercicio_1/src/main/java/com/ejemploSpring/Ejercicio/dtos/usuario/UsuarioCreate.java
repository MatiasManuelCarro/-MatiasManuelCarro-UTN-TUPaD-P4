package com.ejemploSpring.Ejercicio.dtos.usuario;

import com.ejemploSpring.Ejercicio.enums.Rol;

public record UsuarioCreate(
        String nombre,
        String apellido,
        String mail,
        String celular,
        String contrasenia,
        Rol rol
) {}