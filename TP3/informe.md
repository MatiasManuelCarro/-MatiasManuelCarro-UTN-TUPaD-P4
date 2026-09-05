# Informe Técnico de Diseño y Migración (POO Python)

## 1. Diagnóstico de Java-ismos (Parte 1)

| # | Java-ismo | Dónde | Inversión | Síntoma observable |
|---|---|---|---|---|
| 1 | Getters preventivos sin lógica | `Figura.getNombre`, `Figura.getColor` | Compilador → Acuerdo | Atributos envueltos en métodos vacíos innecesarios; en Python nacen públicos y directos[cite: 2]. |
| 2 | Getter/Setter tradicional (Java Bean) | `Lado.getLongitud`, `Lado.setLongitud` | Compilador → Acuerdo | Ceremonia sintáctica; en Python se usa `@property` solo para validar `longitud > 0`[cite: 2]. |
| 3 | Variable mutable de clase (`static`) | `Poligono.catalogo = []` | Declaración → Runtime | La lista vive en el objeto de clase; cualquier instancia corrompe el catálogo global[cite: 2]. |
| 4 | Argumentos por defecto mutables | `Poligono.__init__(lados=[], ...)` | Declaración → Runtime | La lista se evalúa al cargar el módulo; dos instancias comparten la misma lista en RAM[cite: 2]. |
| 5 | Omitir `super().__init__()` | `Poligono.__init__` | Compilador → Acuerdo | No se ejecuta la base `Figura`; `_construida = True` nunca se inicializa[cite: 2]. |
| 6 | Retorno de referencias mutables | `Poligono.getLados` | Compilador → Acuerdo | Exposición del estado interno; un actor externo puede vaciar la lista con `.clear()`[cite: 2]. |
| 7 | Acumulador imperativo en bucle | `Poligono.perimetro` | Compilador → Acuerdo | Código verboso de bajo nivel en lugar de generadores declarativos con `sum()`[cite: 2]. |
| 8 | Sobrecarga emulada con `*args` | `Triangulo.__init__`, `Cuadrado.__init__` | Herencia → Duck typing | Ramas de `isinstance` frágiles; se resuelve con `@classmethod` semánticos[cite: 2]. |

---

## 2. Tabla de Equivalencias del Código Entregado

| Elemento en Java | Cómo quedó en tu código Python | ¿Traducción o rediseño? | Por qué |
|---|---|---|---|
| `public double getLongitud()` / `setLongitud(...)` | `@property` y `@longitud.setter` en `Lado` | Rediseño | Interfaz limpia de atributo (`lado.longitud = 5`) sin perder la validación `valor > 0` en el setter[cite: 2]. |
| `public List<Lado> getLados()` | `def lados(self) -> tuple[Lado, ...]` en `Poligono` | Rediseño | Copia defensiva en salida; la tupla inmutable impide alteraciones externas (`.clear()`, `.pop()`)[cite: 2]. |
| `abstract class PoligonoRegular extends Poligono` | `def es_regular(self) -> bool` en `Poligono` | Rediseño | La regularidad es un estado geométrico dinámico de los lados, no un tipo jerárquico ontológico[cite: 2]. |
| `public interface Exportable` | `@runtime_checkable class Exportable(Protocol)` | Rediseño | Subtipado estructural; permite tipar `PlanoCAD` externo sin tocarlo ni forzar herencia nominal[cite: 1, 2]. |
| Sobrecarga de constructores `Triangulo(...)` | `@classmethod regular(...)` y valores `None` | Rediseño | Sustituye la sobrecarga estática por constructores semánticos explícitos evitando `*args`[cite: 2]. |
| `static List<Poligono> catalogo` | `Taller(poligonos=...)` y método `recibir()` | Rediseño | Agregación explícita de instancias desacopladas en lugar de estado global mutable en la clase[cite: 2]. |
| Validación de tipos con `instanceof` | `lados_esperados()` y falla temprana al instanciar | Rediseño | Valida invariantes semánticas en runtime durante `__init__`, arrojando `TypeError` o `ValueError`[cite: 2]. |

