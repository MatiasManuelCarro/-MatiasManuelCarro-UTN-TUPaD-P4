package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaCreate;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaDto;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaEdit;
import com.ejemploSpring.Ejercicio.entities.Categoria;
import com.ejemploSpring.Ejercicio.repository.CategoriaRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CategoriaServiceImpl implements CategoriaService{
    private final CategoriaRepository categoriaRepository;

    public CategoriaServiceImpl(CategoriaRepository categoriaRepository) {
        this.categoriaRepository = categoriaRepository;
    }

    @Override
    public CategoriaDto save(CategoriaCreate categoriaCreate) {
        Categoria categoria = categoriaCreate.toEntity();
        categoria = categoriaRepository.save(categoria);
        return CategoriaDto.toDto(categoria);
    }

    @Override
    public CategoriaDto findById(Long id) {
        Categoria categoria = categoriaRepository.findById(id)
                .filter(c -> !Boolean.TRUE.equals(c.getEliminado())) // descarta eliminadas
                .orElseThrow(() -> new NullPointerException("No se encontró categoría activa con el id " + id));
        return CategoriaDto.toDto(categoria);
    }

    @Override
    public List<CategoriaDto> findAll() {
        return categoriaRepository.findAllByEliminadoFalse()
                .stream()
                .map(CategoriaDto::toDto)
                .toList();
    }

    @Override
    public CategoriaDto update(CategoriaEdit categoriaEdit, Long idCategoria) {
        Categoria categoria = categoriaRepository.findById(idCategoria).orElseThrow(() -> new NullPointerException("No se contro categoria con el id" + idCategoria));
        categoriaEdit.applyTo(categoria);
        categoria = categoriaRepository.save(categoria);
        return CategoriaDto.toDto(categoria);
    }

    @Override
    public void deleteById(Long id) {
        Categoria categoria = categoriaRepository.findById(id)
                .orElseThrow(() -> new NullPointerException("No se contro categoria con el id " + id));
        categoria.setEliminado(true);
        categoriaRepository.save(categoria);
    }
}
