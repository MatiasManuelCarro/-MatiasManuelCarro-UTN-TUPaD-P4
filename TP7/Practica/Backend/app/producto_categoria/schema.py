from sqlmodel import SQLModel


class ProductoCategoriaCreate(SQLModel):
    producto_id: int
    categoria_id: int
    es_principal: bool = False


class ProductoCategoriaPublic(SQLModel):
    producto_id: int
    categoria_id: int
    es_principal: bool

    class Config:
        orm_mode = True
