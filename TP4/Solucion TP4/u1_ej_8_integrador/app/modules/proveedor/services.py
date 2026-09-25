from fastapi import HTTPException

from .schemas import ProveedorCreate, ProveedorRead

#Mockup de proveedores en la BD 
db_proveedores: list[ProveedorRead]=[
    ProveedorRead(id=1, codigo= "PROV-01", razon_social="desillas SA", cuit="27865565882", email="contacto@desillas.com", telefono="1165238469", activo=True),
    ProveedorRead(id=2, codigo="PROV-02", razon_social="Amoblamientos Garcia SRL", cuit="30715488921", email="ventas@amoblamientosgarcia.com", telefono="1145879632", activo=True),
    ProveedorRead(id=3, codigo="PROV-03", razon_social="ElectroTech SA", cuit="33687412589", email="contacto@electrotech.com.ar", telefono="1132569874", activo=True)
]
id_counter = 4

def _validar_codigo_unico(codigo: str):
    for p in db_proveedores:
        if p.codigo.lower() == codigo.lower():
            raise HTTPException(
                status_code=409,
                detail="RN-02: Ya existe un proveedor con ese código"
            )

def crear(data: ProveedorCreate) -> ProveedorRead:
    global id_counter
    _validar_codigo_unico(data.codigo)
    nuevo = ProveedorRead(id=id_counter, **data.model_dump())
    db_proveedores.append(nuevo)
    id_counter += 1
    return nuevo

def obtener_proveedores(activo: bool | None, skip: int, limit: int) -> list[ProveedorRead]:
    filtrados = [p for p in db_proveedores if activo is None or p.activo == activo]
    return filtrados[skip : skip + limit]

def obtener_por_id(id: int) -> ProveedorRead | None:
    return next((p for p in db_proveedores if p.id == id), None)

def actualizar_total(id: int, data: ProveedorCreate) -> ProveedorRead | None:
    # Reemplazo total: Requiere todos los campos validables (ProveedorCreate)
    proveedor = obtener_por_id(id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="RN-04: Proveedor no encontrado")

    if data.codigo.lower() != proveedor.codigo.lower():
        _validar_codigo_unico(data.codigo)

    for index, p in enumerate(db_proveedores):
        if p.id == id:
            proveedor_actualizado = ProveedorRead(id=id, **data.model_dump())
            db_proveedores[index] = proveedor_actualizado
            return proveedor_actualizado
    return None

def desactivar(id: int) -> ProveedorRead | None:
    # Borrado lógico: Solo altera el estado 'activo'
    proveedor = obtener_por_id(id)
    if not proveedor:
        raise HTTPException(status_code=404, detail="RN-04: Proveedor no encontrado")
    if proveedor.activo is False:
        raise HTTPException(
            status_code=409,
            detail="RN-05: El proveedor ya está desactivado"
        )
    p_dict = proveedor.model_dump()
    p_dict["activo"] = False
    proveedor_actualizado = ProveedorRead(**p_dict)
    for index, p in enumerate(db_proveedores):
        if p.id == id:
            db_proveedores[index] = proveedor_actualizado
            return proveedor_actualizado
    return None

