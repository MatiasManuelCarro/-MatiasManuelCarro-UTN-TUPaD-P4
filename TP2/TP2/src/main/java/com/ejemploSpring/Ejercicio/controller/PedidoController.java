package com.ejemploSpring.Ejercicio.controller;

import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoCreateConUsuario;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoDto;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoEdit;
import com.ejemploSpring.Ejercicio.entities.Pedido;
import com.ejemploSpring.Ejercicio.service.PedidoService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/pedidos")
@RequiredArgsConstructor
public class PedidoController {

    private final PedidoService pedidoService;

    // Crear pedido con detalles
    @PostMapping
    public PedidoDto create(@RequestBody PedidoCreate pedidoCreate) {
        return PedidoDto.toDto(pedidoService.save(pedidoCreate));
    }

    // Obtener pedido por ID
    @GetMapping("/{id}")
    public PedidoDto findById(@PathVariable Long id) {
        return PedidoDto.toDto(pedidoService.findById(id));
    }

    // Obtener todos los pedidos
    @GetMapping
    public List<PedidoDto> findAll() {
        return pedidoService.findAll().stream()
                .map(PedidoDto::toDto)
                .toList();
    }

    // Editar pedido (fecha, estado, forma de pago)
    @PutMapping("/{id}")
    public PedidoDto update(@PathVariable Long id, @RequestBody PedidoEdit pedidoEdit) {
        return PedidoDto.toDto(pedidoService.update(id, pedidoEdit));
    }

    // Soft delete
    @DeleteMapping("/{id}")
    public void delete(@PathVariable Long id) {
        pedidoService.deleteById(id); // baja lógica
    }

    @PostMapping("/asignar")
    public PedidoDto crearPedidoConUsuario(
            @RequestBody PedidoCreateConUsuario dto
    ) {
        Pedido pedido = pedidoService.save(dto.pedido());
        pedidoService.asignarPedido(dto.usuarioId(), pedido);
        return PedidoDto.toDto(pedido);
    }

}