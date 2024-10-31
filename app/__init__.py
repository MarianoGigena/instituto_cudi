from flask import Flask


def create_app():
    app = Flask(__name__)

    app.secret_key = "tu_clave_secreta_aqui"

    from .routes.main import main
    from .routes.alumnos import alumnos_bp
    from .routes.materias import materias_bp

    app.register_blueprint(materias_bp)
    app.register_blueprint(main)
    app.register_blueprint(alumnos_bp)
    return app
