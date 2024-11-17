from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    abort,
)
from ..conexion_bd import obtener_conexion
from functools import wraps


""" def role_required(required_role):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("role") != required_role:
                flash("No tienes permisos para esa acción.", "danger")
                return redirect(
                    url_for("alumnos.alumnos")
                )  # Redirige al usuario a la página de inicio o a una página de error
            return f(*args, **kwargs)

        return decorated_function

    return wrapper """


def role_required(*required_roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = session.get("role")
            if user_role not in required_roles:
                flash("No tienes permisos para esa acción.", "danger")
                return redirect(
                    url_for("alumnos.alumnos")
                )  # Redirige al usuario a la página de inicio o a una página de error
            return f(*args, **kwargs)

        return decorated_function

    return wrapper


main = Blueprint("main", __name__)


@main.route("/")
def index():
    if session:
        logout()
    else:
        pass
    return render_template("login.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Conectar a la base de datos
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)

        # Buscar el usuario en la base de datos
        cursor.execute(
            "SELECT * FROM usuarios WHERE nombre = %s AND password = %s",
            (username, password),
        )
        user = cursor.fetchone()
        cursor.close()
        db.close()

        # Verificar usuario y contraseña
        if user:
            # Inicia sesión: almacena el id y rol en la sesión
            session["user_id"] = user["id_usuario"]
            session["nombre"] = user["nombre"]
            session["role"] = user["role"]

            flash("Inicio de sesión exitoso.", "success")
            return redirect(url_for("alumnos.alumnos"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@main.route("/logout")
def logout():
    session.clear()  # Limpia todos los datos de la sesión
    flash("Has cerrado sesión.", "info")
    return redirect(url_for("main.login"))


@main.route("/registro", methods=["POST"])
def registro():
    username = request.form.get("username")
    password = request.form.get("password")
    role = request.form.get("role")

    if not username or not password or not role:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(
            url_for("main.login")
        )  # Ajusta la redirección según corresponda

    try:
        # Comprobando si el usuario ya existe
        db = obtener_conexion()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE nombre = %s", (username,))
        user = cursor.fetchone()

        if user:
            flash("El usuario ya está registrado.", "danger")
        else:
            # Insertar el nuevo usuario en la base de datos
            cursor.execute(
                "INSERT INTO usuarios (nombre, password, role) VALUES (%s, %s, %s)",
                (username, password, role),
            )
            db.commit()
            flash("Registro exitoso. ¡Puedes iniciar sesión!", "success")
    except Exception as e:
        db.rollback()
        flash(f"Error al registrar el usuario: {str(e)}", "danger")
    finally:
        cursor.close()

    return redirect(url_for("main.login"))
