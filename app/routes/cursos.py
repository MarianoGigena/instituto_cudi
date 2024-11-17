from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.conexion_bd import obtener_conexion
from .main import role_required

cursos_bp = Blueprint("cursos", __name__)


@cursos_bp.route("/cursos", methods=["GET", "POST"])
@role_required("admin", "invitado", "user")
def ver_cursos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    query = """
        SELECT 
            cursos.alumnos_id_alumno_dni, 
            alumnos.nombre AS alumno_nombre,
            alumnos.apellido AS alumno_apellido,
            materias.nombre AS materia_nombre,
            cursos.estado,
            cursos.parcial_1,
            cursos.parcial_2,
            cursos.nota_final,
            cursos.materias_id_materia
        FROM 
            cursos
        JOIN 
            alumnos ON cursos.alumnos_id_alumno_dni = alumnos.id_alumno_dni
        JOIN 
            materias ON cursos.materias_id_materia = materias.id_materia;
    """
    cursor.execute("SELECT DISTINCT nombre FROM materias")
    materias = [row[0] for row in cursor.fetchall()]

    cursor.execute(query)

    cursos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("cursos.html", cursos=cursos, materias=materias)


@cursos_bp.route("/cursos/inscribir", methods=["POST"])
@role_required("admin")
def inscribir():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    alumnos_id_alumno_dni = request.form.get("alumnos_id_alumno_dni")
    materias_id_materia = request.form.get("materias_id_materia")
    estado = request.form.get("estado")

    query = """
        INSERT INTO cursos (alumnos_id_alumno_dni, materias_id_materia, estado)
        VALUES (%s, %s, %s)
    """
    values = (alumnos_id_alumno_dni, materias_id_materia, estado)

    try:
        cursor.execute(query, values)
        conexion.commit()
        flash("Alumno inscrito en la materia exitosamente", "success")
    except Exception as e:
        conexion.rollback()
        flash("Error al inscribir al alumno: " + str(e), "danger")
    finally:
        cursor.close()
        conexion.close()

    return redirect(url_for("cursos.ver_cursos"))


@cursos_bp.route(
    "/cursos/calificar/<int:id_alumno_dni>/<int:id_materia>", methods=["GET", "POST"]
)
@role_required("admin")
def calificar(id_alumno_dni, id_materia):
    if request.method == "POST":
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtén los valores de los parciales del formulario
        parcial_1 = request.form.get("parcial_1", type=float)
        # parcial_2 = request.form.get("parcial_2", type=float)

        # Asegúrate de que los valores de los parciales no son None
        if parcial_1 is None:
            parcial_1 = 0.0
        # if parcial_2 is None:
        #   parcial_2 = 0.0

        query = """
            UPDATE cursos 
            SET parcial_1 = %s 
            WHERE alumnos_id_alumno_dni = %s AND materias_id_materia = %s
        """
        try:
            cursor.execute(query, (parcial_1, id_alumno_dni, id_materia))
            conexion.commit()
            flash("Calificaciones guardadas correctamente", "success")
        except Exception as e:
            conexion.rollback()
            flash(f"Error al guardar calificaciones: {str(e)}", "danger")
        finally:
            cursor.close()
            conexion.close()
        return redirect(url_for("cursos.ver_cursos"))
    flash("Método no permitido", "danger")
    return redirect(url_for("cursos.ver_cursos"))


@cursos_bp.route(
    "/cursos/calificar2/<int:id_alumno_dni>/<int:id_materia>", methods=["GET", "POST"]
)
@role_required("admin")
def calificar2(id_alumno_dni, id_materia):
    if request.method == "POST":
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Obtén los valores de los parciales del formulario
        # parcial_1 = request.form.get("parcial_1", type=float)
        parcial_2 = request.form.get("parcial_2", type=float)

        # Asegúrate de que los valores de los parciales no son None

        if parcial_2 is None:
            parcial_2 = 0.0

        query = """
            UPDATE cursos 
            SET parcial_2 = %s 
            WHERE alumnos_id_alumno_dni = %s AND materias_id_materia = %s
        """
        try:
            cursor.execute(query, (parcial_2, id_alumno_dni, id_materia))
            conexion.commit()
            flash("Calificaciones guardadas correctamente", "success")
        except Exception as e:
            conexion.rollback()
            flash(f"Error al guardar calificaciones: {str(e)}", "danger")
        finally:
            cursor.close()
            conexion.close()
        return redirect(url_for("cursos.ver_cursos"))
    flash("Método no permitido", "danger")
    return redirect(url_for("cursos.ver_cursos"))


