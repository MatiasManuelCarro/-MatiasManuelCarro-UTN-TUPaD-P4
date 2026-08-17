package com.ejemploSpring.Ejercicio.controller;

import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioCreate;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioEdit;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioNombreDto;
import com.ejemploSpring.Ejercicio.service.UsuarioService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/usuarios")
@RequiredArgsConstructor
public class UsuarioController {

    private final UsuarioService usuarioService;

    // Get All
    @GetMapping("")
    public List<UsuarioDto> getUsuarios() {
        return usuarioService.findAll();
    }

    // Get By ID
    @GetMapping("/{id}")
    public UsuarioDto getUsuario(@PathVariable Long id) {
        return usuarioService.findById(id);
    }

    // GET solamente nombre y apellido
    @GetMapping("/{id}/nombre")
    public UsuarioNombreDto getNombreApellido(@PathVariable Long id) {
        return usuarioService.getNombreApellido(id);
    }

    // Create
    @PostMapping("")
    @ResponseStatus(HttpStatus.CREATED)
    public UsuarioDto createUsuario(@Valid @RequestBody UsuarioCreate usuarioCreate) {
        return usuarioService.save(usuarioCreate);
    }

    // Update
    @PutMapping("/{id}")
    public UsuarioDto updateUsuario(
            @PathVariable Long id,
            @Valid @RequestBody UsuarioEdit usuarioEdit
    ) {
        return usuarioService.update(usuarioEdit, id);
    }

    // Delete
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteUsuario(@PathVariable Long id) {
        usuarioService.deleteById(id);
    }

    @GetMapping("/mail/{mail}")
    public UsuarioDto getByEmail(@PathVariable String mail) {
        return usuarioService.findByMail(mail);
    }

}
