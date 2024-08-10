# servidor.py

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo de la tabla de logs
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    servicio = db.Column(db.String(50), nullable=False)
    nivel = db.Column(db.String(20), nullable=False)
    mensaje = db.Column(db.String(200), nullable=False)
    fecha_recepcion = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

# Lista de tokens válidos para autenticación
tokens_validos = ['token1', 'token2', 'token3']

# Endpoint para recibir logs
@app.route('/logs', methods=['POST'])
def recibir_logs():
    token = request.headers.get('Authorization')
    if token not in tokens_validos:
        return jsonify({'error': 'Unauthorized'}), 401

    datos = request.get_json()
    nuevo_log = Log(
        fecha_evento=datetime.datetime.strptime(datos['fecha_evento'], '%Y-%m-%d %H:%M:%S'),
        servicio=datos['servicio'],
        nivel=datos['nivel'],
        mensaje=datos['mensaje']
    )
    db.session.add(nuevo_log)
    db.session.commit()
    
    return jsonify({'mensaje': 'Log almacenado exitosamente'}), 201

# Endpoint para obtener logs
@app.route('/logs', methods=['GET'])
def obtener_logs():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')

    query = Log.query
    if fecha_inicio and fecha_fin:
        fecha_inicio = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d %H:%M:%S')
        fecha_fin = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d %H:%M:%S')
        query = query.filter(Log.fecha_evento.between(fecha_inicio, fecha_fin))
    
    logs = query.all()
    resultado = []
    for log in logs:
        resultado.append({
            'fecha_evento': log.fecha_evento.strftime('%Y-%m-%d %H:%M:%S'),
            'servicio': log.servicio,
            'nivel': log.nivel,
            'mensaje': log.mensaje,
            'fecha_recepcion': log.fecha_recepcion.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify(resultado), 200

if __name__ == '__main__':
    app.run(debug=True)
