from app.models.proveedor import Proveedor
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate
from fastapi import HTTPException, status
from sqlmodel import Session, select


def crear_proveedor(session: Session, data: ProveedorCreate) -> Proveedor:
    # RN-02: Código único
    existe = session.exec(
        select(Proveedor).where(Proveedor.codigo == data.codigo)
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"RN-02: Ya existe un proveedor con código: {data.codigo}",
        )

    nuevo_proveedor = Proveedor(**data.model_dump())
    session.add(nuevo_proveedor)
    session.commit()
    session.refresh(nuevo_proveedor)
    return nuevo_proveedor


def listar_proveedores(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
) -> list[Proveedor]:

    query = select(Proveedor)

    if activo is not None:
        query = query.where(Proveedor.activo == activo)

    query = query.offset(skip).limit(limit)
    return list(session.exec(query).all())


def obtener_proveedor_por_id(session: Session, proveedor_id: int) -> Proveedor:
    proveedor = session.get(Proveedor, proveedor_id)

    if not proveedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="RN-04: Proveedor no encontrado",
        )

    return proveedor


def actualizar_proveedor(session: Session, proveedor_id: int, data: ProveedorUpdate) -> Proveedor:
    proveedor = obtener_proveedor_por_id(session, proveedor_id)

    cambios = data.model_dump(exclude_unset=True)

    # RN-02: Código único (solo si cambia)
    if "codigo" in cambios and cambios["codigo"].lower() != proveedor.codigo.lower():
        existe = session.exec(
            select(Proveedor).where(Proveedor.codigo == cambios["codigo"])
        ).first()

        if existe:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"RN-02: Ya existe un proveedor con código: {cambios['codigo']}",
            )

    proveedor.sqlmodel_update(cambios)

    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor


def desactivar_proveedor(session: Session, proveedor_id: int) -> Proveedor:
    proveedor = obtener_proveedor_por_id(session, proveedor_id)

    if not proveedor.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="RN-05: El proveedor ya está desactivado",
        )

    proveedor.activo = False

    session.add(proveedor)
    session.commit()
    session.refresh(proveedor)
    return proveedor
