package com.ejemploSpring.Ejercicio.controller;

import com.ejemploSpring.Ejercicio.dtos.categoria.CategoriaDto;
import com.ejemploSpring.Ejercicio.dtos.producto.ProductoDto;
import com.ejemploSpring.Ejercicio.dtos.usuario.UsuarioDto;
import com.ejemploSpring.Ejercicio.entities.*;
import com.ejemploSpring.Ejercicio.service.CategoriaService;
import com.ejemploSpring.Ejercicio.service.PedidoService;
import com.ejemploSpring.Ejercicio.service.ProductoService;
import com.ejemploSpring.Ejercicio.service.UsuarioService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequiredArgsConstructor
public class DataController {

    private final UsuarioService usuarioService;
    private final CategoriaService categoriaService;
    private final ProductoService productoService;
    private final PedidoService pedidoService;

    @GetMapping("/usuarios")
    public List<UsuarioDto> getUsuarios() {
        return usuarioService.findAll();
    }

    @GetMapping("/categorias")
    public List<CategoriaDto> getCategorias() {
        return categoriaService.findAll();
    }

    @GetMapping("/productos")
    public List<ProductoDto> getProductos() {
        return productoService.findAll();
    }

    @GetMapping("/pedidos")
    public List<Pedido> getPedidos() {
        return pedidoService.findAll();
    }


}