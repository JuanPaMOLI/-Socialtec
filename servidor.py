import socket
import threading
import sqlite3
from passlib.hash import bcrypt

# Base de datos local para usuarios
DATABASE = "usuarios_server.db"

# Crear base de datos y tabla si no existen
def init_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Registrar un nuevo usuario
def register_user(username, password):
    hashed_password = bcrypt.hash(password)  # Cifrar la contraseña con Passlib
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return "Usuario registrado exitosamente."
    except sqlite3.IntegrityError:
        return "Error: El usuario ya existe."
    finally:
        conn.close()

# Validar inicio de sesión
def validate_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usuarios WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        stored_password = result[0]
        if bcrypt.verify(password, stored_password):  # Comparar la contraseña ingresada con la cifrada
            return "Inicio de sesión exitoso."
    return "Error: Usuario o contraseña incorrectos."

# Manejo de clientes
def handle_client(client_socket):
    print("[NUEVO CLIENTE] Conexión establecida")
    while True:
        try:
            data = client_socket.recv(1024).decode("utf-8").strip()
            if not data:
                break

            print(f"[COMANDO RECIBIDO] {data}")
            command_parts = data.split()
            if len(command_parts) < 1:
                client_socket.send("Error: Comando vacío.".encode("utf-8"))
                continue

            command = command_parts[0].upper()
            args = command_parts[1:]

            if command == "REGISTER":
                if len(args) != 2:
                    response = "Error: Uso correcto: REGISTER <usuario> <contraseña>"
                else:
                    response = register_user(args[0], args[1])
            elif command == "LOGIN":
                if len(args) != 2:
                    response = "Error: Uso correcto: LOGIN <usuario> <contraseña>"
                else:
                    response = validate_user(args[0], args[1])
            else:
                response = "Error: Comando no reconocido."

            client_socket.send(response.encode("utf-8"))
        except Exception as e:
            print(f"[ERROR] {e}")
            break

    print("[CLIENTE DESCONECTADO]")
    client_socket.close()

# Servidor principal
def start_server():
    init_database()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5000))
    server.listen(5)
    print("[SERVIDOR] Esperando conexiones en 127.0.0.1:5000")

    while True:
        client_socket, client_address = server.accept()
        print(f"[CONEXIÓN ESTABLECIDA] Cliente conectado desde {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
