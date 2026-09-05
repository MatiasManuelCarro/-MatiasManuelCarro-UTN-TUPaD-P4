# TP 

# Matias Carro

# Parte 1 

## 1. Tabla de Diagnóstico de Java-ismos

| # | Java-ismo | Dónde (clase.método) | Inversión que lo explica | Síntoma observable |
|---|---|---|---|---|
| 1 | Getters preventivos sin lógica (`getNombre`, `getColor`) | `Figura.getNombre`, `Figura.getColor` | **Compilador → Acuerdo** (Encapsulamiento por convención) | En Java se hacen evitar que que el atributo cambie en el futuro. En Python los atributos son públicos directo (`figura.nombre`), porque si algún día hace falta validarlos, se agrega `@property` sin romper el código que ya los usaba. |
| 2 | Getter y Setter tradicionales estilo Java Bean | `Lado.getLongitud`, `Lado.setLongitud` | **Compilador → Acuerdo** (`@property` para lógica real) | Obliga a usar métodos largos como `lado.getLongitud()` o `lado.setLongitud(5)`. En Python se usa `@property` para que parezca una variable común (`lado.longitud = 5`), pero validando por detrás que no sea negativo. |
| 3 | Variable mutable de clase usada como `static` global compartido | `Poligono.catalogo = []` | **Declaración → Runtime** (Objetos de clase compartidos) | Esa lista pertenece a la clase y no a cada objeto. Si una clase hija o cualquier parte del código la vacía o la toca, le modifica el catálogo a todos los polígonos del sistema al mismo tiempo. |
| 4 | Argumentos por defecto mutables (`lados=[]`, `observaciones=[]`) | `Poligono.__init__` | **Declaración → Runtime** (Valores por defecto evaluados al inicio) | La lista vacía se crea una sola vez cuando Python lee el archivo. Si creás dos polígonos sin pasarles observaciones, ambos comparten la misma lista en memoria (`p1._observaciones is p2._observaciones` da `True`). |
| 5 | Omitir `super().__init__()` y asignar los atributos a mano | `Poligono.__init__` | **Compilador → Acuerdo** (Cadena de herencia) | El constructor del padre (`Figura`) nunca se ejecuta. Como resultado, la marca de control `_construida = True` jamás se crea en el objeto, dejándolo a medio armar. |
| 6 | Guardar y devolver la lista interna sin copiar (falta de copia defensiva) | `Poligono.__init__` y `Poligono.getLados` | **Compilador → Acuerdo** (Protección del estado interno) | Cualquiera desde afuera puede agarrar la lista y hacer `.clear()` o borrarle elementos, arruinando los datos internos del polígono sin que este se entere ni pueda impedirlo. |
| 7 | Bucle `for` con acumulador manual en lugar de usar herramientas nativas | `Poligono.perimetro` | **Compilador → Acuerdo** (Aprovechar el lenguaje) | Escribir cuatro líneas de código imperativo (`total = 0`, `for`, `total = total + ...`) para algo que en Python se resuelve directo y más legible en una sola línea usando `sum(...)`. |
| 8 | Simular sobrecarga de constructores con `*args` e `isinstance` | `Triangulo.__init__` y `Cuadrado.__init__` | **Herencia → Duck typing** (Constructores alternativos) | En Java se crean varios constructores con distintos parámetros. En Python no existe eso: simularlo con ramas de `if isinstance(...)` deja un código enredado y frágil. Se resuelve con valores por defecto o métodos de clase (`@classmethod`). |

---

## 2. Corrección y Justificación de los 8 Java-ismos



### 1. Quitar getters vacíos (`getNombre`, `getColor`)
* **Dónde estaba:** `Figura.getNombre()` y `Figura.getColor()`.
* **Cómo se corrigió:** Se borraron esos métodos y se usan directamente los atributos: `figura.nombre` y `figura.color`.
* **Porque se corrigió:** En Java se crean métodos "por las dudas" porque si más adelante querés validar un atributo, cambiar de variable a método te rompe todo el código que ya lo usaba. En Python hay un acuerdo: los atributos nacen públicos y directos. Si el día de mañana necesitás agregar una validación, le ponés `@property` y el código cliente sigue usando `figura.nombre` exactamente igual, sin romperse.



