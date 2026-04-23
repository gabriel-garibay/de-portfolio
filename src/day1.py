import pandas as pd
import sys
import csv
from pathlib import Path

"""---------------------- List Comprehensions ----------------------"""
# List Comprehensions
# Loop traditional
numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # lista
pares = []  # lista vacía

for n in numeros:
    if n % 2 == 0:
        pares.append(n)
# print(pares)

# Equivalent with List comprehension
"""[QUÉ_QUIERO     PARA_CADA_ELEMENTO     CONDICIÓN]
    """
pares_lc = [n - 1 for n in numeros if n % 2 == 0]
# print(pares_lc)

# Ejemplo práctico para PIPELINE
col_raws = [" Nombre Cliente ", "MONTO_VENTA", "fECHA pedido ", "id"]
col_clean = [n.strip().lower().replace(" ", "_") for n in col_raws]

# print(col_clean)

# DICT comprehension: mapeo col_raws a clean
"""Generating key and value as a result of every iteration with arguments of this loop"""
mapeo = {col.upper(): col.strip().lower().replace(" ", "_") for col in col_raws}
# print(mapeo)

# Uso con Pandas - Using a dictionary to rename columns of a Dataframe
df = pd.DataFrame(columns=col_raws)
# print(df)
df = df.rename(columns=mapeo)
# print(df)

# SET comprehension - unique values NOT ORDERED CANNOT ACCES TO AN ITEM
channels = ["cha1", 12, "cha0", "cha1", 12, "cha1"]  # list
channels_clean = {c for c in channels}  # set
# print(channels_clean)
# For access to an element of python set, you can convert it to a list: list()


"""---------------------- Generators ----------------------"""
# No produce todos los valores de golpe, lo hace uno a no, bajo demanda (lazy)
# Esto permite procesa archivos enormes sin llenar la RAM

# List comprehension: create everything in memory at the time - right now
lista1 = [x**2 for x in range(1_000_000)]
# print(sys.getsizeof(lista1))

# GENERATOR EXPRESSION: only saves instructions
# Comprehension bajo paréntesis, guarda la lógica, lista para ser invocada manteniendo un orden interno

gen = (x**2 for x in range(1_000_000))
# print(sys.getsizeof(gen))
# Produce los valores cuando lo pides
""" print(next(gen))
print(next(gen))
print(next(gen))
 """

# Al usar con funciones se usa yield para retornar y pausar
""" def generate_numbers():
    print("producing 1 ...")
    yield 1
    print("producing 2 ...")
    yield 2
    print("producing 3 ...")
    yield 3
 """

""" gen = generate_numbers()
print(gen)
print(next(gen))
print(next(gen)) """
# La función está pausada entre yields

# GENERATOR para leer archivos grandes:


def leer_csv_en_chunks(filepath, chunk_size=1000):
    # Lee un csv en bloques de chunk_size filas. No carga el archivo completo en RAM
    with open(filepath, "r", encoding="utf-8") as f:
        header = f.readline().strip().split(",")
        # Manejo de archivos, iteradores, generadores:
        # Se consumen progresivamente y mantienen posición interna (no carga todo en memoria)
        # En Py, todo lo que se consume secuencialmente, mantiene estado interno
        chunk = []
        # print(header)
        # readline() ya leyó la 1ra fila, con lo cual el puntero abstracto estaría en la segunda
        # Para reiniciar la posición usar f.seek(0)
        # .seek() solo es para manejo de archivos
        for linea in f:
            valores = linea.strip().split(",")
            # zip(): Combina dos listas en paralelo
            # Los empareja elemento por elemento, como un cierre de cremallera
            fila = dict(zip(header, valores))
            chunk.append(fila)

            if len(chunk) == chunk_size:
                yield chunk  # retorna el chunk y pausa la función allí
                chunk = []  # resetea el chunk para el siguiente bloque

        if chunk:  # Verifica que no está vacío el chunk al terminar el loop
            yield chunk  # devuele la parte faltante


# Procesamiento de archivos sin problema de RAM
cont_filas = 0
# La función se llama en loop para retornar los chunks indicados por los yield
for bloque in leer_csv_en_chunks(
    "D:/AE/de-portfolio/data/raw/olist_orders_dataset.csv", 500
):
    # print(f"Procesando {len(bloque)} filas ...")
    cont_filas += len(bloque)

