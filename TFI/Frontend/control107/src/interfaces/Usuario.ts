export type RolUsuario = "ADMINISTRADOR" | "ENFERMERO";

export interface Usuario {
    id: number;
    nombre: string;
    dni: string;
    email: string;
    rol: RolUsuario;
    activo: boolean;
}

export interface CrearUsuarioRequest {
    nombre: string;
    dni: string;
    email: string;
    rol: RolUsuario;
    clave: string;
    activo: boolean;
}

export interface EditarUsuarioRequest {
    nombre: string;
    dni: string;
    email: string;
    rol: RolUsuario;
    activo: boolean;
}