---

## 3. Las Tres Relaciones Estructurales (Parte 2)

La asignación `self._x = x` es sintácticamente idéntica, pero las relaciones se delatan por la gestión del ciclo de vida, la firma y las copias defensivas:
* **Asociación (`Lado — Etiqueta`, 0..1):** Se delata en `__init__(..., etiqueta: Etiqueta | None = None) -> None:`[cite: 2]. El type hint de unión y el valor por defecto indican que el colaborador es opcional y externo; si el lado desaparece, la etiqueta no se ve afectada[cite: 2].
* **Agregación (`Taller — Poligono`, 0..*):** Se delata en `self._inventario: list[Poligono] = list(poligonos) if poligonos is not None else []` y `def recibir(self, p: Poligono)`[cite: 2]. El taller agrupa figuras ya creadas en el exterior sin instanciarlas internamente ni condicionar su existencia[cite: 2].
* **Composición (`Poligono — Lado`, 3..*):** Se delata en el aislamiento defensivo `self._lados = list(lados)` en la entrada junto a `return tuple(self._lados)` en la salida, condicionado por `lados_esperados()`[cite: 2]. El polígono se adueña de la colección; sin sus lados pierde entidad estructural[cite: 2].

---

## 4. Herencia y Decisión sobre `PoligonoRegular` (Parte 3)

Se descartó la herencia y se eliminó la clase `PoligonoRegular`[cite: 2]. En Java se modelaba como subtipo por la necesidad del compilador de agrupar colecciones homogéneas (`List<PoligonoRegular>`)[cite: 2]. En el dominio real, la regularidad no es una esencia («es-un»), sino un estado geométrico contingente: un triángulo no muta de clase ontológica por tener lados iguales[cite: 2]. Se rediseñó mediante:
1. Una consulta semántica de estado en la base: `def es_regular(self) -> bool`[cite: 2].
2. Constructores de clase alternativos en las subclases: `@classmethod regular(...)`[cite: 2].

---

## 5. Cierre: ABC vs. Protocol, ¿Lenguaje o Dominio? (Parte 4)

**La decide el dominio; el lenguaje solo provee la herramienta técnica[cite: 2].**
* **ABC (Subtipado nominal / «Es-un»):** Se usó para `Poligono` porque comparte identidad, ciclo de vida, atributos base (`nombre`, `color`) y una plantilla rígida de construcción (`lados_esperados()`)[cite: 2].
* **Protocol (Subtipado estructural / «Sabe-hacer»):** Se usó para `Exportable` porque modela una capacidad transversal[cite: 2]. Un `PlanoCAD` y un `Triangulo` no tienen ancestros comunes ni comparten estado, pero ambos exponen `exportar() -> str`[cite: 1, 2]. Una ABC hubiera exigido modificar código externo cerrado o recurrir a registros dinámicos invasivos[cite: 1, 2].

---

## 6. Distinción entre Diseño y Sintaxis

* **Lo que cambió (sintaxis y modelo de ejecución):** La ilusión de privacidad estática se sustituyó por acuerdos de encapsulamiento (`@property`, copias defensivas explícitas)[cite: 2]. Las jerarquías rígidas creadas para complacer al compilador de Java (`PoligonoRegular`, sobrecargas) desaparecieron a favor de duck typing, constructores semánticos y protocolos estructurales[cite: 2].
* **Lo que se mantuvo idéntico (diseño conceptual de fondo):** Las invariantes de dominio fundamentales. Un polígono sigue requiriendo al menos 3 lados[cite: 2], la relación entre figuras y taller continúa siendo una agregación débil donde las figuras sobreviven al contenedor[cite: 2], y el polimorfismo garantiza que el cliente opere sobre contratos sin conocer la implementación concreta[cite: 2].