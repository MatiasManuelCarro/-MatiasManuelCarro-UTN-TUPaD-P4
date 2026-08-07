package com.ejemploSpring.Ejercicio.Service;

import com.ejemploSpring.Ejercicio.dtos.producto.ProductoCreate;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoDto;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoEdit;

import java.util.List;

public interface ProductoService {
    public ProductoDto save(ProductoCreate productoCreate);
    public ProductoDto findById(Long id);
    public List<ProductoDto> findAll();
    public ProductoDto update(ProductoEdit productoEdit, Long idProducto);

    public void deleteById(Long id);
}
