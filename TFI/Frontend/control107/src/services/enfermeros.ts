export async function listarEnfermeros() {
    const res = await fetch("http://localhost:8000/v1/usuarios");
    if (!res.ok) {
        throw new Error("Error al listar enfermeros");
    }

    const usuarios = await res.json();

    return usuarios.filter((u: any) => u.rol === "ENFERMERO");
}

export async function listarEnfermerosActivos() {
    const res = await fetch("http://localhost:8000/v1/usuarios");
    if (!res.ok) {
        throw new Error("Error al listar enfermeros activos");
    }

    const usuarios = await res.json();

    return usuarios.filter(
        (u: any) => u.rol === "ENFERMERO" && u.activo === true
    );
}
