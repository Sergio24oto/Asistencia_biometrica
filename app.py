from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from config import SECRET_KEY, ADMIN_USER, ADMIN_PASSWORD_HASH
from servicios.asistencia_service import (
    registrar_asistencia_por_huella,
    registrar_asistencia_manual,
    obtener_asistencia_del_dia
)

app = Flask(__name__)
app.secret_key = SECRET_KEY


def login_required(f):
    @wraps(f)
    def funcion_decorada(*args, **kwargs):
        if "usuario" not in session:
            flash("Debes iniciar sesión para acceder.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return funcion_decorada


@app.route("/")
def inicio():
    if "usuario" in session:
        return redirect(url_for("ver_asistencia"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "usuario" in session:
        return redirect(url_for("ver_asistencia"))

    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        clave = request.form.get("clave", "").strip()

        if usuario == ADMIN_USER and check_password_hash(ADMIN_PASSWORD_HASH, clave):
            session["usuario"] = usuario
            flash("¡Bienvenida al sistema!", "exito")
            return redirect(url_for("ver_asistencia"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for("login"))


def render_asistencia_view(mensaje=None):
    fecha, presentes, ausentes, llegadas_tarde = obtener_asistencia_del_dia()

    total_matriculados = len(presentes) + len(ausentes)
    total_presentes = len(presentes)
    total_tardes = len(llegadas_tarde)
    total_puntuales = total_presentes - total_tardes
    total_ausentes = len(ausentes)

    porcentaje_asistencia = round((total_presentes / total_matriculados * 100)) if total_matriculados > 0 else 0

    return render_template(
        "asistencia.html",
        fecha=fecha,
        presentes=presentes,
        ausentes=ausentes,
        llegadas_tarde=llegadas_tarde,
        total_matriculados=total_matriculados,
        total_presentes=total_presentes,
        total_puntuales=total_puntuales,
        total_tardes=total_tardes,
        total_ausentes=total_ausentes,
        porcentaje_asistencia=porcentaje_asistencia,
        mensaje=mensaje
    )


@app.route("/asistencia")
@login_required
def ver_asistencia():
    return render_asistencia_view()


@app.route("/simular", methods=["POST"])
@login_required
def simular_huella_web():
    id_huella = request.form.get("id_huella")

    if not id_huella:
        return redirect(url_for("ver_asistencia"))

    resultado = registrar_asistencia_por_huella(int(id_huella))
    return render_asistencia_view(mensaje=resultado.get("mensaje"))


@app.route("/manual/<int:alumno_id>", methods=["POST"])
@login_required
def marcar_manual(alumno_id):
    resultado = registrar_asistencia_manual(alumno_id)
    return render_asistencia_view(mensaje=resultado.get("mensaje"))


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