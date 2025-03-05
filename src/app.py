import io
from flask import Flask, Response, jsonify, redirect, render_template, request, url_for
from database import db, init_db
from models import Creditos  # Importar el modelo correcto
import os

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir,'src', 'templates')

app = Flask(__name__, template_folder=template_dir)

init_db(app)

#Rutaa de la aplicacion
@app.route('/')
def home():
    try:
        clientes = Creditos.query.all()
        clientes_dict = [cliente.__dict__ for cliente in clientes]
        
        # Eliminar metadatos de SQLAlchemy
        for cliente in clientes_dict:
            cliente.pop('_sa_instance_state', None)

        return render_template('index.html', data=clientes_dict)
    
    except Exception as e:
        return f"❌ Error al obtener clientes: {e}"
    
#Ruta para agregar un nuevo cliente
@app.route('/add', methods=['POST'])
def addCliente():
    try:
        cliente = Creditos(
            cliente=request.form['nombre'],
            monto=request.form['monto'],
            tasa_interes=request.form['ti'],
            plazo=request.form['plazo'],
            fecha_otorgamiento=request.form['date']
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"❌ Error al agregar cliente: {e}"

#Ruta para eliminar un cliente
@app.route('/delete/<int:id>')
def deleteCliente(id):
    try:
        cliente = Creditos.query.get(id)
        db.session.delete(cliente)
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"❌ Error al eliminar cliente: {e}"
    
#Ruta para editar un cliente
@app.route('/edit/<int:id>', methods=['POST'])
def editCliente(id):
    try:
        cliente = Creditos.query.get(id)
        if not cliente:
            return "❌ Cliente no encontrado", 404

        # Obtener los datos del formulario
        cliente.cliente = request.form.get('nombre')
        cliente.monto = float(request.form.get('monto'))
        cliente.tasa_interes = float(request.form.get('ti'))
        cliente.plazo = int(request.form.get('plazo'))
        cliente.fecha_otorgamiento = request.form.get('date')

        # Guardar cambios en la BD
        db.session.commit()
        return redirect(url_for('home'))
    except Exception as e:
        return f"❌ Error al editar cliente: {e}"


#Ruta para probar la conexión a la base de datos
@app.route('/test-db')
def test_db():
    try:
        clientes = Creditos.query.all()
        return f"✅ Conectado a la base de datos. creditos en la tabla: {len(clientes)}"
    except Exception as e:
        return f"❌ Error al conectar con la base de datos: {e}"


# Ruta para obtener datos de los créditos
@app.route('/data')
def get_data():
    try:
        # Obtener los créditos agrupados por cliente
        data = db.session.query(Creditos.cliente, db.func.sum(Creditos.monto)).group_by(Creditos.cliente).all()
        
        # Convertir datos a JSON
        chart_data = {
            "labels": [cliente for cliente, _ in data],
            "values": [monto for _, monto in data]
        }
        
        return jsonify(chart_data)
    except Exception as e:
        return jsonify({"error": str(e)})




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True, port=9000)