### 2. Cambiar getter/setter tradicional por `@property`
* **Dónde estaba:** `Lado.getLongitud()` y `Lado.setLongitud(valor)`.
* **Cómo se corrigió:** Se cambiaron por `@property def longitud(self)` y `@longitud.setter`, validando que el valor sea mayor a 0.
* **Porque se corrigió:** Java te obliga a usar métodos largos (`getLongitud()`) para proteger los datos. En Python, la `@property` se usa únicamente cuando hay una regla de negocio real que controlar (en este caso, que la longitud no sea negativa). Esto te da lo mejor de los dos mundos: validación estricta por dentro y acceso simple (`lado.longitud = 5`) por fuera.



### 3. Eliminar lista compartida en la clase (`catalogo = []`)
* **Dónde estaba:** `Poligono.catalogo = []`.
* **Cómo se corrigió:** Se sacó la lista de adentro de la clase `Poligono` y se quitó el autorregistro en el constructor.
* **Porque se corrigió:** En Java un `static` lo maneja el compilador con alcance global. En Python, lo que ponés suelto adentro de una clase se crea en memoria apenas arranca el programa y lo comparten todas las instancias. Si cualquier objeto tocaba esa lista, modificaba el catálogo de todos los demás sin que nadie se entere.



### 4. Reemplazar argumentos por defecto mutables (`lados=[]`)
* **Dónde estaba:** `Poligono.__init__(..., lados=[], observaciones=[])`.
* **Cómo se corrigió:** Se cambiaron por `= None`, y adentro del constructor se crea una lista nueva si vino vacío (`list(lados) if lados is not None else []`).
* **Porque se corrigió:** En Python los valores por defecto se crean una sola vez cuando el intérprete lee el archivo, no cada vez que llamás a la función. Si usás `[]`, todos los objetos que no pasen ese dato terminan apuntando a la misma lista física en memoria. Usar `None` evita esa trampa porque `None` no se puede modificar.



### 5. Llamar a `super().__init__()` en vez de copiar asignaciones a mano
* **Dónde estaba:** `Poligono.__init__`.
* **Cómo se corrigió:** Se agregó `super().__init__(nombre, color)` al inicio del constructor.
* **Porque se corrigió:** Java te obliga o te ayuda a llamar al padre al heredar. En Python es un acuerdo que tenés que escribir vos. Al omitirlo, el constructor de `Figura` nunca se ejecutaba y la marca de control `_construida = True` jamás se creaba, dejando al objeto incompleto.



### 6. Usar copia defensiva en la lista de lados
* **Dónde estaba:** `Poligono.__init__` (`self._lados = lados`) y `Poligono.getLados()` (`return self._lados`).
* **Cómo se corrigió:** El constructor clona la lista que recibe (`list(lados)`) y el método para consultarla devuelve una tupla inmutable (`tuple(self._lados)`).
* **Porque se corrigió:** Como en Python no existe la privacidad absoluta por compilador, si entregás la lista original, cualquiera desde afuera le puede hacer `.clear()` o borrar elementos y romperte el polígono. Devolver una copia o una tupla protege los datos internos de modificaciones externas no deseadas.



### 7. Reemplazar el bucle acumulador manual por `sum()`
* **Dónde estaba:** `Poligono.perimetro()`.
* **Cómo se corrigió:** Se cambió el `for` con la variable `total = total + l` por la función directa `sum(l.longitud for l in self._lados)`.
* **Porque se corrigió:** En lenguajes como Java clásico se programaba paso a paso con acumuladores temporales. En Python existe el acuerdo de aprovechar las herramientas nativas del lenguaje: `sum()` sobre un generador expresa la misma idea de sumar en una sola línea, más clara y eficiente.



### 8. Eliminar sobrecarga falsa con `*args` e `isinstance`
* **Dónde estaba:** `Triangulo.__init__(*args)` y `Cuadrado.__init__(*args)`.
* **Cómo se corrigió:** Se armó un constructor normal con argumentos opcionales con nombre y se sumó un método de clase (`@classmethod def desde_lados`) para la construcción alternativa.
* **Porque se corrigió:** En Java podés escribir varios constructores con distintos tipos de parámetros y el compilador elige cuál usar. En Python eso no existe: querer emularlo preguntando si es una lista o cuántos argumentos llegaron hace que el código sea ilegible y frágil. En Python se resuelve usando nombres claros en los parámetros o constructores alternativos semánticos.

