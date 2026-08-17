package com.ejemploSpring.Ejercicio.repository;

import com.ejemploSpring.Ejercicio.entities.Usuario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
}
