import json
import os

ARCHIVO = "productos.json"


def _cargar_datos():
    if not os.path.exists(ARCHIVO):
        return []
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        contenido = f.read().strip()
        if not contenido:
            return []
        return json.loads(contenido)


def _guardar_datos(productos):
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)


def crear_producto(id, nombre, descripcion, precio, cantidad):
    productos = _cargar_datos()

    for p in productos:
        if p["id"] == id:
            return {"error": f"Ya existe un producto con id '{id}'"}

    nuevo = {
        "id": id,
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": precio,
        "cantidad": cantidad
    }
    productos.append(nuevo)
    _guardar_datos(productos)
    return {"ok": True, "producto": nuevo}


def leer_productos():
    return _cargar_datos()


def leer_producto_por_id(id):
    for p in _cargar_datos():
        if p["id"] == id:
            return p
    return {"error": f"No existe producto con id '{id}'"}


def actualizar_producto(id, datos):
    productos = _cargar_datos()

    for p in productos:
        if p["id"] == id:
            p.update(datos)
            _guardar_datos(productos)
            return {"ok": True, "producto": p}

    return {"error": f"No existe producto con id '{id}'"}


def eliminar_producto(id):
    productos = _cargar_datos()
    nuevos = [p for p in productos if p["id"] != id]

    if len(nuevos) == len(productos):
        return {"error": f"No existe producto con id '{id}'"}

    _guardar_datos(nuevos)
    return {"ok": True, "eliminado": id}