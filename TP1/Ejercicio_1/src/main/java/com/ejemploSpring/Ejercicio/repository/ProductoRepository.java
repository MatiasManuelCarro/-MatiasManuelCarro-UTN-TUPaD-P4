package com.ejemploSpring.Ejercicio.repository;

import com.ejemploSpring.Ejercicio.entities.Producto;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


@Repository
public interface ProductoRepository extends JpaRepository<Producto, Long> {

}
