# Informe Técnico de Diseño y Migración (POO Python)

## 1. Diagnóstico de Java-ismos (Parte 1)

| # | Java‑ismo | Ubicación (clase.método) | Principio que lo explica | Síntoma observable |
|---|---|---|---|---|
| 1 | Getters preventivos sin lógica (`getNombre`, `getColor`) | `Figura.getNombre`, `Figura.getColor` | **Compilador – Acuerdo** (Encapsulamiento por convención) | En Java se implementan para anticipar posibles cambios futuros en los atributos. En Python los atributos se exponen de manera directa (`figura.nombre`), y si en algún momento se requiere validación, se incorpora `@property` sin afectar el código existente. |
| 2 | Getter y Setter tradicionales estilo Java Bean | `Lado.getLongitud`, `Lado.setLongitud` | **Compilador – Acuerdo** (`@property` para lógica concreta) | Obliga a utilizar métodos extensos como `lado.getLongitud()` o `lado.setLongitud(5)`. En Python se emplea `@property` para mantener un acceso simple (`lado.longitud = 5`) mientras se valida internamente que el valor no sea negativo. |
| 3 | Variable mutable de clase utilizada como `static` compartido | `Poligono.catalogo = []` | **Declaración – Runtime** (Objetos de clase compartidos) | La lista pertenece a la clase y no a cada instancia. Si cualquier parte del programa la modifica, afecta simultáneamente a todos los polígonos, generando un estado global no controlado. |
| 4 | Argumentos por defecto mutables (`lados=[]`, `observaciones=[]`) | `Poligono.__init__` | **Declaración – Runtime** (Valores por defecto evaluados al inicio) | La lista vacía se crea una única vez al cargar el archivo. Si se instancian dos polígonos sin proporcionar observaciones, ambos comparten la misma lista en memoria (`p1._observaciones is p2._observaciones` resulta `True`). |
| 5 | Omitir `super().__init__()` y asignar atributos manualmente | `Poligono.__init__` | **Compilador – Acuerdo** (Cadena de herencia) | El constructor de la clase base (`Figura`) no se ejecuta. Como consecuencia, el atributo de control `_construida = True` nunca se inicializa, dejando la instancia incompleta. |
| 6 | Guardar y devolver la lista interna sin copia defensiva | `Poligono.__init__` y `Poligono.getLados` | **Compilador – Acuerdo** (Protección del estado interno) | Código externo puede modificar la lista interna mediante operaciones como `.clear()`, alterando la estructura del polígono sin que este pueda evitarlo. |
| 7 | Uso de un bucle `for` con acumulador manual en lugar de herramientas nativas | `Poligono.perimetro` | **Compilador – Acuerdo** (Aprovechamiento del lenguaje) | Se implementan varias líneas de código imperativo para una operación que en Python puede expresarse de manera más clara y eficiente mediante `sum(...)`. |
| 8 | Simulación de sobrecarga de constructores con `*args` e `isinstance` | `Triangulo.__init__` y `Cuadrado.__init__` | **Herencia – Duck typing** (Constructores alternativos) | En Java es posible definir múltiples constructores con distintas firmas. En Python no existe esa capacidad, y recrearla mediante verificaciones de tipo produce código complejo y frágil. La solución idiomática consiste en utilizar parámetros con nombre o métodos de clase (`@classmethod`). |


---

## 2. Tabla de Equivalencias del Código Entregado

