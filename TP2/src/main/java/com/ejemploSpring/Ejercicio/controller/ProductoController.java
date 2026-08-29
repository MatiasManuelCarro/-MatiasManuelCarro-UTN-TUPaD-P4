package com.ejemploSpring.Ejercicio.controller;

import com.ejemploSpring.Ejercicio.dtos.producto.ProductoCreate;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoDto;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoEdit;
import com.ejemploSpring.Ejercicio.service.ProductoService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/productos")
@RequiredArgsConstructor
public class ProductoController {

    private final ProductoService productoService;

    // Get All
    @GetMapping("")
    public List<ProductoDto> getProductos() {
        return productoService.findAll();
    }

    @GetMapping("/eliminados")
    public List<ProductoDto> getEliminados() {
        return productoService.findAllEliminados();
    }

    // GetByID
    @GetMapping("/{id}")
    public ProductoDto getProducto(@PathVariable Long id) {
        return productoService.findById(id);
    }

    // Create
    @PostMapping("")
    @ResponseStatus(HttpStatus.CREATED)
    public ProductoDto createProducto(@Valid @RequestBody ProductoCreate productoCreate) {
        return productoService.save(productoCreate);
    }

    // Update
    @PutMapping("/{id}")
    public ProductoDto updateProducto(
            @PathVariable Long id,
            @Valid @RequestBody ProductoEdit productoEdit
    ) {
        return productoService.update(productoEdit, id);
    }

    // Delete
    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteProducto(@PathVariable Long id) {
        productoService.deleteById(id);
    }
}