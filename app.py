from flask import Flask, render_template, request, redirect, url_for
from servicios.asistencia_service import (
    registrar_asistencia_por_huella,
    registrar_asistencia_manual,
    obtener_asistencia_del_dia
)

app = Flask(__name__)


@app.route("/")
def inicio():
    return redirect(url_for("ver_asistencia"))


@app.route("/asistencia")
def ver_asistencia():
    fecha, presentes, ausentes = obtener_asistencia_del_dia()

    return render_template(
        "asistencia.html",
        fecha=fecha,
        presentes=presentes,
        ausentes=ausentes,
        mensaje=None
    )


@app.route("/simular", methods=["POST"])
def simular_huella_web():
    id_huella = request.form.get("id_huella")

    if not id_huella:
        return redirect(url_for("ver_asistencia"))

    resultado = registrar_asistencia_por_huella(int(id_huella))

    fecha, presentes, ausentes = obtener_asistencia_del_dia()

    return render_template(
        "asistencia.html",
        fecha=fecha,
        presentes=presentes,
        ausentes=ausentes,
        mensaje=resultado["mensaje"]
    )


@app.route("/manual/<int:alumno_id>", methods=["POST"])
def marcar_manual(alumno_id):
    resultado = registrar_asistencia_manual(alumno_id)

    fecha, presentes, ausentes = obtener_asistencia_del_dia()

    return render_template(
        "asistencia.html",
        fecha=fecha,
        presentes=presentes,
        ausentes=ausentes,
        mensaje=resultado["mensaje"]
    )


@app.route("/api/registrar_huella", methods=["POST"])
def registrar_huella_api():
    datos = request.get_json()

    if not datos:
        return {
            "ok": False,
            "mensaje": "No se recibieron datos"
        }, 400

    id_huella = datos.get("id_huella")

    if id_huella is None:
        return {
            "ok": False,
            "mensaje": "Falta el id_huella"
        }, 400

    resultado = registrar_asistencia_por_huella(int(id_huella))

    return resultado


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)