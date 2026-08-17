package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.detallePedido.DetallePedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoEdit;
import com.ejemploSpring.Ejercicio.entities.Pedido;

import java.util.List;

public interface PedidoService {

    Pedido save(PedidoEdit pedidoEdit, List<DetallePedidoCreate> detalles);

    Pedido findById(Long id);

    List<Pedido> findAll();

    Pedido update(Long id, PedidoEdit pedidoEdit);

    void delete(Long id);
}