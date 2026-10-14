from sqlmodel import SQLModel, Field, Relationship


# ------------------------------
# Modelo intermedio (link model)
# ------------------------------
class EstudianteMateria(SQLModel, table=True):
    estudiante_id: int | None = Field(
        default=None,
        foreign_key="estudiante.id",
        primary_key=True
    )
    materia_id: int | None = Field(
        default=None,
        foreign_key="materia.id",
        primary_key=True
    )


# ------------------------------
# Modelo Estudiante
# ------------------------------
class Estudiante(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str

    materias: list["Materia"] = Relationship(
        back_populates="estudiantes",
        link_model=EstudianteMateria
    )


# ------------------------------
# Modelo Materia
# ------------------------------
class Materia(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nombre: str

    estudiantes: list["Estudiante"] = Relationship(
        back_populates="materias",
        link_model=EstudianteMateria
    )

# python -c "from app.database import crear_tablas; import app.models; crear_tablas()"