### demo_sintomas.py 

```python
class PoligonoOriginal:
    # Simula el constructor original con defaults mutables y asignación directa sin copia
    #El linter informa: Do not use mutable data structures for argument 
    def __init__(self, lados=[], observaciones=[]):
        self._lados = lados  # Aliasing: guarda la referencia directa
        self._observaciones = observaciones  # Default mutable


def demostrar_sintoma_1_default_mutable():
    print("--- SÍNTOMA 1: Argumento por defecto mutable (observaciones=[]) ---")

    # Creamos dos instancias usando el valor por defecto
    p1 = PoligonoOriginal()
    p2 = PoligonoOriginal()

    # Agregamos una observación únicamente al primer polígono
    p1._observaciones.append("Revisar vértice A")

    # Verificación de identidad en memoria
    mismo_objeto = p1._observaciones is p2._observaciones

    print(f"¿p1._observaciones es el mismo objeto que p2._observaciones?: {mismo_objeto}")
    print(f"Observaciones de p1: {p1._observaciones}")
    print(f"Observaciones de p2 (sin haberle agregado nada): {p2._observaciones}")

    print(
        "Fallo observable: p2 quedó contaminado con los datos de p1 "
        "porque ambos comparten la misma lista creada en tiempo de definición."
    )

    def demostrar_sintoma_2_aliasing_sin_copia_defensiva():
    print("\n--- SÍNTOMA 2: Violación de encapsulamiento por falta de copia defensiva ---")

    lista_externa = ["LadoA", "LadoB", "LadoC"]

    # Instanciamos el polígono pasándole la lista externa
    p = PoligonoOriginal(lados=lista_externa)

    print(f"Lados internos de p al iniciar: {p._lados}")

    # Un actor externo modifica su propia lista después de haber creado el objeto
    lista_externa.clear()

    print(f"Lados internos de p tras vaciar la lista externa: {p._lados}")

    print(
        "Fallo observable: el estado interno de p fue corrompido desde afuera sin pasar "
        "por ningún método del polígono, porque se guardó el alias en vez de una copia."
    )


if __name__ == "__main__":
    demostrar_sintoma_1_default_mutable()
    demostrar_sintoma_2_aliasing_sin_copia_defensiva()

```

Salida en consola:

```
--- SÍNTOMA 1: Argumento por defecto mutable (observaciones=[]) ---
¿p1._observaciones es el mismo objeto que p2._observaciones?: True
Observaciones de p1: ['Revisar vértice A']
Observaciones de p2 (sin haberle agregado nada): ['Revisar vértice A']
Fallo observable: p2 quedó contaminado con los datos de p1 porque ambos comparten la misma lista creada en tiempo de definición.

--- SÍNTOMA 2: Violación de encapsulamiento por falta de copia defensiva ---
Lados internos de p al iniciar: ['LadoA', 'LadoB', 'LadoC']
Lados internos de p tras vaciar la lista externa: []
Fallo observable: el estado interno de p fue corrompido desde afuera sin pasar por ningún método del polígono, porque se guardó el alias en vez de una copia.

```

***Explicación Conceptual: ¿Por qué pasa y cómo funciona?***

#### 1. Síntoma de Argumento por Defecto Mutable

* **Por qué ocurre:**
  En Java, los valores por defecto no existen en la firma; se resuelven mediante sobrecarga en tiempo de compilación. En Python, las expresiones en los argumentos por defecto se evalúan **una única vez cuando el módulo se lee e interpreta** (tiempo de carga/definición), y no cada vez que se instancia la clase.
* **Cómo funciona el fallo en memoria:**
  Al escribir `def __init__(self, observaciones=[])`, Python reserva un único objeto de tipo lista en la memoria RAM vinculado a la firma del método. Cada vez que se ejecuta `PoligonoOriginal()` sin parámetros, el puntero `self._observaciones` de la nueva instancia apunta a esa misma dirección de memoria. Cuando `p1` agrega un elemento a su lista, está mutando la estructura compartida, por lo que `p2` ve la modificación de forma inmediata y automática (`p1._observaciones is p2._observaciones` evalúa a `True`).
