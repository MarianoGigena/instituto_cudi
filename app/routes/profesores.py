from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.conexion_bd import obtener_conexion
from .main import role_required

profesores_bp = Blueprint("profesores", __name__)


@profesores_bp.route("/profesores", methods=["GET"])
def profesores():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """SELECT profesores.id_profesor_dni, profesores.nombre, profesores.apellido, materias.nombre 
        FROM profesores
        INNER JOIN materias ON profesores.materias_id_materia = materias.id_materia"""
    )
    profesores = cursor.fetchall()
    query = "SELECT id_materia, nombre FROM materias"
    cursor.execute(query)
    materias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("profesores.html", profesores=profesores, materias=materias)


@profesores_bp.route("/profesores/add", methods=["POST"])
@role_required("admin")
def add():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    id_profesor_dni = request.form.get("id_profesor_dni")
    nombre = request.form.get("nombre")
    apellido = request.form.get("apellido")

    materia = request.form.get("materia")

    # Verifica que los campos requeridos estén completos
    if not nombre or not apellido or not materia:
        flash("Todos los campos son requeridos", "danger")
        return redirect(url_for("profesores"))  # Redirecciona a la página de alumnos

    # Construye la consulta SQL para insertar el nuevo alumno
    query = """
        INSERT INTO profesores (id_profesor_dni, nombre, apellido, materias_id_materia)
        VALUES (%s, %s, %s, %s)
    """
    values = (id_profesor_dni, nombre, apellido, materia)

    # Ejecuta la consulta e inserta los datos en la base de datos
    try:
        cursor.execute(query, values)
        conexion.commit()

        flash(f"Profesor {nombre} {apellido} agregado exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al agregar el profesor: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("profesores.profesores"))


@profesores_bp.route("/profesores/edit/<int:id_profesor_dni>", methods=["GET", "POST"])
@role_required("admin")
def edit(id_profesor_dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if request.method == "POST":
        id_profesor_dni = request.form["id_profesor_dni"]
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]

        materia = request.form["materia"]
        query = "UPDATE profesores SET id_profesor_dni = %s, nombre = %s, apellido = %s,  materias_id_materia = %s WHERE id_profesor_dni = %s"
        try:
            cursor.execute(
                query,
                (id_profesor_dni, nombre, apellido, materia, id_profesor_dni),
            )
            conexion.commit()
            flash(f"Profesor {nombre} {apellido}  editado exitosamente", "success")
        except Exception as e:
            conexion.rollback()
            flash("Error al editar el profesor: " + str(e), "danger")
        finally:
            cursor.close()
            conexion.close()

        return redirect(url_for("profesores.profesores"))


@profesores_bp.route("/profesores/delete/<int:id_profesor_dni>", methods=["POST"])
@role_required("admin")
def delete(id_profesor_dni):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "DELETE FROM profesores WHERE id_profesor_dni = %s"
    try:
        cursor.execute(query, (id_profesor_dni,))
        conexion.commit()
        flash(f"Profesor con id {id_profesor_dni} eliminado exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al eliminar el profesor: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("profesores.profesores"))