# print(cont_filas)

# Al usar "continue" dentro de un loop esto le indica al bucle pasar a la siguiente iteración
# El yield retorna la variable nombrada o la variable de forma explícita:
# yield {"id":partes[0],"producto":partes[1].strip(),"monto":monto}
# Manejo de errores
""" try: _SE INTENTA EJECUTAR_
    except ValueError: _ACCIÓN AL ENCONTRAR DATO MALO_
    finally: _ACCIÓN QUE SE EJECUTA SIEMPRE_"""


"""---------------------- Iterators ----------------------"""
# Al "for item in algo", Python internamente:
numeros = [1, 2, 3]
# Python convierte el for en:
iterador = iter(numeros)
while True:
    try:
        n = next(iterador)
        # print(n)
    except StopIteration:
        # print("Acabó la iteración")
        break

    # Una clase iterable: Se verá en EXTRACTORS
# class RangoPersonalizado:
#     def __init__(self, inicio, fin, paso=1):
#         self.inicio = inicio
#         self.fin = fin
#         self.paso = paso

#     def __iter__(self):
#         actual = self.inicio
#         while actual < self.fin:
#             yield actual
#             actual += self.paso

# for n in RangoPersonalizado(0, 10, 2):
#     print(n)  # 0, 2, 4, 6, 8


"""---------------------- Ejercicios prácticos ----------------------"""
# EJERCICIO 1


def limpiar_columnas(columnas: list) -> list:
    return [col.strip().lower().replace(" ", "_") for col in columnas]


def leer_csv_limpio(filepath: str) -> list:
    # Lee un csv y retorna lista de dicts con columnas limpias (por separado)
    with open(filepath, "r", encoding="utf-8") as f:
        # header = f.readline().strip().split(",")
        # col_limpias = limpiar_columnas(header)
        # return [dict(zip(col_limpias, fila.strip().split(","))) for fila in f]
        reader = csv.reader(f)
        col_limpias = limpiar_columnas(next(reader))
        return [dict(zip(col_limpias, fila)) for fila in reader]
    # readline() devuelve la primera linea en crudo, luego se debe parsear con el split()
    # csv.reader() interpreta el csv y separa por comas, maneja comillas, etc. Es un for linea in f pero con parsing incluido
    #   Ambos consumen secuencialmente, como generators, mantienen posición interna


# prueba
base = Path(__file__).parent.parent
ruta1 = str(base / "data/raw/ventas_prueba.csv")
datos = leer_csv_limpio(ruta1)

# print(list(datos[0].keys()))
# for fila in datos:
#    print(fila)


# EJERCICIO 2
def generar_ventas_validas(filepath: str):
    """
    Generator que produce solo filas donde:
    - nombre_producto no está vacío
    - monto_total es un número positivo
    Imprime un resumen al final.
    """
    descartadas = 0
    producidas = 0
    # cont_filas = 1
    # filas_validas = []

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(
            f
        )  # Class in python that reads CSV data each row into a one dictionary (several dicts)
        # Automatically uses the first row of the CSV file as keys for the resulting dictionaries
        for fila in reader:
            fila_limpia = {
                k.strip().lower().replace(" ", "_"): v.strip() for k, v in fila.items()
            }
            # Validación 1: producto no vacío
            if not fila_limpia.get("nombre_producto"):
                # Usa [] si estás 100% seguro de que la clave existe y quieres que el programa falle si falta
                # Usa .get() si la clave es opcional. Devuelve None o un valor que elijas, en vez de fallar.
                print(f" DESCARTADA (sin producto):{fila_limpia}")
                descartadas += 1
                continue
            # Validación 2: Monto válido y positivo
            try:
                monto = float(fila_limpia["monto_total"])
                if monto <= 0:
                    print(f" DESCARTADA (monto negativo):{fila_limpia}")
                    descartadas += 1
                    continue
            except ValueError:
                print(f" DESCARTADA (monto no numérico):{fila_limpia}")
                descartadas += 1
                continue

            producidas += 1
            yield fila_limpia

    print(f"\nResumen: {producidas} válidas, {descartadas} descartadas.")


