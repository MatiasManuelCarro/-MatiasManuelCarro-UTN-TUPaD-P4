package com.ejemploSpring.Ejercicio.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {

    @GetMapping("/")
    public String home() {
        return """
                <style>
                     body { font-family: Arial; padding: 20px; }
                     h1 { margin-bottom: 10px; }
                     pre { background: #f4f4f4; padding: 15px; border-radius: 5px; }
                     a { color: blue; }
                     </style>
                
                     <h1>API funcionando</h1>
      
                <pre>
                <h2>Consola H2:</h2>
                - <a href="http://localhost:8080/h2-console">http://localhost:8080/h2-console</a>
                
                =====================================
                <h2>USUARIOS (/usuarios)</h2>
                =====================================
                - <a href="http://localhost:8080/usuarios">http://localhost:8080/usuarios</a>
                
                GET  /usuarios                 listar todos
                GET  /usuarios/{id}            buscar por ID
                GET  /usuarios/{id}/nombre     obtener nombre y apellido
                GET  /usuarios/mail/{mail}     buscar por email
                POST /usuarios                 crear usuario
                PUT  /usuarios/{id}            editar usuario
                DELETE /usuarios/{id}          eliminar usuario
                
                =====================================
                <h2>PRODUCTOS (/productos)</h2>
                =====================================
                - <a href="http://localhost:8080/productos">http://localhost:8080/productos</a>
                
                GET  /productos                listar todos
                GET  /productos/eliminados     listar eliminados
                GET  /productos/{id}           buscar por ID
                POST /productos                crear producto
                PUT  /productos/{id}           editar producto
                DELETE /productos/{id}         eliminar producto
                
                =====================================
                <h2>PEDIDOS (/pedidos)</h2>
                =====================================
                - <a href="http://localhost:8080/pedidos">http://localhost:8080/pedidos</a>
                
                GET  /pedidos                  listar todos
                GET  /pedidos/{id}             buscar por ID
                POST /pedidos                  crear pedido
                PUT  /pedidos/{id}             editar pedido
                DELETE /pedidos/{id}           baja lógica
                POST /pedidos/asignar          crear pedido y asignarlo a usuario
                
                =====================================
                <h2>CATEGORIAS (/categorias)</h2>
                =====================================
                - <a href="http://localhost:8080/categorias">http://localhost:8080/categorias</a>
                
                GET  /categorias               listar activas
                GET  /categorias/{id}          buscar por ID
                POST /categorias               crear categoría
                PUT  /categorias/{id}          editar categoría
                DELETE /categorias/{id}        baja lógica
                </pre>            
            """;
    }
}
