import os
from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.environ.get("DB_PATH", os.path.join(BASE_DIR, "database.db"))
SECRET_KEY = os.environ.get("SECRET_KEY", "proa_secreto_asistencia_2026")

ADMIN_USER = os.environ.get("ADMIN_USER", "Preceptora")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "proalp2026")
ADMIN_PASSWORD_HASH = generate_password_hash(ADMIN_PASSWORD)

# Horario de jornada escolar (Argentina)
# Inicio de recepción de alumnos: 06:30 hs
# Límite de puntualidad: 08:10 hs (ingresos posteriores son llegadas tarde)
HORA_INICIO_JORNADA = os.environ.get("HORA_INICIO", "06:30:00")
HORA_LIMITE_LLEGADA_TARDE = os.environ.get("HORA_LIMITE", "08:10:00")