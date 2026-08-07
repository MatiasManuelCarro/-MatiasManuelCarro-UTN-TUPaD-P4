package com.ejemploSpring.Ejercicio.Service;

import com.ejemploSpring.Ejercicio.dtos.producto.ProductoCreate;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoDto;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoEdit;
import com.ejemploSpring.Ejercicio.entities.Categoria;
import com.ejemploSpring.Ejercicio.entities.Producto;
import com.ejemploSpring.Ejercicio.repository.CategoriaRepository;
import com.ejemploSpring.Ejercicio.repository.ProductoRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductoServiceImpl implements ProductoService {

    private final ProductoRepository productoRepository;
    private final CategoriaRepository categoriaRepository;

    public ProductoServiceImpl(ProductoRepository productoRepository, CategoriaRepository categoriaRepository) {
        this.productoRepository = productoRepository;
        this.categoriaRepository = categoriaRepository;
    }

    @Override
    public ProductoDto save(ProductoCreate productoCreate) {
        Categoria categoria = categoriaRepository.findById(productoCreate.idCategoria()).orElseThrow(() -> new NullPointerException("No se econtro categoria con id" + productoCreate.idCategoria()));
        Producto producto = productoCreate.toEntity(categoria);
        producto = productoRepository.save(producto);
        return ProductoDto.toDto(producto);
    }

    @Override
    public ProductoDto findById(Long id) {
        Producto producto = productoRepository.findById(id).orElseThrow(() -> new NullPointerException("No se econtro categoria con id" + id));
        return ProductoDto.toDto(producto);
    }

    @Override
    public List<ProductoDto> findAll() {
        List<Producto> productos = productoRepository.findAll();
        return productos.stream().map(ProductoDto::toDto).toList();
    }

    @Override
    public ProductoDto update(ProductoEdit productoEdit, Long idProducto) {
        Producto producto = productoRepository.findById(idProducto).orElseThrow(() -> new NullPointerException(("No se econtro categoria con id" + idProducto)));
        Categoria categoria = null;
        if(productoEdit.idCategoria() != null) {
            categoria = categoriaRepository.findById(productoEdit.idCategoria()).orElseThrow(() -> new NullPointerException(("No se econtro categoria con id" + idProducto)));
        }
        productoEdit.applyTo(producto, categoria);
        producto = productoRepository.save(producto);
        return ProductoDto.toDto(producto);
    }

    @Override
    public void deleteById(Long id) {
        Producto producto = productoRepository.findById(id).orElseThrow(() -> new NullPointerException(("No se econtro categoria con id" + id)));
        producto.setEliminado(true);
        productoRepository.save(producto);

    }
}
