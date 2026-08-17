package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioEdit;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioNombreDto;
import com.ejemploSpring.Ejercicio.entities.Usuario;
import com.ejemploSpring.Ejercicio.repository.UsuarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class UsuarioServiceImpl implements UsuarioService {

    private final UsuarioRepository usuarioRepository;

    @Override
    public UsuarioDto save(UsuarioCreate usuarioCreate) {

        Usuario usuario = usuarioCreate.toEntity(new Usuario());

        Usuario guardado = usuarioRepository.save(usuario);

        return UsuarioDto.toDto(guardado);
    }

    @Override
    public UsuarioDto findById(Long id) {

        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        return UsuarioDto.toDto(usuario);
    }

    @Override
    public List<UsuarioDto> findAll() {

        return usuarioRepository.findAll()
                .stream()
                .map(UsuarioDto::toDto)
                .toList();
    }

    @Override
    public UsuarioDto update(UsuarioEdit usuarioEdit, Long idUsuario) {

        Usuario usuario = usuarioRepository.findById(idUsuario)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        usuarioEdit.applyTo(usuario);

        Usuario actualizado = usuarioRepository.save(usuario);

        return UsuarioDto.toDto(actualizado);
    }

    @Override
    public void deleteById(Long id) {

        if (!usuarioRepository.existsById(id)) {
            throw new RuntimeException("Usuario no encontrado");
        }

        usuarioRepository.deleteById(id);
    }

    @Override
    public UsuarioNombreDto getNombreApellido(Long id) {

        Usuario usuario = usuarioRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Usuario no encontrado"));

        return UsuarioNombreDto.toDto(usuario);
    }
}