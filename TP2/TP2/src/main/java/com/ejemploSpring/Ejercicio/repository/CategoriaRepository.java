package com.ejemploSpring.Ejercicio.repository;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;


import com.ejemploSpring.Ejercicio.entities.Categoria;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface CategoriaRepository extends JpaRepository<Categoria, Long>{
    List<Categoria> findAllByEliminadoFalse();

}