* **Cómo se soluciona idiomáticamente:**
  Se utiliza un valor inmutable como centinela en la firma (`observaciones: list[str] | None = None`). Dentro del cuerpo del constructor se comprueba: si el valor recibido es `None`, se instancia una lista nueva e independiente `[]` para ese objeto específico.

#### 2. Síntoma de Aliasing por Falta de Copia Defensiva

* **Por qué ocurre :**
  En Python no existen modificadores de acceso por hardware o compilador como `private`. Toda asignación de variables sobre objetos mutables (como listas o diccionarios) copia únicamente la referencia en memoria, no el contenido del contenedor.
* **Cómo funciona el fallo en memoria:**
  Al hacer `self._lados = lados`, el atributo interno `_lados` y la variable externa `lista_externa` quedan vinculados al mismo bloque de memoria. El objeto polígono pierde el control exclusivo sobre sus propios componentes. Si el código cliente que creó la lista decide vaciarla con `lista_externa.clear()`, el polígono se queda sin lados sin haber ejecutado ningún método propio, rompiendo la invariante estructural de la figura.
* **Cómo se soluciona idiomáticamente:**
  Aplicando **copia defensiva en la entrada y en la salida**:
  * En la entrada (constructor), se clona la colección entrante creando una lista nueva: `self._lados = list(lados) if lados is not None else []`.
  * En la salida (método o propiedad de lectura), se expone una tupla inmutable: `tuple(self._lados)`. De este modo, cualquier operación de mutación externa sobre la tupla es rechazada directamente por el lenguaje.

  ## 4. Demostración y Justificación de @property (`demo_property.py`)

En el diseño original existían métodos de acceso y mutación tradicionales estilo Java Bean (`getLongitud` y `setLongitud`) dentro de la clase `Lado`. De todos los getters y setters del diagnóstico, este es el único caso donde correspondía aplicar `@property` porque existe una regla de negocio real: **la longitud de un lado debe ser un número estrictamente positivo**.

A través del script `demo_property.py` se contrasta el enfoque tradicional contra la solución idiomática, evidenciando por qué `@property` resuelve la tensión entre encapsulamiento y legibilidad.

---

### Explicación del problema con el enfoque Java Bean (`LadoJavaismo`)

El enfoque tradicional acarrea dos problemas concretos:

1. **Ceremonia innecesaria en el cliente:**  
   Obliga a invocar métodos explícitos con paréntesis (`lado.getLongitud()` y `lado.setLongitud(valor)`). Esto hace que operaciones cotidianas (como sumar lados o calcular perímetros) queden sobrecargadas de llamadas a funciones, restando claridad matemática y semántica al código.

2. **Falsa sensación de seguridad:**  
   En Python no existe la privacidad por compilador. El prefijo `_longitud` es un acuerdo de no tocar, no un candado físico. Si el cliente o un desarrollador distraído asigna directamente al atributo interno (`lado._longitud = -999.0`), se saltea por completo el método de validación sin que el sistema emita ninguna advertencia, corrompiendo el estado interno.

---

### Por qué `@property` es la solución correcta (`LadoPythonico`)

La combinación de `@property` con `@longitud.setter` ofrece tres ventajas estructurales:

1. **Interfaz limpia y natural:**  
   El código cliente interactúa con `lado.longitud` como si fuera una variable común, tanto para leer (`print(lado.longitud)`) como para escribir (`lado.longitud = 25.5`) o calcular (`lado.longitud * 4`).

2. **Validación automática e invisible:**  
   Cualquier intento de asignación pasa de manera obligatoria por el decorador setter. Si se intenta fijar un valor menor o igual a cero (`lado.longitud = -10.0`), se dispara inmediatamente una excepción `ValueError`, preservando el estado válido del objeto.

3. **Garantía desde el nacimiento:**  
   Al escribir `self.longitud = longitud` dentro de `__init__`, la validación se dispara desde el momento mismo de la instanciación. No es posible crear un lado inválido de entrada.

