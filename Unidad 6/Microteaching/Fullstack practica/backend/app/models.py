from sqlmodel import Field, Relationship, SQLModel

class Autor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str

    libros: list["Libro"] = Relationship(back_populates="autor")


class Libro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str

    autor_id: int | None = Field(default=None, foreign_key="autor.id")
    autor: Autor | None = Relationship(back_populates="libros")
