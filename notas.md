## Dia 1

### Aprendizaje
1. COMPREHENSION
Empezando por list comprehensions, la cual es una manera más eficiente y limpia de trabajar una lista bajo determinadas condiciones.
- List Comprehension:[QUÉ_QUIERO     PARA_CADA_ELEMENTO     CONDICIÓN]
ejm -> col_clean = [n.strip().lower().replace(" ", "_") for n in col_raws]
- Dict Comprehension:
ejm -> mapeo = {col.upper(): col.strip().lower().replace(" ", "_") for col in col_raws}
Generating key and value as a result of every iteration with arguments of this loop.
    Se puede usar to rename columns of a Dataframe
- SET comprehension
Unique values NOT ORDERED CANNOT ACCES TO AN ITEM
ejm -> channels = ["cha1", 12, "cha0", "cha1", 12, "cha1"]  # list
channels_clean = {c for c in channels}  # set
For access to an element of python set, you can convert it to a list: list()

2. GENERATORS
No produce todos los valores de golpe, lo hace uno a no, bajo demanda (lazy). Esto permite procesaR archivos enormes sin llenar la RAM.
Only saves instructions
Comprehension bajo paréntesis, guarda la lógica, lista para ser invocada manteniendo un orden interno.
lista1 = [x**2 for x in range(1_000_000)] VARIOS MB
gen = (x**2 for x in range(1_000_000)) POCOS CIENTOS DE BYTES
- Para llamar a producir los valores de un generador:
print(next(gen)) Llama a la primera iteración
print(next(gen)) Llama a la segunda iteración
...
- En funciones, se usa "yield" para limitar entre iteraciones o ejecuciones (pausa)
def generate_numbers():
    print("producing 1 ...")
    yield 1
    print("producing 2 ...")
    yield 2
print(next(gen)) : producing 1 ...      1
print(next(gen)) : producing 2 ...      2
- Para manejo de archivos:
with open(filepath, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")
-> readline() ya leyó la 1ra fila, con lo cual el puntero abstracto estaría en la segunda
-> Para reiniciar la posición usar f.seek(0), solo es para manejo de archivos
        for linea in f:
            valores = linea.strip().split(",")
-> Empieza desde la segunda fila (secuencialmente el consumo - a pedido)
            fila = dict(zip(header, valores))
            chunk.append(fila)
            if len(chunk) == chunk_size:
                yield chunk
-> retorna el chunk y congela la función allí mismo
                chunk = []
-> Se da al volver del congelamiento, resetea el chunk para el siguiente bloque

3. ITERATORS
Al "for item in algo", Python internamente:
numeros = [1, 2, 3]
-> Python convierte el for en:
iterador = iter(numeros)
while True:
    try:
        n = next(iterador)
        # print(n)
    except StopIteration:
        # print("Acabó la iteración")
        break

### Conceptos clave
- Manejo de archivos, iteradores, generadores:
    Se consumen progresivamente y mantienen posición interna (no carga todo en memoria)
    En Py, todo lo que se consume secuencialmente, mantiene estado interno.
- len() para diccionarios lee y cuenta claves únicas; para listas de diccionarios, cuenta la cantidad de diccionarios
- Manejo de errores:
    try: _SE INTENTA EJECUTAR_
    except ValueError: _ACCIÓN AL ENCONTRAR DATO MALO_
    finally: _ACCIÓN QUE SE EJECUTA SIEMPRE_
-> Si se llama a un generator que ya se agotó: El script fallará si no hay excepción StopIteration. Se debe manejar bajo except StopIteration:
- Manejo de archivos: readline() + for vs csv.reader() + next()
    with open(filepath, "r", encoding="utf-8") as f:
        a. 
        header = f.readline().strip().split(",")
        col_limpias = limpiar_columnas(header)
        return [dict(zip(col_limpias, fila.strip().split(","))) for fila in f]
        b.
        reader = csv.reader(f)
        col_limpias = limpiar_columnas(next(reader))
        return [dict(zip(col_limpias, fila)) for fila in reader]
-> readline() devuelve la primera linea en crudo, luego se debe parsear con el split()
-> csv.reader() interpreta el csv y separa por comas, maneja comillas, etc. Es un for linea in f pero con parsing incluido
-> Ambos consumen secuencialmente, como generators, mantienen posición interna
- Manejo de archivos: csv.DictReader() vs csv.reader() + dict(zip)
with open(filepath, "r", encoding="utf-8") as f:
        a.
        reader = csv.DictReader(f)
-> Class in python that reads CSV data each row into a one dictionary (several dicts)
-> Automatically uses the first row of the CSV file as keys for the resulting dictionaries
        for fila in reader:
            fila_limpia = {
                k.strip().lower().replace(" ", "_"): v.strip() for k, v in fila.items()
            }
        b.
        reader = csv.reader(f)
        headers = [col.strip().lower().replace(" ", "_") for col in next(reader)]
-> Para hacer las transformaciones se requiere acceder elemento por elemento de la lista
        for fila in reader:
            fila_limpia = dict(zip(headers, [col.strip() for col in fila]))

- Validación:
    dict1.get("nombre_producto") vs dict1["nombre_producto"]
-> Usa [] si estás 100% seguro de que la clave existe y quieres que el programa falle si falta
-> Usa .get() si la clave es opcional. Devuelve None o un valor que elijas, en vez de fallar.
assert lista == lista2, "Error: los valores son distintos"
-> assert sirve para capturar errores propios, del tipo que deben detener el código.
-> Aduana en el código, el programa se detiene y lanza un error. Para errores imposibles de permitir.
-> Ayuda a entender que se trata de una condición obligatoria

- Agrupar en main()
def main():
    datos = leer_csv_limpio(ruta1)
    print(f"Columnas limpias: {list(datos[0].keys())}")
    print(f"Total filas leidas: {len(datos)}")
    ventas_ok = list(generar_ventas_validas(ruta1))
    print(f"Ventas procesadas: {len(ventas_ok)}")
    comparar_memoria()
if __name__ == "__main__":
    main()
-> Sirve para ejecutar siempre y cuando se esté llamando directamente, no se ejecuta al importar desde otros proyectos
-> Organización para identificar donde empieza la ejecución principal del programa
-> Modularidad: Permite al archivo funcionar como script independiente y como una librería al mismo tiempo

### Complejidad
- Memorización de la estructura de los diferentes Comprehension y entender la importancia de su eficiencia para pasos de transformación.
- Entender la secuencialidad y manera de consumo de los Generators, el posicionamiento interno y su aplicación en funciones y manejos de archivos.
- Aplicar los métodos de manera correcta y entender equivalencias, además del yield para plantear limites, también comprender el valor de cada iteración en el código.
- Visualizar el proceso interno de los iterators para python, y cómo impacta en la memoria según su manera de trabajar.
