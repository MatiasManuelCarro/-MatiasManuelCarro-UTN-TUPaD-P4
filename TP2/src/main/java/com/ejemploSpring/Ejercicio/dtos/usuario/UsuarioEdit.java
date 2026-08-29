package com.ejemploSpring.Ejercicio.dtos.usuario;

import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.enums.Rol;

import java.util.Optional;

public record UsuarioEdit(
        String nombre,
        String apellido,
        String mail,
        String celular,
        String contrasenia,
        Rol rol
) {

    public void applyTo(Usuario usuario) {

        if (this.nombre != null) {
            usuario.setNombre(this.nombre);
        }

        if (this.apellido != null) {
            usuario.setApellido(this.apellido);
        }

        if (this.mail != null) {
            usuario.setMail(this.mail);
        }

        if (this.celular != null) {
            usuario.setCelular(this.celular);
        }

        if (this.contrasenia != null) {
            usuario.setContrasenia(this.contrasenia);
        }

        if (this.rol != null) {
            usuario.setRol(this.rol);
        }
    }
}