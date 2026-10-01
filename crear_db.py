import sqlite3
from config import DB_NAME


def crear_tablas():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            apellido TEXT NOT NULL,
            nombre TEXT NOT NULL,
            id_huella INTEGER UNIQUE NOT NULL,
            activo INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asistencias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            origen TEXT NOT NULL CHECK (origen IN ('huella', 'manual')),

            FOREIGN KEY (alumno_id) REFERENCES alumnos(id),
            UNIQUE (alumno_id, fecha)
        )
    """)

    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    crear_tablas()
    print("Tablas creadas correctamente.")