@cursos_bp.route(
    "/cursos/actualizar_nota_final/<int:id_alumno_dni>/<int:id_materia>",
    methods=["POST"],
)
@role_required("admin")
def actualizar_nota_final(id_alumno_dni, id_materia):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener los valores de los parciales desde la base de datos
    cursor.execute(
        """
        SELECT parcial_1, parcial_2 
        FROM cursos 
        WHERE alumnos_id_alumno_dni = %s AND materias_id_materia = %s
    """,
        (id_alumno_dni, id_materia),
    )
    result = cursor.fetchone()
    parcial_1 = result[0] if result else 0.0
    parcial_2 = result[1] if result else 0.0

    # Calcular la nota final
    nota_final = (parcial_1 + parcial_2) / 2

    # Actualizar la nota final en la base de datos
    query = """
        UPDATE cursos 
        SET nota_final = %s 
        WHERE alumnos_id_alumno_dni = %s AND materias_id_materia = %s
    """
    try:
        cursor.execute(query, (nota_final, id_alumno_dni, id_materia))
        conexion.commit()
        flash("Nota final actualizada correctamente", "success")
    except Exception as e:
        conexion.rollback()
        flash(f"Error al actualizar la nota final: {str(e)}", "danger")
    finally:
        cursor.close()
        conexion.close()
    return redirect(url_for("cursos.ver_cursos"))


@cursos_bp.route("/cursos/filtros", methods=["GET", "POST"])
@role_required("admin")
def filtros():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    dni = request.args.get("dni", "")
    apellido = request.args.get("apellido", "")
    materia = request.args.get("materia", "")

    print(f"Filtros recibidos: DNI={dni}, Apellido={apellido}, Materia={materia}")

    query = """
        SELECT 
            cursos.alumnos_id_alumno_dni, 
            alumnos.nombre AS alumno_nombre,
            alumnos.apellido AS alumno_apellido,
            materias.nombre AS materia_nombre,
            cursos.estado,
            cursos.parcial_1,
            cursos.parcial_2,
            cursos.nota_final,
            cursos.materias_id_materia
        FROM 
            cursos
        JOIN 
            alumnos ON cursos.alumnos_id_alumno_dni = alumnos.id_alumno_dni
        JOIN 
            materias ON cursos.materias_id_materia = materias.id_materia
        WHERE 1=1
    """
    params = []

    if dni:
        query += " AND cursos.alumnos_id_alumno_dni LIKE %s"
        params.append(f"%{dni}%")
    if apellido:
        query += " AND alumnos.apellido LIKE %s"
        params.append(f"%{apellido}%")
    if materia:
        query += " AND materias.nombre LIKE %s"
        params.append(f"%{materia}%")

    print(f"Consulta generada: {query} con parámetros {params}")

    try:
        cursor.execute(query, params)
        cursos = cursor.fetchall()
        cursor.execute("SELECT DISTINCT nombre FROM materias")
        materias = [row[0] for row in cursor.fetchall()]
        print(f"Resultados encontrados: {cursos}")
    except Exception as e:
        print(f"Error en la consulta: {e}")
        cursos = []
    finally:
        cursor.close()
        conexion.close()
    return render_template("cursos.html", cursos=cursos, materias=materias)


@cursos_bp.route("/cursos/eliminar_curso", methods=["POST"])
def eliminar_curso():
    # Captura el ID del usuario desde el formulario
    id_alumno = request.form.get("id_alumno_dni")
    id_materia = request.form.get("id_materia")
    materia = request.form.get("materia")
    print(f"id de usuario{request.form}")
    # Validar que el ID no esté vacío
    if not id_alumno or not id_materia:
        flash("El ID del usuario es obligatorio para eliminarlo.", "danger")
        return redirect(url_for("cursos.ver_cursos"))

    # Conexión a la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Consulta SQL para eliminar el usuario
        print(f"id {id_alumno}")
        query = "DELETE FROM cursos WHERE alumnos_id_alumno_dni = %s and materias_id_materia = %s"
        cursor.execute(
            query,
            (
                id_alumno,
                id_materia,
            ),
        )
        conexion.commit()

        # Verificar si se eliminó algún registro
        if cursor.rowcount == 0:
            flash("No se encontró ningún curso con ese ID.", "warning")
        else:
            flash(
                f"Curso {id_alumno} {id_materia} {materia} eliminado exitosamente.",
                "success",
            )
    except Exception as err:
        # Manejo de errores
        print(f"Error: {err}")
        flash("Hubo un error al eliminar el curso.", "danger")
    finally:
        cursor.close()
        conexion.close()

    # Redirigir al panel de administración
    return redirect(url_for("cursos.ver_cursos"))