| Elemento en Java | Cómo quedó en tu código Python | ¿Traducción o rediseño? | Por qué |
|---|---|---|---|
| `public double getLongitud()` / `setLongitud(...)` | `@property` y `@longitud.setter` en `Lado` | Rediseño | Interfaz limpia de atributo (`lado.longitud = 5`) sin perder la validación `valor > 0` en el setter. |
| `public List<Lado> getLados()` | `def lados(self) -> tuple[Lado, ...]` en `Poligono` | Rediseño | Copia defensiva en salida; la tupla inmutable impide alteraciones externas (`.clear()`, `.pop()`). |
| `abstract class PoligonoRegular extends Poligono` | `def es_regular(self) -> bool` en `Poligono` | Rediseño | La regularidad es un estado geométrico dinámico de los lados, no un tipo jerárquico ontológico. |
| `public interface Exportable` | `@runtime_checkable class Exportable(Protocol)` | Rediseño | Subtipado estructural; permite tipar `PlanoCAD` externo sin tocarlo ni forzar herencia nominal. |
| Sobrecarga de constructores `Triangulo(...)` | `@classmethod regular(...)` y valores `None` | Rediseño | Sustituye la sobrecarga estática por constructores semánticos explícitos evitando `*args`. |
| `static List<Poligono> catalogo` | `Taller(poligonos=...)` y método `recibir()` | Rediseño | Agregación explícita de instancias desacopladas en lugar de estado global mutable en la clase. |
| Validación de tipos con `instanceof` | `lados_esperados()` y falla temprana al instanciar | Rediseño | Valida invariantes semánticas en runtime durante `__init__`, arrojando `TypeError` o `ValueError`. |

---

## 3. Las Tres Relaciones Estructurales (Parte 2)

La asignación `self._x = x` es sintácticamente idéntica, pero las relaciones se delatan por la gestión del ciclo de vida, la firma y las copias defensivas:
* **Asociación (`Lado — Etiqueta`, 0..1):** Se delata en `__init__(..., etiqueta: Etiqueta | None = None) -> None:`. El type hint de unión y el valor por defecto indican que el colaborador es opcional y externo; si el lado desaparece, la etiqueta no se ve afectada.
* **Agregación (`Taller — Poligono`, 0..*):** Se delata en `self._inventario: list[Poligono] = list(poligonos) if poligonos is not None else []` y `def recibir(self, p: Poligono)`. El taller agrupa figuras ya creadas en el exterior sin instanciarlas internamente ni condicionar su existencia.
* **Composición (`Poligono — Lado`, 3..*):** Se delata en el aislamiento defensivo `self._lados = list(lados)` en la entrada junto a `return tuple(self._lados)` en la salida, condicionado por `lados_esperados()`. El polígono se adueña de la colección; sin sus lados pierde entidad estructural.

---

## 4. Herencia y Decisión sobre `PoligonoRegular` (Parte 3)

Se descartó la herencia y se eliminó la clase `PoligonoRegular`. En Java se modelaba como subtipo por la necesidad del compilador de agrupar colecciones homogéneas (`List<PoligonoRegular>`). En el dominio real, la regularidad no es una esencia («es-un»), sino un estado geométrico contingente: un triángulo no muta de clase ontológica por tener lados iguales. Se rediseñó mediante:
1. Una consulta semántica de estado en la base: `def es_regular(self) -> bool`.
2. Constructores de clase alternativos en las subclases: `@classmethod regular(...)`.

---

## 5. Cierre: ABC vs. Protocol, ¿Lenguaje o Dominio? (Parte 4)

**La decide el dominio; el lenguaje solo provee la herramienta técnica.**
* **ABC (Subtipado nominal / «Es-un»):** Se usó para `Poligono` porque comparte identidad, ciclo de vida, atributos base (`nombre`, `color`) y una plantilla rígida de construcción (`lados_esperados()`).
* **Protocol (Subtipado estructural / «Sabe-hacer»):** Se usó para `Exportable` porque modela una capacidad transversal. Un `PlanoCAD` y un `Triangulo` no tienen ancestros comunes ni comparten estado, pero ambos exponen `exportar() -> str`. Una ABC hubiera exigido modificar código externo cerrado o recurrir a registros dinámicos invasivos.

---

## 6. Distinción entre Diseño y Sintaxis

* **Lo que cambió (sintaxis y modelo de ejecución):** La ilusión de privacidad estática se sustituyó por acuerdos de encapsulamiento (`@property`, copias defensivas explícitas). Las jerarquías rígidas creadas para complacer al compilador de Java (`PoligonoRegular`, sobrecargas) desaparecieron a favor de duck typing, constructores semánticos y protocolos estructurales.
* **Lo que se mantuvo idéntico (diseño conceptual de fondo):** Las invariantes de dominio fundamentales. Un polígono sigue requiriendo al menos 3 lados, la relación entre figuras y taller continúa siendo una agregación débil donde las figuras sobreviven al contenedor, y el polimorfismo garantiza que el cliente opere sobre contratos sin conocer la implementación concreta.