---

### Codigo y demostracion en la salida de la consola:

```python
"""demo_property.py — Demostración de transición a @property.

Prueba que el código cliente no cambia su sintaxis al incorporar validación
mediante @property, a diferencia de los getters/setters estilo Java.
"""

# =====================================================================
# 1. ENFOQUE ANTES: Estilo Java Bean 
# =====================================================================


class LadoJavaismo:

    def __init__(self, longitud: float):
        self._longitud = longitud

    def getLongitud(self) -> float:
        return self._longitud

    def setLongitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser estrictamente positiva.")
        self._longitud = valor


# =====================================================================
# 2. ENFOQUE DESPUÉS: Idiomático con @property 
# =====================================================================


class LadoPythonico:

    def __init__(self, longitud: float):
        # Al asignar self.longitud pasa por el setter y valida desde el nacimiento
        self.longitud = longitud

    @property
    def longitud(self) -> float:
        return self._longitud

    @longitud.setter
    def longitud(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("La longitud debe ser estrictamente positiva.")
        self._longitud = valor


# =====================================================================
# 3. DEMOSTRACIÓN: Comparación del impacto en el Código Cliente
# =====================================================================


def probar_enfoque_java():
    print("--- Enfoque Antes (Estilo Java) ---\n")
    lado_java = LadoJavaismo(10.0)

    # El cliente está obligado a invocar métodos con paréntesis
    print(f"Lectura con getLongitud(): {lado_java.getLongitud()}")
    lado_java.setLongitud(25.5)
    print(f"Lectura tras setLongitud(25.5): {lado_java.getLongitud()}")

    # Además, el atributo interno queda expuesto si se accede por error
    lado_java._longitud = -999.0
    print(
        f"Demostracion: Se ignoro el setter asignando al atributo privado: {lado_java._longitud}\n"
    )


def probar_enfoque_python():
    print("\n--- Enfoque Python (@property) ---\n")

    # Supongamos que el cliente consumía atributos públicos normales:
    # lado = Lado(10.0)
    # total = lado.longitud + 5.0
    # lado.longitud = 25.5

    # Al migrar a @property, las líneas del cliente son exactamente las mismas:
    lado = LadoPythonico(10.0)

    # 1. Lectura directa (sintaxis de atributo sin paréntesis)
    print(f"Lectura directa (lado.longitud): {lado.longitud}")

    # 2. Asignación directa (sintaxis de atributo)
    lado.longitud = 25.5
    print(f"Lectura tras reasignación (lado.longitud = 25.5): {lado.longitud}")

    # 3. Operaciones matemáticas limpias
    perimetro_estimado = lado.longitud * 4
    print(f"Cálculo directo (lado.longitud * 4): {perimetro_estimado}")

    # 4. Verificación de la invariante: frena valores inválidos transparentemente
    print("Intentando asignar valor negativo (lado.longitud = -10.0)...")
    try:
        lado.longitud = -10.0
    except ValueError as error:
        print(f"Excepción capturada con éxito: {error}")

    print(
        f"El valor se mantuvo protegido en su último estado válido: {lado.longitud}"
    )


if __name__ == "__main__":
    probar_enfoque_java()
    probar_enfoque_python()

```


Salida en consola:

```
--- Enfoque Antes (Estilo Java) ---

Lectura con getLongitud(): 10.0
Lectura tras setLongitud(25.5): 25.5
Demostracion: Se ignoro el setter asignando al atributo privado: -999.0


--- Enfoque Python (@property) ---

Lectura directa (lado.longitud): 10.0
Lectura tras reasignación (lado.longitud = 25.5): 25.5
Cálculo directo (lado.longitud * 4): 102.0
Intentando asignar valor negativo (lado.longitud = -10.0)...
Excepción capturada con éxito: La longitud debe ser estrictamente positiva.
El valor se mantuvo protegido en su último estado válido: 25.5
```
---

# Parte 2 - elaciones estructurales 

## Relaciones Estructurales y Diferenciación en el Código

En Python, la sintaxis para almacenar un atributo siempre es la misma (`self._algo = algo`). Por ende, la distinción entre **Asociación**, **Agregación** y **Composición** no está en la asignación, sino en:

