import socket
import threading
import tkinter as tk
from tkinter import messagebox
import sqlite3
from passlib.hash import bcrypt
import redsocial  # Importamos el archivo redsocial.py

# Base de datos local para usuarios
DATABASE = "usuarios.db"


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

# Guardar un nuevo usuario en la base de datos
def save_user(username, password):
    hashed_password = bcrypt.hash(password)
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # El usuario ya existe
    finally:
        conn.close()

# Validar usuario y contraseña en la base de datos
def validate_user(sock, username, password):
    send_str = "LOGIN " + username + " " + password
    sock.send(send_str.encode())
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print(data.decode())
        if data.decode() == "Inicio de sesión exitoso.":
            return True
        elif data.decode() == "Error: Usuario o contraseña incorrectos":
            return False
     

# Clase para la interfaz gráfica del cliente
class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("InstaFace - Cliente")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")

        # Socket
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(("localhost", 8567))


        # Pantalla de inicio
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="InstaFace", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#1d3557").pack(pady=20)

        tk.Label(self.root, text="Usuario:", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show="*", width=25)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Iniciar Sesión", font=("Arial", 12), bg="#457b9d", fg="white", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Registrarse", font=("Arial", 12), bg="#1d3557", fg="white", command=self.show_register_screen).pack()

    def show_register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="InstaFace - Registro", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#1d3557").pack(pady=20)

        tk.Label(self.root, text="Usuario:", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Contraseña:", font=("Arial", 14), bg="#f0f0f0").pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), show="*", width=25)
        self.password_entry.pack(pady=5)

        tk.Button(self.root, text="Registrar", font=("Arial", 12), bg="#457b9d", fg="white", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Volver", font=("Arial", 12), bg="#1d3557", fg="white", command=self.show_login_screen).pack()

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if save_user(username, password):
            messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
            self.show_login_screen()
        else:
            messagebox.showerror("Error", "El usuario ya existe.")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        sock = self.client

        if not username or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if validate_user(sock, username, password):
            self.open_social_network()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

    def open_social_network(self):
        self.root.destroy()  # Cierra la ventana principal
        redsocial.start_app()  # Llama a la función principal en red_social.py

# Inicializar base de datos y ejecutar la app
if __name__ == "__main__":
    init_database()
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()
