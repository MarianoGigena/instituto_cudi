from flask import Flask


def create_app():
    app = Flask(__name__)

    app.secret_key = "tu_clave_secreta_aqui"

    from .routes.main import main
    from .routes.alumnos import alumnos_bp
    from .routes.materias import materias_bp
    from .routes.profesores import profesores_bp
    from .routes.cursos import cursos_bp
    from .routes.admin import admin_bp

    app.register_blueprint(cursos_bp)
    app.register_blueprint(profesores_bp)
    app.register_blueprint(materias_bp)
    app.register_blueprint(main)
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(admin_bp)
    return app
