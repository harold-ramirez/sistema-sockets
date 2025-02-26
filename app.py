from flask import Flask, render_template, jsonify, request
import socket
import threading
import json

app = Flask(__name__)

# Almacenar datos de los clientes en un diccionario
devices_data = {}

def save_data():
    """Guarda los datos en un archivo JSON"""
    print(f"Guardando datos en data.json: {devices_data}")  # 🔹 Verificar antes de guardar
    with open("data.json", "w") as file:
        json.dump(devices_data, file, indent=4)
        print("Contenido actual de data.json:", json.dumps(devices_data, indent=4))

def handle_client(client_socket):
    """Maneja la conexión de un cliente y recibe sus datos."""
    try:
        data = client_socket.recv(4096).decode('utf-8')
        print(f"Datos recibidos: {data}")  # 🔹 Ver si el servidor está recibiendo información
        
        if data:
            storage_info = json.loads(data)  # Convertir JSON a diccionario
            device_name = storage_info[0]['device_name']
            devices_data[device_name] = storage_info
            save_data()
            print(f"Datos guardados para {device_name}: {storage_info}")  
    except Exception as e:
        print(f"Error recibiendo datos: {e}")
    finally:
        client_socket.close()

def start_server():
    """Inicia el servidor para recibir datos de los clientes."""
    server_ip = "0.0.0.0"
    server_port = 12123

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 🔹 Permitir reutilizar el puerto
    server_socket.bind((server_ip, server_port))
    server_socket.listen(5)
    print(f"Servidor escuchando en {server_ip}:{server_port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            print(f"Conexión establecida con {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except Exception as e:
        print(f"Error en el servidor de sockets: {e}")
    finally:
        server_socket.close()  # 🔹 Asegurar que el socket se cierre cuando se detenga


@app.route('/')
def index():
    """Muestra la página web con la información consolidada."""
    print("Cargando index.html")
    return render_template('index.html', devices_data=devices_data)

@app.route('/data')
def get_data():
    """Devuelve los datos en formato JSON para la web."""
    return jsonify(devices_data)

try:
    with open("data.json", "r") as file:
        devices_data = json.load(file)  # Cargar datos previos si existen
except (FileNotFoundError, json.decoder.JSONDecodeError):
    devices_data = {}  # Inicializar como diccionario vacío si no hay datos previos

@app.route('/receive_data', methods=['POST'])
def receive_data():
    global devices_data  # Indicar que usaremos la variable global

    try:
        data = request.get_json()
        print("Datos recibidos:", data)

        # Agrupar por device_name
        for entry in data:
            device_id = entry["device_name"]
            if device_id not in devices_data:
                devices_data[device_id] = []
            devices_data[device_id].append(entry)

        # Guardar en data.json
        save_data()
        return jsonify({"message": "Datos guardados exitosamente"}), 200

    except Exception as e:
        print("Error recibiendo datos:", str(e))
        return jsonify({"error": "Error procesando datos"}), 500

if __name__ == '__main__':
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
