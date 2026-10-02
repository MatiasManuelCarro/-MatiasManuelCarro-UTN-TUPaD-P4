from sqlmodel import Field, Relationship, SQLModel

# Un autor escribe mucho libros. Un libro tiene un solo autor

class Autor(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    
    # EI lado "Uno" NO es una columna: es el puente en Python
    # para llegar a los libros de este autor.
    libros: list["Libro"] = Relationship(back_populates="autor")

class Libro(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    
    # ESTA si es una columna real de Ia tabla: guarda el id del autor.
    # Es Ia clave foranea, y es 10 unico que hace falta para un I:N.
    autor_id: int | None = Field(default=None, foreign_key="autor.id")

    # back_populates conecta los dos lados: si agrego un libro
    # a autor.libros, este campo se completa solo.
    autor: Autor | None = Relationship(back_populates="libros")

#PARA CREAR LAS TABLAS USANDO LA TERMINAL
# python -c "from app.database import crear_tablas; import app.models; crear_tablas()"