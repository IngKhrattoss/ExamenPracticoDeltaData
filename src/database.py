from flask_sqlalchemy import SQLAlchemy
import os

# Definir la base de datos
db = SQLAlchemy()

def init_db(app):
    db_path = os.path.normpath("C:/Users/ilayg/workspaces/bdsqlite/prueba2.db")  # Normaliza la ruta
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    print(f"📂 Base de datos usada: {app.config['SQLALCHEMY_DATABASE_URI']}")  # Verificar ruta
