import unittest
import os
import json
import sys

# Permite importar productos.py desde la carpeta raíz
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from productos import (
    crear_producto,
    leer_productos,
    leer_producto_por_id,
    actualizar_producto,
    eliminar_producto,
    ARCHIVO
)


def limpiar_archivo():
    """Borra el contenido del JSON antes de cada prueba para partir limpio."""
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        json.dump([], f)


class TestCrear(unittest.TestCase):

    def setUp(self):
        limpiar_archivo()

    def test_crear_exitoso(self):
        """Crear un producto nuevo debe retornar ok y los datos correctos."""
        resultado = crear_producto(1, "Teclado", "Teclado mecánico", 150000, 10)
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["producto"]["nombre"], "Teclado")

    def test_crear_id_duplicado(self):
        """Crear un producto con id repetido debe retornar error."""
        crear_producto(1, "Teclado", "Teclado mecánico", 150000, 10)
        resultado = crear_producto(1, "Mouse", "Mouse inalámbrico", 80000, 5)
        self.assertIn("error", resultado)


class TestLeer(unittest.TestCase):

    def setUp(self):
        limpiar_archivo()

    def test_leer_todos_exitoso(self):
        """Leer productos debe retornar la lista con los productos creados."""
        crear_producto(1, "Teclado", "Teclado mecánico", 150000, 10)
        crear_producto(2, "Mouse", "Mouse inalámbrico", 80000, 5)
        resultado = leer_productos()
        self.assertEqual(len(resultado), 2)

    def test_leer_por_id_exitoso(self):
        """Buscar por id existente debe retornar el producto correcto."""
        crear_producto(1, "Teclado", "Teclado mecánico", 150000, 10)
        resultado = leer_producto_por_id(1)
        self.assertEqual(resultado["nombre"], "Teclado")

    def test_leer_por_id_no_existe(self):
        """Buscar por id inexistente debe retornar error."""
        resultado = leer_producto_por_id(999)
        self.assertIn("error", resultado)


class TestActualizar(unittest.TestCase):

    def setUp(self):
        limpiar_archivo()

    def test_actualizar_exitoso(self):
        """Actualizar un campo de un producto existente debe reflejarse."""
        crear_producto(1, "Teclado", "Teclado mecánico", 150000, 10)
        resultado = actualizar_producto(1, {"precio": 170000})
        self.assertTrue(resultado["ok"])
        self.assertEqual(resultado["producto"]["precio"], 170000)

    def test_actualizar_no_existe(self):
        """Actualizar un producto inexistente debe retornar error."""
        resultado = actualizar_producto(999, {"precio": 170000})
        self.assertIn("error", resultado)


class TestEliminar(unittest.TestCase):

    def setUp(self):
        limpiar_archivo()

    def test_eliminar_exitoso(self):
        """Eliminar un producto existente debe retornar ok."""
        crear_producto(1, "Teclado", "Teclado mecánico", 150000, 10)
        resultado = eliminar_producto(1)
        self.assertTrue(resultado["ok"])

    def test_eliminar_no_existe(self):
        """Eliminar un producto inexistente debe retornar error."""
        resultado = eliminar_producto(999)
        self.assertIn("error", resultado)


if __name__ == "__main__":
    unittest.main()