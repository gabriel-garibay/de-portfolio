import csv
from pathlib import Path


base = Path(__file__).parent.parent
raw = base / "data" / "raw"
raw.mkdir(parents=True, exist_ok=True)

datos = [
    ["ID Pedido", "Nombre Producto", "Monto Total", "Fecha Pedido", "Canal"],
    ["1", "Laptop HP", "2500.00", "2024-01-15", "D2C"],
    ["2", "", "150.50", "2024-01-16", "RETAIL"],
    ["3", "Mouse Logitech", "-50", "2024-01-16", "OWN"],
    ["4", "Teclado Mecanico", "320.00", "fecha_invalida", "D2C"],
    ["5", "Monitor 4K", "1800.00", "2024-01-17", "RETAIL"],
    ["6", "Webcam HD", "220.00", "2024-01-17", "D2C"],
]

with open(raw / "ventas_prueba.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(datos)

print("CSV de prueba creado en data/raw/ventas.prueba.csv")
