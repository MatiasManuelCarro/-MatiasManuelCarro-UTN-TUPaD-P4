package com.example.demo;

import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/ejemplo")
public class EjemploController {

    // GET: leer datos
    @GetMapping
    public Map<String, String> obtener() {
        Map<String, String> respuesta = new HashMap<>();
        respuesta.put("mensaje", "GET: recurso consultado");
        return respuesta;
    }

    // POST: crear recurso
    @PostMapping
    public Map<String, String> crear() {
        Map<String, String> respuesta = new HashMap<>();
        respuesta.put("mensaje", "POST: recurso creado");
        return respuesta;
    }

    // PUT: actualizar recurso por id
    @PutMapping("/{id}")
    public Map<String, String> actualizar(@PathVariable int id) {
        Map<String, String> respuesta = new HashMap<>();
        respuesta.put("mensaje", "PUT: recurso " + id + " actualizado");
        return respuesta;
    }

    // DELETE: eliminar recurso por id
    @DeleteMapping("/{id}")
    public Map<String, String> eliminar(@PathVariable int id) {
        Map<String, String> respuesta = new HashMap<>();
        respuesta.put("mensaje", "DELETE: recurso " + id + " eliminado");
        return respuesta;
    }
}