"""reader = csv.reader(f)
        headers = next(reader)
        for fila in reader:
            if fila[1] == "":
                print(f"Fila {cont_filas}: DESCARTADA (sin producto)")
                cont_filas += 1
                descartadas += 1
                continue
            if float(fila[2]) <= 0:
                print(f"Fila {cont_filas}: DESCARTADA (monto negativo)")
                cont_filas += 1
                descartadas += 1
                continue
            filas_validas.append(cont_filas)
            cont_filas += 1
            producidas += 1
    print(f"Filas {str(filas_validas)} producidas") """


def generar_ventas_validas2(filepath: str):

    descartadas = 0
    producidas = 0

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = [col.strip().lower().replace(" ", "_") for col in next(reader)]
        # Para hacer las transformaciones se requiere acceder elemento por elemento de la lista
        # List Comprehension: Alterar una lista bajo determinadas condiciones
        for fila in reader:
            fila_limpia = dict(zip(headers, [col.strip() for col in fila]))
            # Validación 1: producto no vacío
            if not fila_limpia.get("nombre_producto"):
                print(f" DESCARTADA (sin producto):{fila_limpia}")
                descartadas += 1
                continue
            # Validación 2: Monto válido y positivo
            try:
                monto = float(fila_limpia["monto_total"])
                if monto <= 0:
                    print(f" DESCARTADA (monto negativo):{fila_limpia}")
                    descartadas += 1
                    continue
            except ValueError:
                print(f" DESCARTADA (monto no numérico):{fila_limpia}")
                descartadas += 1
                continue

            producidas += 1
            yield fila_limpia

    print(f"\nResumen: {producidas} válidas, {descartadas} descartadas.")


# prueba
base = Path(__file__).parent.parent
ruta1 = str(base / "data/raw/ventas_prueba.csv")
# datos = generar_ventas_validas(ruta1)
# for venta in generar_ventas_validas2(ruta1):
#    print(f" OK: {venta}")


# EJERCICIO 3
def comparar_memoria():
    N = 1_000_000

    lista = [x**2 for x in range(N)]  # Lista
    gen = (x**2 for x in range(N))  # Instrucción a ejecutarse

    tam_lista = sys.getsizeof(lista)
    tam_gen = sys.getsizeof(gen)

    print(f"\n=== Comparación de memoria (N={N:,}) ===")
    print(
        f"List comprehension : {tam_lista:>12,} bytes ({tam_lista / 1024 / 1024:.1f} MB)"
    )
    print(f"List comprehension : {tam_gen:>12,} bytes ({tam_gen / 1024 / 1024:.1f} MB)")
    print(f"El generator usa {tam_lista // tam_gen}x menos memoria")
    # Verificar valores
    lista2 = list(
        gen
    )  # List es un "Consumidor total", Python ejecuta un for internamente hasta que se agotan los valores (StopIteration)
    # next(): es un consumidor puntual
    assert lista == lista2, "Error: los valores son distintos"
    # assert sirve para capturar errores propios, del tipo que deben detener el código.
    # Aduana en el código, el programa se detiene y lanza un error. Para errores imposibles de permitir.
    # Ayuda a entender que se trata de una condición obligatoria
    print("Verificación: ambos producen los mismos resultados.")


# comparar_memoria()

# EJERCICIO 4

"""Agrupar en main()"""


def main():
    print("=" * 60)
    print("DIA 1 — Comprehensions, Generators e Iteradores")
    print("=" * 60)
    base = Path(__file__).parent.parent
    ruta1 = str(base / "data/raw/ventas_prueba.csv")
    print("\n--- Ejercicio 1: limpiar columnas ---")
    datos = leer_csv_limpio(ruta1)
    print(f"Columnas limpias: {list(datos[0].keys())}")
    print(f"Total filas leidas: {len(datos)}")

    print("\n--- Ejercicio 2: generator con validacion ---")
    ventas_ok = list(generar_ventas_validas(ruta1))
    print(f"Ventas procesadas: {len(ventas_ok)}")

    print("\n--- Ejercicio 3: comparacion de memoria ---")
    comparar_memoria()

    print("\nDia 1 completado.")


# Sirve para ejecutar siempre y cuando se esté llamando directamente, no se ejecuta al importar desde otros proyectos
# Organización para identificar donde empieza la ejecución principal del programa
# Modularidad: Permite al archivo funcionar como script independiente y como una librería al mismo tiempo
if __name__ == "__main__":
    main()

"Cambio para primer commit"
