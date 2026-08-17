package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashMap;
import java.util.Map;

@RestController
public class SaludoController {

    @GetMapping("/saludo")
    public String obtenerSaludo() {
        return "Saludo: Hola!";
    }

    @GetMapping("/usuario")
    public Map<String, String> obtenerUsuario() {
        Map<String, String> usuario = new HashMap<>();
        usuario.put("nombre", "jose");
        usuario.put("apellido", "Douglas");
        return usuario;
    }
}
