package com.ejemploSpring.Ejercicio.repository;

import com.ejemploSpring.Ejercicio.entities.Pedido;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PedidoRepository  extends JpaRepository<Pedido, Long> {
}
