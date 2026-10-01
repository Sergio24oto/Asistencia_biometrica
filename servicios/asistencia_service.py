#La logica de asistencia
from datetime import datetime, date
from database import obtener_conexion


def obtener_fecha_actual():
    return date.today().isoformat()


def obtener_hora_actual():
    return datetime.now().strftime("%H:%M:%S")


def buscar_alumno_por_huella(id_huella):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, apellido, nombre, id_huella
        FROM alumnos
        WHERE id_huella = ?
        AND activo = 1
    """, (id_huella,))

    alumno = cursor.fetchone()
    conexion.close()

    return alumno


def alumno_ya_registro_asistencia(alumno_id, fecha):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id
        FROM asistencias
        WHERE alumno_id = ?
        AND fecha = ?
    """, (alumno_id, fecha))

    asistencia = cursor.fetchone()
    conexion.close()

    return asistencia is not None


def registrar_asistencia_por_huella(id_huella):
    alumno = buscar_alumno_por_huella(id_huella)

    if alumno is None:
        return {
            "ok": False,
            "mensaje": "Huella no reconocida"
        }

    fecha = obtener_fecha_actual()
    hora = obtener_hora_actual()

    if alumno_ya_registro_asistencia(alumno["id"], fecha):
        return {
            "ok": False,
            "mensaje": "El alumno ya registró asistencia hoy",
            "alumno": f"{alumno['apellido']} {alumno['nombre']}"
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO asistencias (alumno_id, fecha, hora, origen)
        VALUES (?, ?, ?, ?)
    """, (
        alumno["id"],
        fecha,
        hora,
        "huella"
    ))

    conexion.commit()
    conexion.close()

    return {
        "ok": True,
        "mensaje": "Asistencia registrada correctamente",
        "alumno": f"{alumno['apellido']} {alumno['nombre']}",
        "hora": hora
    }


def registrar_asistencia_manual(alumno_id):
    fecha = obtener_fecha_actual()
    hora = obtener_hora_actual()

    if alumno_ya_registro_asistencia(alumno_id, fecha):
        return {
            "ok": False,
            "mensaje": "Alumno presente"
        }

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO asistencias (alumno_id, fecha, hora, origen)
        VALUES (?, ?, ?, ?)
    """, (
        alumno_id,
        fecha,
        hora,
        "manual"
    ))

    conexion.commit()
    conexion.close()

    return {
        "ok": True,
        "mensaje": "Asistencia manual registrada correctamente"
    }


def obtener_asistencia_del_dia():
    fecha = obtener_fecha_actual()

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT 
            alumnos.id,
            alumnos.apellido,
            alumnos.nombre,
            asistencias.hora,
            asistencias.origen
        FROM alumnos
        INNER JOIN asistencias
            ON alumnos.id = asistencias.alumno_id
        WHERE asistencias.fecha = ?
        AND alumnos.activo = 1
        ORDER BY alumnos.apellido, alumnos.nombre
    """, (fecha,))

    presentes = cursor.fetchall()

    cursor.execute("""
        SELECT 
            alumnos.id,
            alumnos.apellido,
            alumnos.nombre
        FROM alumnos
        WHERE alumnos.activo = 1
        AND alumnos.id NOT IN (
            SELECT alumno_id
            FROM asistencias
            WHERE fecha = ?
        )
        ORDER BY alumnos.apellido, alumnos.nombre
    """, (fecha,))

    ausentes = cursor.fetchall()

    conexion.close()

    return fecha, presentes, ausentes