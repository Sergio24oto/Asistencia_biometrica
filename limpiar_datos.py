import sqlite3
from config import DB_NAME


def limpiar_datos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    # Primero borramos asistencias porque dependen de alumnos
    cursor.execute("DELETE FROM asistencias")

    # Después borramos alumnos
    cursor.execute("DELETE FROM alumnos")

    conexion.commit()
    conexion.close()

    print("Datos de prueba eliminados correctamente.")


if __name__ == "__main__":
    limpiar_datos()