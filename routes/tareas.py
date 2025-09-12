from flask import Blueprint, request, jsonify
from config.db import get_db_connection, mysql
from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear el blueprint
tareas_bp = Blueprint("tareas", __name__)

# Crear un endpoint obtener tareas


@tareas_bp.route("/obtener", methods=["GET"])
@jwt_required()
def get():
    # Obtenemos la identidad del dueño del token
    current_user = get_jwt_identity()

    # Conectamos a la bd
    cursor = get_db_connection()

    # Ejecutar la consulta
    query = """
                SELECT a.id_usuario, a.descripcion, b.nombre, b.email, a.creado_en
                FROM tareas as a
                INNER JOIN usuarios as b
                WHERE a.id_usuario = %s    
            """
    cursor.execute(query, (current_user,))
    lista = cursor.fetchall()
    if not lista:
        return jsonify({"Error": "El usuario no tiene tareas"}), 404
    else:
        return jsonify({"lista": lista}), 200


# Crear endpoint con post recibiendo datos desde el body


@tareas_bp.route("/crear", methods=["POST"])
@jwt_required()
def crear():
    # Obtener la identidad del dueño del token
    current_user = get_jwt_identity()

    # Obtener los datos del body

    data = request.get_json()

    descripcion = data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "Debes teclear una descripcion"}), 400

    # Obtenemos el cursor
    cursor = get_db_connection()

    # Hacemos el insert
    try:
        cursor.execute(
            "INSERT INTO tareas (descripcion, id_usuario) values (%s, %s)",
            (descripcion, current_user),
        )
        cursor.connection.commit()
        return jsonify({"message": "Tarea creada"}), 201
    except Exception as e:
        return jsonify({"Error": f"No se pudo crear la tarea: {str(e)}"})
    finally:
        cursor.close()


# Crear endpoint usando PUT y pasando datos por el body y el url


@tareas_bp.route("/modificar/<int:user_id>", methods=["PUT"])
@jwt_required()
def modificar(id_tareas):

    current_user = get_jwt_identity()
    # Obtenemos los datos del body
    data = request.get_json()

    description = data.get("description")

    cursor = get_db_connection()

    query = "SELECT * FROM tareas WHERE id_tareas = %s"

    cursor.execute(query, (id_tareas))
    tarea = cursor.fetchone()

    if not tarea:
        jsonify({"error": "No hay tareaaaaaaaaaaaaaaa"}), 404

    return jsonify({})
