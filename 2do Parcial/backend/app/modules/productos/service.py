from datetime import UTC, datetime

from app.modules.categorias.model import Categoria
from app.modules.productos.model import Producto, ProductoCategoria
from app.modules.productos.schema import (
    CategoriaProductoPublic,
    ProductoCreate,
    ProductoPublic,
    ProductoUpdate,
)
from app.modules.unidades_medida.model import TipoUnidad, UnidadMedida
from fastapi import HTTPException, status
from sqlmodel import Session, select


# POST /api/v1/productos
def crear_producto(session: Session, data: ProductoCreate) -> ProductoPublic:

    # RN-03 Verificacion de existencia de unidad medida
    unidad = session.get(UnidadMedida, data.unidad_venta_id)

    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada",
        )

    # RN-02: Validacion de nombre unico en productos activos
    existe = session.exec(
        select(Producto).where(Producto.nombre == data.nombre, Producto.activo == True)
    ).first()

    if existe:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un producto con nombre: {data.nombre}",
        )

    # RN-10
    if (
        unidad.tipo == TipoUnidad.CONTABLE
        and data.stock_cantidad != data.stock_cantidad.to_integral_value()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El stock debe ser un número entero para unidades contables",
        )

    nuevo_producto = Producto(**data.model_dump())
    session.add(nuevo_producto)
    session.commit()
    session.refresh(nuevo_producto)

    return ProductoPublic(
        **nuevo_producto.model_dump(),
        unidad_venta=nuevo_producto.unidad_venta,
        categorias=nuevo_producto.categorias,
        hay_stock=nuevo_producto.stock_cantidad > 0,
    )


# GET /api/v1/productos
def listar_productos(
    session: Session,
    skip: int = 0,
    limit: int = 10,
    activo: bool | None = None,
    disponible: bool | None = None,
    categoria_id: int | None = None,
    search: str | None = None,
) -> list[ProductoPublic]:

    query = select(Producto)

    if activo is False:
        query = query.where(Producto.activo == False)
    else:
        query = query.where(Producto.activo == True)

    if disponible is not None:
        query = query.where(Producto.disponible == disponible)

    if search is not None and search.strip():
        query = query.where(Producto.nombre.ilike(f"%{search}%"))

    if categoria_id is not None:
        query = (
            query.join(ProductoCategoria, Producto.id == ProductoCategoria.producto_id)
            .where(ProductoCategoria.categoria_id == categoria_id)
            .distinct()
        )

    query = query.offset(skip).limit(limit)

    productos = session.exec(query).all()

    return [
        ProductoPublic(
            **producto.model_dump(),
            unidad_venta=producto.unidad_venta,
            categorias=producto.categorias,
            hay_stock=producto.stock_cantidad > 0,
        )
        for producto in productos
    ]


# GET /api/v1/productos/{id}
def obtener_producto_por_id(session: Session, producto_id: int) -> Producto:
    producto = session.get(Producto, producto_id)

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado",
        )

    return producto


# PUT /api/v1/productos/{id}
def actualizar_producto(
    session: Session, producto_id: int, data: ProductoUpdate
) -> ProductoPublic:
    producto = obtener_producto_por_id(session, producto_id)

    # RN-05
    if not producto.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede modificar un producto anulado",
        )

    unidad = session.get(UnidadMedida, data.unidad_venta_id)

    # RN-03
    if not unidad:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidad de medida no encontrada",
        )

    # RN-10
    if (
        unidad.tipo == TipoUnidad.CONTABLE
        and data.stock_cantidad != data.stock_cantidad.to_integral_value()
    ):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El stock debe ser un número entero para unidades contables",
        )

    # RN-02: Validación de nombre único
    producto_existente = session.exec(
        select(Producto).where(
            Producto.nombre == data.nombre,
            Producto.activo == True,
            Producto.id != producto_id,
        )
    ).first()

    if producto_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un producto activo con ese nombre",
        )

    # Aplicar el reemplazo completo
    producto.sqlmodel_update(data.model_dump())

    session.add(producto)
    session.commit()
    session.refresh(producto)

    return ProductoPublic(
        **producto.model_dump(),
        unidad_venta=producto.unidad_venta,
        categorias=producto.categorias,
        hay_stock=producto.stock_cantidad > 0,
    )


# DELETE /api/v1/productos/{id}
def desactivar_producto(session: Session, producto_id: int) -> Producto:
    producto = obtener_producto_por_id(session, producto_id)

    if not producto.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya no esta activo",
        )

    producto.activo = False
    producto.anulado_at = datetime.now(UTC)

    session.add(producto)
    session.commit()
    session.refresh(producto)
    
    return producto


# POST /api/v1/productos/{id}/categorias
def clasificar_producto(
    session: Session, producto_id: int, categoria_id: int, es_principal: bool
) -> ProductoCategoria:

    producto = obtener_producto_por_id(session, producto_id)
    categoria = session.get(Categoria, categoria_id)

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Categoria no encontrada"
        )

    # RN-08: No clasificar si producto o categoría están anulados
    if not producto.activo or not categoria.activo:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto y la categoria deben estar activos",
        )

    # RN-07: Un producto no puede clasificarse dos veces en la misma categoría
    vinculo_existente = session.exec(
        select(ProductoCategoria).where(
            ProductoCategoria.producto_id == producto_id,
            ProductoCategoria.categoria_id == categoria_id,
        )
    ).first()

    if vinculo_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El producto ya esta en esta categoria",
        )

    # RN-09: Un producto tiene como máximo una categoría principal
    if es_principal:
        vinculo_principal = session.exec(
            select(ProductoCategoria).where(
                ProductoCategoria.producto_id == producto_id,
                ProductoCategoria.es_principal == True,
            )
        ).first()

        if vinculo_principal:
            vinculo_principal.es_principal = False
            session.add(vinculo_principal)

    nuevo_vinculo = ProductoCategoria(
        producto_id=producto_id, categoria_id=categoria_id, es_principal=es_principal
    )

    session.add(nuevo_vinculo)
    session.commit()
    session.refresh(nuevo_vinculo)

    return nuevo_vinculo


# GET /api/v1/productos/{id}/categorias
def listar_categorias_producto(
    session: Session, producto_id: int
) -> list[CategoriaProductoPublic]:

    # Valida que el producto exista
    obtener_producto_por_id(session, producto_id)

    # union de la tabla intermedia
    vinculos = session.exec(
        select(ProductoCategoria, Categoria)
        .join(Categoria, ProductoCategoria.categoria_id == Categoria.id)
        .where(ProductoCategoria.producto_id == producto_id)
    ).all()

    resultado = []

    for vinculo, categoria in vinculos:
        resultado.append(
            CategoriaProductoPublic(
                **categoria.model_dump(), es_principal=vinculo.es_principal
            )
        )

    return resultado
