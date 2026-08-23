package com.ejemploSpring.Ejercicio.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {

    @GetMapping("/")
    public String home() {
        return "App funcionando - Ingresar a localhost:8080/h2-console para ver la base de datos";
    }
}
