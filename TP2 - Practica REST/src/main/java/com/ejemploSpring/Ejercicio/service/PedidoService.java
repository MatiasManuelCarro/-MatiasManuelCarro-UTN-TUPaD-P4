package com.ejemploSpring.Ejercicio.service;

import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoCreate;
import com.ejemploSpring.Ejercicio.dtos.pedido.PedidoEdit;
import com.ejemploSpring.Ejercicio.entities.Pedido;

import java.util.List;

public interface PedidoService {

    Pedido save(PedidoCreate pedidoCreate);

    Pedido findById(Long id);

    List<Pedido> findAll();

    Pedido update(Long id, PedidoEdit pedidoEdit);

    void asignarPedido(Long usuarioId, Pedido pedido);

    void deleteById(Long id);

}