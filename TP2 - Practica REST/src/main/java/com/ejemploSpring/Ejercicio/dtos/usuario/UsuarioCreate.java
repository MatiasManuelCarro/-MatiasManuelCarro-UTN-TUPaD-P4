package com.ejemploSpring.Ejercicio.dtos.usuario;

import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.enums.Rol;

public record UsuarioCreate(
        String nombre,
        String apellido,
        String mail,
        String celular,
        String contrasenia,
        Rol rol
) {
    public Usuario toEntity(Usuario usuario){
        return Usuario.builder()
                .nombre(this.nombre)
                .apellido(this.apellido)
                .mail(this.mail)
                .celular(this.celular)
                .contrasenia(this.contrasenia)
                .rol(this.rol)
                .build();

    }

}