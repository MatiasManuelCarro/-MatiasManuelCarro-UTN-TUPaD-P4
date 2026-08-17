package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioEdit;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioNombreDto;
import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.entities.Usuario;

import java.util.List;

public interface UsuarioService {
    public UsuarioDto save(UsuarioCreate usuarioCreate);

    public UsuarioDto findById(Long id);

    public List<UsuarioDto> findAll();

    public UsuarioDto update(UsuarioEdit usuarioEdit, Long idUsuario);

    public void deleteById(Long id);

    public UsuarioDto findByMail(String email);

    public UsuarioNombreDto getNombreApellido(Long id);

}
