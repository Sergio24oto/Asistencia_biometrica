#La logica de asistencia
from datetime import datetime, date
from database import obtener_conexion
from config import HORA_LIMITE_LLEGADA_TARDE


def calcular_minutos_tarde(hora_str, limite_str=HORA_LIMITE_LLEGADA_TARDE):
    try:
        partes_hora = [int(p) for p in hora_str.split(":")]
        partes_limite = [int(p) for p in limite_str.split(":")]

        segundos_hora = partes_hora[0] * 3600 + partes_hora[1] * 60 + (partes_hora[2] if len(partes_hora) > 2 else 0)
        segundos_limite = partes_limite[0] * 3600 + partes_limite[1] * 60 + (partes_limite[2] if len(partes_limite) > 2 else 0)

        diferencia = segundos_hora - segundos_limite
        if diferencia > 0:
            return max(1, round(diferencia / 60))
        return 0
    except Exception:
        return 0



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

    filas_presentes = cursor.fetchall()
    presentes = []
    llegadas_tarde = []

    for fila in filas_presentes:
        alumno = dict(fila)
        es_tarde = alumno["hora"] > HORA_LIMITE_LLEGADA_TARDE
        alumno["es_tarde"] = es_tarde
        if es_tarde:
            alumno["minutos_tarde"] = calcular_minutos_tarde(alumno["hora"])
            llegadas_tarde.append(alumno)
        else:
            alumno["minutos_tarde"] = 0
        presentes.append(alumno)

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

    ausentes = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return fecha, presentes, ausentes, llegadas_tarde