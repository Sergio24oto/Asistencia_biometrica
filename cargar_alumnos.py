import sqlite3
from config import DB_NAME


def cargar_alumnos():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    alumnos = [

        ("Maximo", "Vivas", 1),
        ("Alessio", "Thiago", 2),
        ("Aguinaldo", "Valentina", 3),
        ("Avila", "Nelson", 4),
        ("Angulo", "Lorena", 5),
        ("Carena", "Jazmin", 6),
        ("Farias", "Laureno", 7),
        ("Fernandez", "Francisco", 8),
        ("Herrador", "Alexander", 9),
        ("Ibañez", "Emma", 10),
        ("Moyano", "Miriam", 11),
        ("Pascal", "Blas", 12),
        ("Pascal", "Nacho", 13),
        ("Quaglia", "Candela", 14),
        ("Rinaudo", "Trinidad", 15),
        ("Rodriguez", "Maria Sol", 16),
        ("Rodriguez", "Santiago", 17),
        ("Sotomayor", "Kris", 18),
        ("Sorello", "Tomas", 19),
        ("Silva", "Benjamin", 20),
        ("Taus", "Bejamin", 21),
        ("Villada", "Betiana", 22),
        ("Yllarra", "Benjamin", 23),
        ("Baldo", "Gael", 24),
        ("Prado","Mauricio",25)
        

    ]

    for apellido, nombre, id_huella in alumnos:
        cursor.execute("""
            INSERT INTO alumnos (apellido, nombre, id_huella)
            VALUES (?, ?, ?)
        """, (apellido, nombre, id_huella))

    conexion.commit()
    conexion.close()

    print("Alumnos cargados correctamente.")


if __name__ == "__main__":
    cargar_alumnos()