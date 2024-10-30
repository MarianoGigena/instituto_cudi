from flask import Blueprint, render_template, request, redirect, url_for, session
from app.conexion_bd import obtener_conexion

alumnos_bp = Blueprint("alumnos", __name__)


@alumnos_bp.route("/alumnos", methods=["GET"])
def alumnos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM alumnos")
    alumnos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render_template("alumnos.html", alumnos=alumnos)
