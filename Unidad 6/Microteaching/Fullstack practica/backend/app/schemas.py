from sqlmodel import SQLModel

# AUTOR

class AutorCreate(SQLModel):
    nombre: str


class AutorRead(SQLModel):
    id: int
    nombre: str


class LibroRead(SQLModel):
    id: int
    titulo: str
    autor_id: int


class AutorReadWithLibros(AutorRead):
    libros: list[LibroRead] = []



# LIBRO
class LibroCreate(SQLModel):
    titulo: str
    autor_id: int


class LibroReadWithAutor(LibroRead):
    autor: AutorRead | None = None
