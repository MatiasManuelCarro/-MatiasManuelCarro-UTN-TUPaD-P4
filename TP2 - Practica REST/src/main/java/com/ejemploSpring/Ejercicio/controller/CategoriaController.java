package com.ejemploSpring.Ejercicio.controller;


import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaCreate;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaDto;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaEdit;
import com.ejemploSpring.Ejercicio.service.CategoriaService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/categorias")
@RequiredArgsConstructor
public class CategoriaController {

    private final CategoriaService categoriaService;

    // Crear categoría
    @PostMapping
    public CategoriaDto create(@RequestBody CategoriaCreate categoriaCreate) {
        return categoriaService.save(categoriaCreate);
    }

    // Obtener categoría por ID (solo activas)
    @GetMapping("/{id}")
    public CategoriaDto findById(@PathVariable Long id) {
        return categoriaService.findById(id);
    }

    // Obtener todas las categorías activas
    @GetMapping
    public List<CategoriaDto> findAll() {
        return categoriaService.findAll();
    }

    // Editar categoría
    @PutMapping("/{id}")
    public CategoriaDto update(@PathVariable Long id,
                               @RequestBody CategoriaEdit categoriaEdit) {
        return categoriaService.update(categoriaEdit, id);
    }

    // Soft delete
    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        categoriaService.deleteById(id);
    }

}