1. **La dependencia de existencia y ciclo de vida** entre las partes.
2. **Quién es responsable de instanciar el objeto.**
3. **El grado de acoplamiento e independencia que expone la firma de la interfaz.**

A continuación se analiza cada relación señalando la **línea exacta que la delata**:


### 1. Lado — Etiqueta: Asociación (0..1)

* **Concepto:** Relación débil y opcional entre dos entidades independientes. Un `Lado` puede existir con o sin una `Etiqueta`, y la etiqueta no determina la existencia del lado.
* **Líneas exactas que lo delatan:**  
  En la cabecera del constructor:
  ```python
  def __init__(self, longitud: float, etiqueta: Etiqueta | None = None) -> None:
  ```
  y en su asignación:
  ```python
  self.etiqueta: Etiqueta | None = etiqueta
  ```
* **Por qué lo delata:** El uso del type hint de unión `Etiqueta | None` junto con el valor por defecto `= None`. Revela explícitamente la multiplicidad `0..1`: el objeto colaborador es prescindible para la construcción y vida de la instancia receptora.


### 2. Taller — Poligono: Agregación (0..*)

* **Concepto:** Relación todo/parte débil. El `Taller` contiene polígonos que no fueron fabricados por él, sino que le fueron provistos ya creados desde un ámbito externo. Si el `Taller` es destruido o eliminado de memoria, los polígonos continúan existiendo de manera autónoma.
* **Líneas exactas que lo delatan:**  
  En la firma y asignación del constructor:
  ```python
  self._inventario: list[Poligono] = list(poligonos) if poligonos is not None else []
  ```
  y en el método de incorporación:
  ```python
  def recibir(self, poligono: Poligono) -> None:
      self._inventario.append(poligono)
  ```
* **Por qué lo delata:** En ningún punto dentro de `Taller` se ejecuta `Poligono(...)`. La clase se limita a recibir instancias vivas inyectadas por parámetro y agruparlas en su colección interna. El ciclo de vida de los polígonos es completamente ajeno al del taller.


### 3. Poligono — Lado: Composición (3..*)

* **Concepto:** Relación todo/parte fuerte y existencia condicionada por contrato. Un `Poligono` no puede definirse geométricamente sin sus lados; estos constituyen su estructura física esencial.
* **Líneas exactas que lo delatan:**  
  En el constructor con la copia defensiva obligatoria:
  ```python
  self._lados = list(lados) if lados is not None else []
  ```
  combinado con el método abstracto:
  ```python
  @abstractmethod
  def lados_esperados(self) -> int:
  ```
  y la exposición blindada en la salida:
  ```python
  def lados(self) -> tuple[Lado, ...]:
      return tuple(self._lados)
  ```
* **Por qué lo delata:** Aunque los lados puedan suministrarse externamente en la construcción, el `Poligono` se apropia de la estructura:
  * **Aislamiento defensivo:** Al hacer `list(lados)` en la entrada y `tuple(self._lados)` en la salida, el polígono se independiza del exterior y se convierte en el único custodio de la colección.
  * **Invariante de dominio:** A través de `lados_esperados()`, cada subclase (`Triangulo` con 3, `Cuadrado` con 4) impone que el objeto no es semánticamente válido sin esa cantidad exacta de componentes. Si el polígono deja de existir, sus lados pierden propósito estructural en el sistema.


### Resumen Comparativo de Ciclo de Vida

| Relación | Tipo | ¿Quién instancia el objeto? | Ciclo de vida / Dependencia |
| :--- | :--- | :--- | :--- |
| **Lado — Etiqueta** | Asociación (`0..1`) | Ámbito externo. | Totalmente desacoplados (`Etiqueta \| None = None`). |
| **Taller — Poligono** | Agregación (`0..*`) | Ámbito externo. | Débil: entran por `recibir()` o `__init__`; si muere el Taller, los Polígonos sobreviven. |
| **Poligono — Lado** | Composición (`3..*`) | Gestionado por el Polígono. | Fuerte: el Polígono encapsula y aísla sus partes con copias defensivas y valida su cantidad. |

