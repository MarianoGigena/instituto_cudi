from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort,
)
from app.conexion_bd import obtener_conexion
from .main import role_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin-panel")
def admin_panel():
    if session.get("role") != "admin":
        abort(403)  # Retorna un error "403 Forbidden" si el usuario no es admin

    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Consulta a la tabla 'usuarios'
        consulta = "SELECT id_usuario, nombre, password, role, estado FROM usuarios"
        cursor.execute(consulta)

        # Obtener todos los resultados
        usuarios = cursor.fetchall()

        # Renderizar la plantilla con los usuarios
        return render_template("admin_panel.html", usuarios=usuarios)

    except Exception as err:
        print(f"Error: {err}")
        return "Error al conectar con la base de datos."

    finally:
        cursor.close()
        conexion.close()


@admin_bp.route("/admin-panel/editar", methods=["POST"])
@role_required("admin")
def editar_usuario():
    print("edicion de usuario")
    # Captura los datos del formulario
    id_usuario = request.form.get("id_usuario")
    nombre = request.form.get("nombre")
    password = request.form.get("password")
    role = request.form.get("role")

    # Validación básica de los datos
    if not id_usuario or not nombre or not password or not role:
        flash("Todos los campos son obligatorios.", "danger")
        return redirect(url_for("admin.admin_panel"))

    # Conexión a la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Actualizar los datos del usuario
        query = """
        UPDATE usuarios
        SET nombre = %s, password = %s, role = %s
        WHERE id_usuario = %s
        """
        cursor.execute(query, (nombre, password, role, id_usuario))
        conexion.commit()

        # Mensaje de éxito
        flash(f"Usuario {nombre} actualizado exitosamente.", "success")
    except Exception as err:
        # Manejo de errores
        print(f"Error: {err}")
        flash("Hubo un error al actualizar el usuario.", "danger")
    finally:
        cursor.close()
        conexion.close()

    # Redirigir al panel de administración
    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/admin_panel/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    # Captura el ID del usuario desde el formulario
    id_usuario = request.form.get("id_usuario")
    print(f"id de usuario{request.form}")
    # Validar que el ID no esté vacío
    if not id_usuario:
        flash("El ID del usuario es obligatorio para eliminarlo.", "danger")
        return redirect(url_for("admin.admin_panel"))

    # Conexión a la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Consulta SQL para eliminar el usuario
        print(f"id {id_usuario}")
        query = """UPDATE usuarios 
        SET estado = 'inactivo' 
        WHERE id_usuario = %s"""
        cursor.execute(query, (id_usuario,))
        conexion.commit()

        # Verificar si se eliminó algún registro
        if cursor.rowcount == 0:
            flash("No se encontró ningún usuario con ese ID.", "warning")
        else:
            flash(f"Usuario {id_usuario} desactivado exitosamente.", "success")
    except Exception as err:
        # Manejo de errores
        print(f"Error: {err}")
        flash("Hubo un error al eliminar el usuario.", "danger")
    finally:
        cursor.close()
        conexion.close()

    # Redirigir al panel de administración
    return redirect(url_for("admin.admin_panel"))


@admin_bp.route("/activar_usuario", methods=["POST"])
def activar_usuario():
    id_usuario = request.form.get("id_usuario")

    if not id_usuario:
        flash("No se proporcionó el ID del usuario", "warning")
        return redirect(url_for("admin.admin_panel"))

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Actualizar el estado del usuario a "activo"
        query = "UPDATE usuarios SET estado = 'activo' WHERE id_usuario = %s"
        cursor.execute(query, (id_usuario,))
        conexion.commit()
        flash("El usuario ha sido activado correctamente.", "success")
    except Exception as e:
        conexion.rollback()
        flash(f"Error al activar el usuario: {e}", "danger")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("admin.admin_panel"))
