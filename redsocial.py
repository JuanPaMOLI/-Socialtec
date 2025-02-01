import tkinter as tk
from tkinter import PhotoImage

class User_Profile:

    def open_user_profile(root):
        # Header bar
        header = tk.Frame(root, bg="#4267B2", height=80)
        header.pack(fill="x")

        tk.Label(header, text="InstaFace", font=("Arial", 24, "bold"), bg="#4267B2", fg="white").pack(side="left", padx=20, pady=10)

        tk.Button(header, text="Inicio", font=("Arial", 12), bg="#4e8ef7", fg="white", bd=0).pack(side="right", padx=10)
        tk.Button(header, text="Salir", font=("Arial", 12), bg="#e63946", fg="white", bd=0, command=root.quit).pack(side="right", padx=10)

        tk.Button(header, text="buscar", font=("Arial", 12), bg="#4e8ef7", fg="white", bd=0).pack(padx=10, pady=10, side="right")
        search_entry = tk.Entry(header).pack(padx=10, pady=20)

        # Profile section
        profile_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
        profile_frame.pack(pady=20, padx=50, fill="x")

        # Profile picture placeholder
        profile_picture = PhotoImage(width=100, height=100)  # Placeholder image
        tk.Label(profile_frame, image=profile_picture, bg="white").grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # User info
        tk.Label(profile_frame, text="Nombre del Usuario", font=("Arial", 16, "bold"), bg="white").grid(row=0, column=1, sticky="w")
        tk.Label(profile_frame, text="Ciudad: San José, Costa Rica", font=("Arial", 12), bg="white").grid(row=1, column=1, sticky="w")

        # Content section
        content_frame = tk.Frame(root, bg="white", bd=1, relief="solid")
        content_frame.pack(pady=10, padx=50, fill="both", expand=True)

        tk.Label(content_frame, text="Publicaciones", font=("Arial", 16, "bold"), bg="white").pack(anchor="w", padx=10, pady=10)

        # Example post
        post_frame = tk.Frame(content_frame, bg="white", bd=1, relief="solid")
        post_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(post_frame, text="Nombre del Usuario", font=("Arial", 12, "bold"), bg="white", fg="#4267B2").pack(anchor="w", padx=10, pady=5)
        tk.Label(post_frame, text="Esto es un ejemplo de publicación en tu perfil de InstaFace.", font=("Arial", 12), bg="white", wraplength=700, justify="left").pack(anchor="w", padx=10, pady=5)

        # Footer
        footer = tk.Frame(root, bg="#f7f7f7", height=50)
        footer.pack(fill="x", side="bottom")

        tk.Label(footer, text="© 2025 InstaFace", font=("Arial", 10), bg="#f7f7f7", fg="gray").pack(pady=10)


def start_app():
    root = tk.Tk()
    root.title("InstaFace - Perfil de Usuario")
    root.geometry("800x600")
    root.configure(bg="#e9ebee")

    profile1 = User_Profile
    profile1.open_user_profile(root)

    root.mainloop()

if __name__ == "__main__":
    start_app()
