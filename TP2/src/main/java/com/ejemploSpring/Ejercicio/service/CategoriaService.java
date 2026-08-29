package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaCreate;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaDto;
import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaEdit;
import com.ejemploSpring.Ejercicio.entities.Categoria;

import java.util.List;

public interface CategoriaService {
    public CategoriaDto save(CategoriaCreate categoriaCreate);
    public CategoriaDto findById(Long id);
    public List<CategoriaDto> findAll();
    public CategoriaDto update(CategoriaEdit categoriaEdit, Long idCategoria);
    public void deleteById(Long id);

}
