from fastapi import APIRouter, HTTPException

from .utils import find_by_id, load_json, save_json

router = APIRouter(prefix="/v1/turnos")


# ---------------------------------------------------------
# GET /v1/turnos
# ---------------------------------------------------------
@router.get("")
def listar_turnos():
    data = load_json("turnos")
    print("TURNOS CARGADOS:", data)
    return data


# ---------------------------------------------------------
# GET /v1/turnos/{id}
# ---------------------------------------------------------
@router.get("/{turno_id}")
def obtener_turno(turno_id: int):
    turnos = load_json("turnos")
    turno = find_by_id(turnos, turno_id)
    if not turno:
        raise HTTPException(404, "Turno no encontrado")
    return turno


# ---------------------------------------------------------
# POST /v1/turnos
# ---------------------------------------------------------
@router.post("")
def crear_turno(body: dict):
    """
    Body según OpenAPI (TurnoRequestDTO):
    {
      "fecha": "2026-10-12",
      "horario": "MANIANA",
      "adminId": 1,
      "enfermeroId": 2,
      "ambulanciaId": 3,
      "nombreChofer": "Carlos",
      "nombreMedico": "Dr. Pérez"
    }
    """
    turnos = load_json("turnos")
    nuevo_id = max([t["id"] for t in turnos], default=0) + 1

    nuevo_turno = {
        "id": nuevo_id,
        "fecha": body["fecha"],
        "horario": body["horario"],
        "estado": "PROGRAMADO",
        "chofer": body.get("nombreChofer"),
        "medico": body.get("nombreMedico"),
        "ambulancia": {"id": body["ambulanciaId"]},
        "enfermero": {"id": body["enfermeroId"]},
        "admin": {"id": body["adminId"]},
        "observacionesIngreso": None,
        "observacionesEgreso": None,
        "controlInsumos": [],
    }

    turnos.append(nuevo_turno)
    save_json("turnos", turnos)
    return nuevo_turno


# ---------------------------------------------------------
# PUT /v1/turnos/{id}
# ---------------------------------------------------------
@router.put("/{turno_id}")
def modificar_turno(turno_id: int, body: dict):
    turnos = load_json("turnos")
    turno = find_by_id(turnos, turno_id)

    if not turno:
        raise HTTPException(404, "Turno no encontrado")

    for campo in ["fecha", "horario", "estado"]:
        if campo in body:
            turno[campo] = body[campo]

    if "nombreChofer" in body:
        turno["chofer"] = body["nombreChofer"]

    if "nombreMedico" in body:
        turno["medico"] = body["nombreMedico"]

    if "ambulanciaId" in body:
        turno["ambulancia"] = {"id": body["ambulanciaId"]}

    if "enfermeroId" in body:
        turno["enfermero"] = {"id": body["enfermeroId"]}

    if "adminId" in body:
        turno["admin"] = {"id": body["adminId"]}

    save_json("turnos", turnos)
    return turno


# ---------------------------------------------------------
# POST /v1/turnos/{id}/cancelar
# ---------------------------------------------------------
@router.post("/{turno_id}/cancelar")
def cancelar_turno(turno_id: int, body: dict):
    turnos = load_json("turnos")
    turno = find_by_id(turnos, turno_id)

    if not turno:
        raise HTTPException(404, "Turno no encontrado")

    turno["estado"] = "CANCELADO"
    turno["observacionesEgreso"] = body.get("observaciones")

    save_json("turnos", turnos)
    return turno


# ---------------------------------------------------------
# POST /v1/turnos/ingreso
# ---------------------------------------------------------
@router.post("/ingreso")
def registrar_ingreso(body: dict):
    """
    Body según OpenAPI (IngresoEgresoDTO):
    {
      "turnoId": 1,
      "insumos": [
        { "id": 1, "cantidad": 10, "cantidadRestockeo": 0 }
      ],
      "observaciones": "string"
    }
    """
    turnos = load_json("turnos")
    turno = find_by_id(turnos, body["turnoId"])

    if not turno:
        raise HTTPException(404, "Turno no encontrado")

    turno["observacionesIngreso"] = body.get("observaciones")

    # Agregar control de insumos
    control_insumos = load_json("control_insumos")
    nuevo_id = max([c["id"] for c in control_insumos], default=0) + 1

    for insumo in body["insumos"]:
        control_insumos.append(
            {
                "id": nuevo_id,
                "turno_id": body["turnoId"],
                "insumo_id": insumo["id"],
                "cantidad_ingreso": insumo["cantidad"],
                "cantidad_restockeo": insumo.get("cantidadRestockeo", 0),
                "cantidad_egreso": None,
            }
        )
        nuevo_id += 1

    save_json("control_insumos", control_insumos)
    save_json("turnos", turnos)

    return turno


# ---------------------------------------------------------
# POST /v1/turnos/egreso
# ---------------------------------------------------------
@router.post("/egreso")
def registrar_egreso(body: dict):
    turnos = load_json("turnos")
    turno = find_by_id(turnos, body["turnoId"])

    if not turno:
        raise HTTPException(404, "Turno no encontrado")

    turno["observacionesEgreso"] = body.get("observaciones")

    control_insumos = load_json("control_insumos")

    for insumo in body["insumos"]:
        control = find_by_id(control_insumos, insumo["id"])
        if control:
            control["cantidad_egreso"] = insumo["cantidad"]

    save_json("control_insumos", control_insumos)
    save_json("turnos", turnos)

    return turno


# ---------------------------------------------------------
# GET /v1/turnos/activos
# ---------------------------------------------------------
@router.get("/activos")
def obtener_turnos_activos():
    turnos = load_json("turnos")
    activos = [t for t in turnos if t["estado"] in ["PROGRAMADO", "EN_CURSO"]]
    return activos


# ---------------------------------------------------------
# GET /v1/turnos/resumen
# ---------------------------------------------------------
@router.get("/resumen")
def resumen_operativo():
    turnos = load_json("turnos")
    ambulancias = load_json("ambulancias")

    activos = len([t for t in turnos if t["estado"] == "EN_CURSO"])
    disponibles = len([a for a in ambulancias if a.get("disponible", True)])
    totales = len(ambulancias)

    return {
        "turnosActivos": activos,
        "ambulanciasDisponibles": disponibles,
        "ambulanciasTotales": totales,
        "alertas": 0,
        "inconsistencias": 0,
        "listaAmbulancias": ambulancias,
    }
