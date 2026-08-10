package com.ejemploSpring.Ejercicio.Service;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioEdit;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class UsuarioServiceImpl implements UsuarioService {

    @Override
    public UsuarioDto save(UsuarioCreate usuarioCreate) {
        // implementación
        return null;
    }

    @Override
    public UsuarioDto findById(Long id) {
        // implementación
        return null;
    }

    @Override
    public List<UsuarioDto> findAll() {
        // implementación
        return null;
    }

    @Override
    public UsuarioDto update(UsuarioEdit usuarioEdit, Long idUsuario) {
        // implementación
        return null;
    }

    @Override
    public void deleteById(Long id) {
        // implementación
    }
}