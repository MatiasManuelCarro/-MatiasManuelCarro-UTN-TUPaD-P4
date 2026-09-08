"""
Módulo: Dominio 1 - Identidad & Acceso (Orientado a Objetos Puro)
"""

from datetime import datetime, timezone

# -------------------------------------------------------------------
# 1. CLASES "PARTE" O DEPENDIENTES
# -------------------------------------------------------------------

class DireccionEntrega:
    """Clase parte. Será fabricada mediante Composición por el Usuario."""
    
    def __init__(self, linea1: str, ciudad: str, alias: str = "", 
                 linea2: str = "", provincia: str = "", codigo_postal: str = "", 
                 es_principal: bool = False) -> None:
        # Atributos propios
        self.alias = alias
        self.linea1 = linea1
        self.linea2 = linea2
        self.ciudad = ciudad
        self.provincia = provincia
        self.codigo_postal = codigo_postal
        self.es_principal = es_principal
        
        # Auditoría automática (al instanciar)
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
        self.deleted_at: datetime | None = None

    def __repr__(self) -> str:
        return f"DireccionEntrega('{self.alias or self.linea1}', ciudad='{self.ciudad}')"


class UsuarioRol:
    """Clase Link/Asociación. Será fabricada mediante Composición por el Usuario."""
    
    def __init__(self, rol: 'Rol', asignado_por: 'Usuario | None' = None, 
                 expires_at: datetime | None = None) -> None:
        # En OOP puro guardamos la referencia al objeto, no el ID/FK
        self.rol = rol 
        self.asignado_por = asignado_por  
        self.expires_at = expires_at
        self.created_at = datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"UsuarioRol(rol='{self.rol.codigo}')"


# -------------------------------------------------------------------
# 2. CLASES PRINCIPALES ("TODOS")
# -------------------------------------------------------------------

class Rol:
    """
    Catálogo de Roles. 
    Se relaciona por AGREGACIÓN (rombo blanco) con UsuarioRol.
    """
    
    def __init__(self, codigo: str, nombre: str, descripcion: str = "") -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        
        # Asociación 0..*: inicia vacía
        self._usuarios_agrupados: list[UsuarioRol] = []

    # AGREGACIÓN: recibe la parte (UsuarioRol) YA CONSTRUIDA por parámetro
    def agrupar_usuario(self, usuario_rol: UsuarioRol) -> None:
        self._usuarios_agrupados.append(usuario_rol)

    @property
    def usuarios_agrupados(self) -> tuple[UsuarioRol, ...]:
        return tuple(self._usuarios_agrupados)

    def __repr__(self) -> str:
        return f"Rol({self.codigo})"


class Usuario:
    """
    Entidad principal. 
    Se relaciona por COMPOSICIÓN (rombo negro) con DireccionEntrega y UsuarioRol.
    """
    
    def __init__(self, nombre: str, apellido: str, email: str, password_hash: str, celular: str = "") -> None:
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.celular = celular
        self.password_hash = password_hash
        
        self.created_at = datetime.now(timezone.utc)
        self.updated_at = self.created_at
        self.deleted_at: datetime | None = None
        
        # Contenedores para las composiciones (protegidos)
        self._roles: list[UsuarioRol] = []
        self._direcciones: list[DireccionEntrega] = []

    # COMPOSICIÓN 1: El Usuario FABRICA su propia dirección internamente
    def agregar_direccion(self, linea1: str, ciudad: str, alias: str = "", 
                          es_principal: bool = False) -> DireccionEntrega:
        
        nueva_direccion = DireccionEntrega(
            linea1=linea1, ciudad=ciudad, alias=alias, es_principal=es_principal
        )
        self._direcciones.append(nueva_direccion)
        return nueva_direccion

    # COMPOSICIÓN 2: El Usuario FABRICA su propia asignación de rol internamente
    def asignar_rol(self, rol: Rol, asignador: 'Usuario | None' = None) -> UsuarioRol:
        
        nuevo_rol = UsuarioRol(rol=rol, asignado_por=asignador)
        self._roles.append(nuevo_rol)
        
        # Disparamos la agregación inversa para que el Rol también se entere
        rol.agrupar_usuario(nuevo_rol)
        
        return nuevo_rol

    # Properties de solo lectura para evitar que "trasplanten" partes desde afuera
    @property
    def direcciones(self) -> tuple[DireccionEntrega, ...]:
        return tuple(self._direcciones)
        
    @property
    def roles(self) -> tuple[UsuarioRol, ...]:
        return tuple(self._roles)

    def __repr__(self) -> str:
        return f"Usuario({self.email})"


# -------------------------------------------------------------------
# SCRIPT DE PRUEBA (Validando el Ciclo de Vida)
# -------------------------------------------------------------------

if __name__ == "__main__":
    print("=== 1. Creación de Objetos Independientes ===")
    rol_admin = Rol("ADMIN", "Administrador del Sistema")
    admin_user = Usuario("Ignacio", "Carné", "admin@foodstore.com", "hash123")
    cliente = Usuario("Hugo", "Catalan", "hugo@email.com", "hash456")
    print(rol_admin)
    print(admin_user)
    
    print("\n=== 2. Composición: El Usuario fabrica sus partes ===")
    # Se pasa la data, el usuario construye el objeto por dentro
    cliente.agregar_direccion(linea1="Calle Falsa 123", ciudad="Buenos Aires", alias="Casa")
    
    # Se pasa la referencia del rol, el usuario construye el UsuarioRol por dentro
    cliente.asignar_rol(rol=rol_admin, asignador=admin_user)
    
    print("Roles de Hugo:", cliente.roles)
    print("Direcciones de Hugo:", cliente.direcciones)
    
    print("\n=== 3. Agregación: El Rol recibió la parte ya armada ===")
    # Validamos que el Rol tiene agregado el "UsuarioRol" (Agregación)
    print("Usuarios agrupados en ADMIN:", rol_admin.usuarios_agrupados)
    
    print("\n=== 4. Prueba del Ciclo de Vida ===")
    # Si borro a Hugo, mueren sus direcciones y la instancia UsuarioRol porque no tienen
    # variables globales que las apunten, nacieron atadas a la vida de su Usuario.
    del cliente
    print("El usuario Hugo fue eliminado del sistema.")
    print("¿El rol ADMIN sigue existiendo?:", rol_admin)