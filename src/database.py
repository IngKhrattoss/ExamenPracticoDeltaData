from flask_sqlalchemy import SQLAlchemy
import os

# Definir la base de datos
db = SQLAlchemy()

def init_db(app):
     # Obtener la ruta base del proyecto
    base_dir = os.path.abspath(os.path.dirname(__file__))  
    db_path = os.path.join(base_dir, "ExamenCreditos.db")  # Crea la BD en el proyecto
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    print(f"📂 Base de datos usada: {app.config['SQLALCHEMY_DATABASE_URI']}")  # Verificar ruta
