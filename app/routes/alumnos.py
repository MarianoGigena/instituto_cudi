from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.conexion_bd import obtener_conexion

alumnos_bp = Blueprint("alumnos", __name__)


@alumnos_bp.route("/alumnos", methods=["GET"])
def alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()
    query = "SELECT id_materia, nombre FROM materias"
    cursor.execute(query)
    materias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("alumnos.html", alumnos=alumnos, materias=materias)


@alumnos_bp.route("/alumnos/edit/<int:id_alumno_dni>", methods=["GET", "POST"])
def edit(id_alumno_dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if request.method == "POST":
        id_alumno_dni_nuevo = request.form["id_alumno_dni"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]

        fecha_nacimiento = request.form["fecha_nacimiento"]
        genero = request.form["genero"]
        query = "UPDATE alumnos SET id_alumno_dni=%s, nombre = %s, apellido = %s, fecha_nacimiento = %s, genero = %s WHERE id_alumno_dni = %s"
        try:
            cursor.execute(
                query,
                (
                    id_alumno_dni_nuevo,
                    nombre,
                    apellido,
                    fecha_nacimiento,
                    genero,
                    id_alumno_dni,
                ),
            )
            conexion.commit()
            flash(f"Alumno {nombre} {apellido}  editado exitosamente", "success")
        except Exception as e:
            conexion.rollback()
            flash("Error al editar el alumno: " + str(e), "danger")
        finally:
            cursor.close()
            conexion.close()

        return redirect(url_for("alumnos.alumnos"))


@alumnos_bp.route("/alumnos/add", methods=["POST"])
def add():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    id_alumno_dni = request.form.get("id_alumno_dni")
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")

    fecha_nacimiento = request.form.get("fecha_nacimiento")
    genero = request.form.get("genero")

    # Verifica que los campos requeridos estén completos
    if (
        not nombre
        or not apellido
        or not id_alumno_dni
        or not fecha_nacimiento
        or not genero
    ):
        flash("Todos los campos son requeridos", "danger")
        return redirect(url_for("alumnos"))  # Redirecciona a la página de alumnos

    # Construye la consulta SQL para insertar el nuevo alumno
    query = """
        INSERT INTO alumnos (id_alumno_dni, nombre, apellido, fecha_nacimiento, genero)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (id_alumno_dni, nombre, apellido, fecha_nacimiento, genero)

    # Ejecuta la consulta e inserta los datos en la base de datos
    try:
        cursor.execute(query, values)
        conexion.commit()

        flash(f"Alumno {nombre} {apellido} agregado exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al agregar el alumno: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("alumnos.alumnos"))  # Redirecciona a la página de alumnos


@alumnos_bp.route("/alumnos/delete/<int:id_alumno_dni>", methods=["POST"])
def delete(id_alumno_dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "DELETE FROM alumnos WHERE id_alumno_dni = %s"
    try:
        cursor.execute(query, (id_alumno_dni,))
        conexion.commit()
        flash(f"Alumno con id {id_alumno_dni} eliminado exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al eliminar el alumno: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("alumnos.alumnos"))
