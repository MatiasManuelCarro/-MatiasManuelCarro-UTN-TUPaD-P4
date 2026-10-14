from sqlmodel import Session, SQLModel, create_engine

# El engine es la conexion a la base. Se crea UNA sola vez
engine = create_engine(
    "sqlite:///biblioteca.db",
    echo=True,  # muestra el SQL real que se ejectua
)


def crear_tablas():
    SQLModel.metadata.create_all(engine)

# Una sesion por request: el yield la cierra cuando el request termina. 

def get_session():
    with Session(engine) as session:
        yield session