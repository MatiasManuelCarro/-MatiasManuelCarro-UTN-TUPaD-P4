

```mermaid
classDiagram
    %% ==========================================
    %% DEFINICIÓN DE DOMINIOS (NAMESPACES)
    %% ==========================================

    namespace Dominio_1_Identidad_y_Acceso {
        class Rol {
            <<Catalog>>
            === PK semántica ~no surrogate~ ===
            +codigo : VARCHAR~20~ [PK, seed]
            === Atributos ===
            +nombre : VARCHAR~50~ [UQ, NN]
            +descripcion : TEXT
        }

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
    }

    namespace Dominio_2_Catalogo_Productos {
        class Categoria {
            <<Table>>
            === PK ===
            +id : BIGSERIAL [PK]
            === FK auto-referencia ===
            +parent_id : BIGINT [FK -> Categoria.id, NULL]
            === Atributos ===
            +nombre : VARCHAR~100~ [UQ, NN]
            +descripcion : TEXT
            +imagen_url : TEXT
            === Auditoría ===
            +created_at : TIMESTAMPTZ [NN]
            +updated_at : TIMESTAMPTZ [NN]
            +deleted_at : TIMESTAMPTZ
        }

        class ProductoCategoria {
            <<Link>>
            === PK compuesta ===
            +producto_id : BIGINT [PK, FK -> Producto.id]
            +categoria_id : BIGINT [PK, FK -> Categoria.id]
            === Atributos ===
            +es_principal : BOOLEAN [NN, DEFAULT false]
            +created_at : TIMESTAMPTZ [NN]
        }

        class Producto {
            <<Table>>
            === PK ===
            +id : BIGSERIAL [PK]
            === FK ===
            +unidad_venta_id : BIGINT [FK -> UnidadMedida.id, NULL]
            === Atributos ===
            +nombre : VARCHAR~150~ [NN]
            +descripcion : TEXT
            +precio_base : DECIMAL~10,2~ [NN, CHECK >= 0]
            +imagenes_url : TEXT[]
            +stock_cantidad : INTEGER [NN, CHECK >= 0, DEFAULT 0]
            +disponible : BOOLEAN [NN, DEFAULT true]
            === Auditoría ===
            +created_at : TIMESTAMPTZ [NN]
            +updated_at : TIMESTAMPTZ [NN]
            +deleted_at : TIMESTAMPTZ
        }

        class UnidadMedida {
            <<Catalog>>
            === PK ===
            +id : BIGSERIAL [PK]
            === Atributos ===
            +nombre : VARCHAR~50~ [UQ, NN]
            +simbolo : VARCHAR~10~ [UQ, NN]
            +tipo : VARCHAR~20~ [NN]
            +created_at : TIMESTAMPTZ [NN]
        }

        class ProductoIngrediente {
            <<Link>>
            === PK compuesta ===
            +producto_id : BIGINT [PK, FK -> Producto.id]
            +ingrediente_id : BIGINT [PK, FK -> Ingrediente.id]
            === Atributos ===
            +cantidad : DECIMAL~10,3~ [NN, CHECK > 0]
            +unidad_medida_id : BIGINT [FK -> UnidadMedida.id, NN]
            +es_removible : BOOLEAN [NN, DEFAULT false]
        }

        class Ingrediente {
            <<Table>>
            === PK ===
            +id : BIGSERIAL [PK]
            === Atributos ===
            +nombre : VARCHAR~100~ [UQ, NN]
            +stock_cantidad : INTEGER [NN, CHECK >= 0, DEFAULT 0]
            +descripcion : TEXT
            +es_alergeno : BOOLEAN [NN, DEFAULT false]
            === Auditoría ===
            +created_at : TIMESTAMPTZ [NN]
            +updated_at : TIMESTAMPTZ [NN]
        }
    }

    namespace Dominio_3_Ventas_Pagos_Trazabilidad {
        class FormaPago {
            <<Catalog>>
            === PK semántica ===
            +codigo : VARCHAR~20~ [PK, seed]
            === Atributos ===
            +descripcion : VARCHAR~80~ [NN]
            +habilitado : BOOLEAN [NN, DEFAULT true]
        }

        class Pedido {
            <<Table>>
            === PK ===
            +id : BIGSERIAL [PK]
            === FK ===
            +usuario_id : BIGINT [FK -> Usuario.id, NN]
            +direccion_id : BIGINT [FK -> DireccionEntrega.id, SET NULL]
            +estado_codigo : VARCHAR~20~ [FK -> EstadoPedido.codigo, NN]
            +forma_pago_codigo : VARCHAR~20~ [FK -> FormaPago.codigo, NN]
            === Snapshot monetario ~inmutable desde creación~ ===
            +subtotal : DECIMAL~10,2~ [NN, snap]
            +descuento : DECIMAL~10,2~ [NN, DEFAULT 0.00, snap]
            +costo_envio : DECIMAL~10,2~ [NN, DEFAULT 50.00, snap]
            +total : DECIMAL~10,2~ [NN, CHECK >= 0, snap]
            === Atributos ===
            +notas : TEXT
            === Auditoría ===
            +created_at : TIMESTAMPTZ [NN]
            +updated_at : TIMESTAMPTZ [NN]
            +deleted_at : TIMESTAMPTZ
        }

        class Pago {
            <<Table>>
            === PK ===
            +id : BIGSERIAL [PK]
            === FK ===
            +pedido_id : BIGINT [FK -> Pedido.id, NN]
            === MercadoPago Checkout API ===
            +mp_payment_id : BIGINT [UQ, NULL]
            +mp_status : VARCHAR~30~ [NN]
            +mp_status_detail : VARCHAR~100~
            +external_reference : VARCHAR~100~ [UQ, NN]
            +idempotency_key : VARCHAR~100~ [UQ, NN]
            +transaction_amount : DECIMAL~10,2~ [NN]
            +payment_method_id : VARCHAR~50~
            === Auditoría ===
            +created_at : TIMESTAMPTZ [NN]
            +updated_at : TIMESTAMPTZ [NN]
        }

        class HistorialEstadoPedido {
            <<Append>>
            === PK ===
            +id : BIGSERIAL [PK]
            === FK de trazabilidad ===
            +pedido_id : BIGINT [FK -> Pedido.id, NN, CASCADE]
            +estado_desde : VARCHAR~20~ [FK -> EstadoPedido.codigo, NULL]
            +estado_hacia : VARCHAR~20~ [FK -> EstadoPedido.codigo, NN]
            +usuario_id : BIGINT [FK -> Usuario.id, NULL]
            === Atributos ===
            +motivo : TEXT
            +created_at : TIMESTAMPTZ [NN, append-only]
        }

        class EstadoPedido {
            <<Catalog>>
            === PK semántica ===
            +codigo : VARCHAR~20~ [PK, seed]
            === Atributos ===
            +descripcion : VARCHAR~80~ [NN]
            +orden : INT [NN]
            +es_terminal : BOOLEAN [NN]
        }

        class DetallePedido {
            <<Table>>
            === PK compuesta ===
            +pedido_id : BIGINT [PK, FK -> Pedido.id, CASCADE]
            +producto_id : BIGINT [PK, FK -> Producto.id, RESTRICT]
            === Atributos ===
            +cantidad : SMALLINT [NN, CHECK >= 1]
            === Snapshot ~inmutable desde creación~ ===
            +nombre_snapshot : VARCHAR~200~ [NN, snap]
            +precio_snapshot : DECIMAL~10,2~ [NN, CHECK >= 0, snap]
            +subtotal_snap : DECIMAL~10,2~ [NN, snap]
            +personalizacion : INTEGER[]
            === Auditoría ===
            +created_at : TIMESTAMPTZ [NN]
        }
    }

    %% ==========================================
    %% NOTAS Y DOCUMENTACIÓN
    %% ==========================================

    note for Rol "Seed obligatorio (app/db/seed.py):<br/>ADMIN — acceso total sin restricciones<br/>STOCK — actualiza stock y disponible<br/>PEDIDOS — avanza estados CONFIRMADO→ENTREGADO<br/>CLIENT — opera solo sus propios datos<br/><br/>PK semántica: FK legible en JWT payload<br/>Payload: { roles: ['ADMIN'] }"
    note for Producto "stock_cantidad y disponible son flags INDEPENDIENTES:<br/>stock=0 + disponible=true → badge 'Sin stock' (UI)<br/>stock>0 + disponible=false → deshabilitado por operador<br/><br/>unidad_venta_id resuelve la ambigüedad de precio_base:<br/>precio_base=12.50 + unidad='kg' → 'S/. 12.50 / kg'<br/>precio_base=3.00 + unidad=NULL → 'S/. 3.00' (por pieza)<br/><br/>Snapshot al crear DetallePedido:<br/>precio_base → DetallePedido.precio_snapshot (inmutable)<br/>nombre → DetallePedido.nombre_snapshot (inmutable)"
    note for UnidadMedida "Seed obligatorio (app/db/seed.py):<br/>— masa: kilogramo (kg), gramo (g)<br/>— volumen: litro (L), mililitro (mL)<br/>— unidad: pieza (u), docena (doc)<br/>— area: metro cuadrado (m²)<br/><br/>tipo permite filtrar/agrupar en UI de administración<br/>y habilita conversión entre unidades compatibles (v-futura).<br/>simbolo → se muestra en ProductCard: 'S/. 12.50 / kg'<br/>nombre → se usa en catálogos de administración"
    note for Ingrediente "es_alergeno = true → badge UI en:<br/>· ProductoDetail (lista de ingredientes)<br/>· ProductCard (ícono de advertencia)<br/><br/>Ingrediente es global (no duplicado por producto).<br/>ProductoIngrediente.es_removible = true → aparece en checkboxes de personalización.<br/>IDs seleccionados → DetallePedido.personalizacion[]."
    note for FormaPago "Seed obligatorio (app/db/seed.py):<br/>MERCADOPAGO — Checkout API · CardPayment SDK<br/>EFECTIVO — retiro en local (direccion_id=NULL)<br/>TRANSFERENCIA — bancaria<br/>habilitado=false: registro histórico preservado, oculto en formularios de nuevo pedido"
    note for Pago "Patrón Idempotent Payment:<br/>idempotency_key = UUID generado POR EL BACKEND.<br/>Enviado a MP en header X-Idempotency-Key.<br/>Evita cobros duplicados en reintentos del cliente.<br/><br/>Flujo webhook IPN (POST /api/v1/pagos/webhook):<br/>1. Validar firma X-Signature con MP_WEBHOOK_SECRET<br/>2. topic=payment → sdk.payment().get(resource_id)<br/>3. Si approved → avanzar Pedido a CONFIRMADO (UoW)<br/>4. UPDATE Pago.mp_status + mp_status_detail<br/>5. HTTP 200 {'status':'ok'} (MP reintenta si no recibe 200)<br/><br/>Estados MP → Food Store:<br/>approved → pedido CONFIRMADO (webhook FSM)<br/>pending → pedido sigue PENDIENTE (efectivo sin acreditar)<br/>rejected → HTTP 402, pedido sigue PENDIENTE<br/>in_process → pedido sigue PENDIENTE, webhook resolverá<br/>cancelled → cliente puede reintentar o cancelar pedido"
    note for HistorialEstadoPedido "APPEND-ONLY (RN-03): solo INSERT.<br/>Jamás UPDATE ni DELETE. Implementar como ledger de auditoría.<br/>Reconstruir estado actual: ORDER BY created_at ASC.<br/>El último registro = estado actual del pedido.<br/><br/>Flujo atómico en avanzar_estado() (UoW):<br/>1. Validar transición en mapa FSM (Service)<br/>2. UPDATE Pedido.estado_codigo<br/>3. INSERT HistorialEstadoPedido<br/>4. commit() vía UoW.exit()<br/><br/>estado_desde NULL → creación del pedido (RN-02).<br/>usuario_id NULL → actor es el sistema (webhook)."
    note for EstadoPedido "FSM — validar en Service, NUNCA en Router:<br/>PENDIENTE (ord 1, terminal=false) → CONFIRMADO → CANCELADO<br/>CONFIRMADO (ord 2, terminal=false) → EN_PREP → CANCELADO<br/>EN_PREP (ord 3, terminal=false) → EN_CAMINO → CANCELADO*<br/>ENTREGADO (ord 4, terminal=TRUE) ← terminal<br/>CANCELADO (ord 5, terminal=TRUE) ← terminal<br/>(*) solo ADMIN / PEDIDOS pueden cancelar desde EN_PREP<br/><br/>RN-01: es_terminal=true → 0 transiciones salientes.<br/>RN-02: primer HistorialEstadoPedido → estado_desde=NULL.<br/>RN-03: HistorialEstadoPedido es append-only.<br/>RN-04: Snapshot en DetallePedido → inmutable.<br/>RN-05: motivo obligatorio si estado_hacia = CANCELADO."
    note for DetallePedido "Fila INMUTABLE: sin updated_at por diseño (RN-04).<br/>Snapshot garantiza integridad histórica de precios y nombres.<br/>personalizacion = INTEGER[] con IDs de Ingrediente removidos.<br/>Ejemplo: [3, 7] = cliente removió ingredientes id=3 e id=7.<br/>Solo válido para ProductoIngrediente.es_removible = true.<br/>Schema: ItemPedidoRequest.personalizacion: list[int] | None"

    %% ==========================================
    %% RELACIONES
    %% ==========================================
    
    %% Dominio 1
    Rol "1" o-- "0..*" UsuarioRol : agrupa
    Usuario "1" *-- "0..*" UsuarioRol : posee
    Usuario "1" *-- "0..*" DireccionEntrega : invalida
    Usuario "1" o-- "0..*" UsuarioRol : asignado_por

    %% Dominio 2
    Categoria "0..1" o-- "0..*" Categoria : parent
    Categoria "1" o-- "0..*" ProductoCategoria : agrupa
    Producto "1" *-- "1..*" ProductoCategoria : clasifica
    UnidadMedida "1" o-- "0..*" Producto : unidad venta
    UnidadMedida "1" o-- "0..*" ProductoIngrediente : mide
    Producto "1" *-- "0..*" ProductoIngrediente : contiene
    Ingrediente "1" o-- "0..*" ProductoIngrediente : referencia

    %% Dominio 3 y Conexiones Multi-Dominio
    FormaPago "1" o-- "0..*" Pedido : pagado con
    DireccionEntrega "0..1" o-- "0..*" Pedido : destino
    Usuario "1" o-- "0..*" Pedido : realiza
    Pedido "1" *-- "0..*" Pago : registra
    Pedido "1" *-- "0..*" HistorialEstadoPedido : historial
    Usuario "1" o-- "0..*" HistorialEstadoPedido : modifico
    EstadoPedido "1" o-- "0..*" HistorialEstadoPedido : desde
    EstadoPedido "1" o-- "0..*" HistorialEstadoPedido : hacia
    EstadoPedido "1" o-- "0..*" Pedido : en estado
    Pedido "1" *-- "1..*" DetallePedido : contiene
    Producto "1" o-- "0..*" DetallePedido : referenciado
    ```