from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.conexion_bd import obtener_conexion
from .main import role_required

materias_bp = Blueprint("materias", __name__)


@materias_bp.route("/materias", methods=["GET"])
@role_required("admin", "invitado", "user")
def materias():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("materias.html", materias=materias)


@materias_bp.route("/materias/add", methods=["POST"])
@role_required("admin")
def add():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    nombre = request.form.get("nombre")

    # Verifica que los campos requeridos estén completos
    if not nombre:
        flash("Todos los campos son requeridos", "danger")
        return redirect(url_for("materias"))  # Redirecciona a la página de alumnos

    # Construye la consulta SQL para insertar el nuevo alumno
    query = """
        INSERT INTO materias (nombre)
        VALUES (%s)
    """
    values = (nombre,)

    # Ejecuta la consulta e inserta los datos en la base de datos
    try:
        cursor.execute(query, values)
        conexion.commit()

        flash(f"La materia {nombre} fue agregada exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al agregar el materia: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("materias.materias"))  # Redirecciona a la página de alumnos


@materias_bp.route("/materias/edit/<int:id_materia>", methods=["GET", "POST"])
@role_required("admin")
def edit(id_materia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    if request.method == "POST":
        id_materia = request.form["id_materia"]
        nombre = request.form["nombre"]

        query = "UPDATE materias SET nombre = %s WHERE id_materia = %s"
        try:
            cursor.execute(
                query,
                (nombre, id_materia),
            )
            conexion.commit()
            flash(f"La materia {nombre} fue editada exitosamente", "success")
        except Exception as e:
            conexion.rollback()
            flash("Error al editar la materia: " + str(e), "danger")
        finally:
            cursor.close()
            conexion.close()

        return redirect(url_for("materias.materias"))


@materias_bp.route("/materias/delete/<int:id_materia>", methods=["POST"])
@role_required("admin")
def delete(id_materia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = "DELETE FROM materias WHERE id_materia = %s"
    try:
        cursor.execute(query, (id_materia,))
        conexion.commit()
        flash(f"Materia con id {id_materia} eliminada exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al eliminar la materia: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("materias.materias"))
