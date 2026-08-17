package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.producto.ProductoCreate;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoDto;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoEdit;
import com.ejemploSpring.Ejercicio.entities.Producto;

import java.util.List;

public interface ProductoService {
    public ProductoDto save(ProductoCreate productoCreate);
    public ProductoDto findById(Long id);
    public List<ProductoDto> findAll();
    public ProductoDto update(ProductoEdit productoEdit, Long idProducto);
    public Producto findEntityById(Long id);
    public void deleteById(Long id);
    public List<ProductoDto> findAllEliminados();
}
