
Diagrama uml

```mermaid
classDiagram
    class Rol {
        <<Catalog>>
        
        === PK semántica ~no surrogate~ ===
        +codigo : VARCHAR~20~ [PK, seed]
        
        === Atributos ===
        +nombre : VARCHAR~50~ [UQ, NN]
        +descripcion : TEXT
    }

    note for Rol "Seed obligatorio (app/db/seed.py):<br/>ADMIN — acceso total sin restricciones<br/>STOCK — actualiza stock y disponible<br/>PEDIDOS — avanza estados CONFIRMADO→ENTREGADO<br/>CLIENT — opera solo sus propios datos<br/><br/>PK semántica: FK legible en JWT payload<br/>Payload: { roles: ['ADMIN'] }"

    class UsuarioRol {
        <<Link>>
        
        === PK compuesta ===
        +usuario_id : BIGINT [PK, FK -> Usuario.id]
        +rol_codigo : VARCHAR~20~ [PK, FK -> Rol.codigo]
        
        === Atributos ===
        +asignado_por_id : BIGINT [FK -> Usuario.id, NULL]
        +expires_at : TIMESTAMPTZ

        === Audit ===
        +created_at : TIMESTAMPTZ [NN]
    }

    class Usuario {
        <<Table>>
        
        === PK ===
        +id : BIGSERIAL [PK]
        
        === Datos personales ===
        +nombre : VARCHAR~80~ [NN]
        +apellido : VARCHAR~80~ [NN]
        +email : VARCHAR~254~ [UQ, NN]
        +celular : VARCHAR~20~
        +password_hash : CHAR~60~ [NN, bcrypt]
        
        === Audit ===
        +created_at : TIMESTAMPTZ [NN]
        +updated_at : TIMESTAMPTZ [NN]
        +deleted_at : TIMESTAMPTZ
    }

    class DireccionEntrega {
        <<Table>>
        
        === PK ===
        +id : BIGSERIAL [PK]
        
        === FK ===
        +usuario_id : BIGINT [FK -> Usuario.id, NN]
        
        === Atributos ===
        +alias : VARCHAR~50~
        +linea1 : TEXT [NN]
        +linea2 : TEXT
        +ciudad : VARCHAR~100~ [NN]
        +provincia : VARCHAR~100~
        +codigo_postal : VARCHAR~10~
        +es_principal : BOOLEAN [NN, DEFAULT false]
        
        === Audit ===
        +created_at : TIMESTAMPTZ [NN]
        +updated_at : TIMESTAMPTZ [NN]
        +deleted_at : TIMESTAMPTZ
    }

    %% Relaciones (Respetando la cardinalidad y tipo de flechas de tu prompt)
    Rol "1" o-- "0..*" UsuarioRol : agrupa
    Usuario "1" *-- "0..*" UsuarioRol : posee
    Usuario "1" *-- "0..*" DireccionEntrega : invalida
    Usuario "1" o-- "0..*" UsuarioRol: asignado_por

    ```