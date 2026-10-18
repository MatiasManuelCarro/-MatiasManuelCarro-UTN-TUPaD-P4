```
backend/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py        # SQLAlchemy + SessionLocal + engine
│   │
│   ├── catalogo/
│   │   ├── models.py          # SQLAlchemy ORM (Categoria, Producto, ProductoCategoria)
│   │   ├── schemas.py         # Pydantic (request/response)
│   │   ├── service.py         # CRUD con SQLAlchemy
│   │   └── router.py          # Endpoints FastAPI
│
├── requirements.txt
└── README.md


```