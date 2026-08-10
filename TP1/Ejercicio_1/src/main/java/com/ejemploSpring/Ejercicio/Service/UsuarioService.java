package com.ejemploSpring.Ejercicio.Service;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioEdit;

import java.util.List;

public interface UsuarioService {
    public UsuarioDto save(UsuarioCreate usuarioCreate);

    public UsuarioDto findById(Long id);

    public List<UsuarioDto> findAll();

    public UsuarioDto update(UsuarioEdit usuarioEdit, Long idUsuario);

    public void deleteById(Long id);

}
