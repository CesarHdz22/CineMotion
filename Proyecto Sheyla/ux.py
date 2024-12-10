import customtkinter as ctk  
from PIL import Image, ImageTk
from tkinter import messagebox
import tkinter as tk
from db_connection import get_collection
import sys

sys.stdout.reconfigure(encoding='utf-8')

emotion_to_genres = {}

collection = get_collection('train')
data = list(collection.find())

for item in data:
    emotion = item['emocion']
    genres = item['generos']
    emotion_to_genres[emotion] = genres

genre_to_id = {}
dictionary_collection = get_collection('Diccionario')
dictionary_data = list(dictionary_collection.find())

for item in dictionary_data:
    genre_to_id[item['nombre']] = item['_id']    

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

#Convierte los ides de los géneros a sus nombres
def get_genre_mapping():
    try:
        dictionary_collection = get_collection("Diccionario")
        genres = dictionary_collection.find()
        return {str(genre["_id"]): genre["nombre"] for genre in genres}
    except Exception as e:
        print(f"Error al obtener el mapeo de géneros: {e}")
        return {}

#Extrae todas las películas de la base de datos
def get_all_movies():
    try:
        movies_collection = get_collection("Peliculas")
        
        movies = list(movies_collection.find())
        return movies
    except Exception as e:
        print(f"Error al obtener los datos de las películas: {e}")
        return []

#Da las imagenes de los botones
def load_and_resize_image(filepath, width, height):
    try:
        pil_img = Image.open(filepath).convert("RGBA")  
        pil_img = pil_img.resize((width, height), Image.Resampling.LANCZOS)  
        img_tk = ImageTk.PhotoImage(pil_img)
        return img_tk
    except FileNotFoundError:
        messagebox.showerror("Error", f"No se encontró la imagen: {filepath}")
        return None

#Crea el login
def create_login_window():
    login_window = ctk.CTk()
    login_window.title("Login - CINEMOTION")
    login_window.geometry("370x600")
    login_window.configure(fg_color="#aee3fa")


    logo_path = "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/logo3.png"  
    logo_image = load_and_resize_image(logo_path, 660,400)  
    if logo_image:
        logo_label = ctk.CTkLabel(login_window, image=logo_image, text="")  
        logo_label.image = logo_image 
        logo_label.pack(pady=10)

    user_entry = ctk.CTkEntry(login_window, placeholder_text="Usuario", height=40, border_color="#3796b0")
    user_entry.pack(pady=10, padx=30)

    password_entry = ctk.CTkEntry(login_window, placeholder_text="Contraseña", show="*", height=40, border_color="#3796b0")
    password_entry.pack(pady=10, padx=30)
    #Aqui se hace la consulta en mongo
    def submit_login():
        user = user_entry.get()
        password = password_entry.get()
        
        if user and password:
            users_collection = get_collection("usuarios")
            existing_user = users_collection.find_one({"username": user, "contrasena": password})
            
            if existing_user:
                messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso")
                login_window.destroy()
                create_main_window()
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
        else:
            messagebox.showwarning("Error", "Por favor, completa todos los campos.")
    
    def open_register_window():
        login_window.destroy()
        create_register_window()

    ctk.CTkButton(
        login_window, text="Iniciar Sesión", 
        fg_color="#48cbef", hover_color="#3796b0", 
        text_color="white", font=("Arial", 16),
        command=submit_login, height=40
    ).pack(pady=20, padx=30)

    ctk.CTkButton(
        login_window, text="Registrar", 
        fg_color="#aee3fa", hover_color="#48cbef", 
        text_color="#034efc", font=("Arial", 14), 
        command=open_register_window, height=35
    ).pack(pady=10)

    login_window.mainloop()


#La otra opcion, por si lo que hara es registrarse
def create_register_window():
    register_window = ctk.CTk()
    register_window.title("Registro - CINEMOTION")
    register_window.geometry("400x600")
    register_window.configure(fg_color="#aee3fa")

    ctk.CTkLabel(register_window, text="CINEMOTION", font=("coolvetica", 28, "bold"), text_color="#034efc").pack(pady=5)
    ctk.CTkLabel(register_window, text="Registro de Usuario", font=("Arial", 18), text_color="#034efc").pack(pady=5)

    frame = ctk.CTkFrame(register_window, fg_color="white", corner_radius=15)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    fields = {
        "Nombre": ctk.CTkEntry(frame, placeholder_text="Ingresa tu nombre"),
        "Apellido Paterno": ctk.CTkEntry(frame, placeholder_text="Ingresa tu apellido paterno"),
        "Apellido Materno": ctk.CTkEntry(frame, placeholder_text="Ingresa tu apellido materno"),
        "Correo Electrónico": ctk.CTkEntry(frame, placeholder_text="Ingresa tu correo electrónico"),
        "Teléfono": ctk.CTkEntry(frame, placeholder_text="Ingresa tu número de teléfono"),
        "Nombre de Usuario": ctk.CTkEntry(frame, placeholder_text="Crea un nombre de usuario"),
        "Contraseña": ctk.CTkEntry(frame, placeholder_text="Crea una contraseña", show="*"),
    }

    for field, entry in fields.items():
        ctk.CTkLabel(frame, text=f"{field}:", text_color="#aee3fa").pack(pady=5)
        entry.pack(pady=5, padx=10)
    #Se manda la data del usuario a la bd
    def register_user():
        for field, entry in fields.items():
            if not entry.get():
                messagebox.showerror("Error", f"El campo '{field}' es obligatorio.")
                return

        user_data = {
            "nombre": fields["Nombre"].get(),
            "a_pat": fields["Apellido Paterno"].get(),
            "a_mat": fields["Apellido Materno"].get(),
            "correo": fields["Correo Electrónico"].get(),
            "telefono": fields["Teléfono"].get(),
            "username": fields["Nombre de Usuario"].get(),
            "contrasena": fields["Contraseña"].get(),
        }

        users_collection = get_collection("usuarios")
        
        if users_collection.find_one({"username": user_data["username"]}):
            messagebox.showerror("Error", "El nombre de usuario ya está en uso. Elige otro.")
            return

        try:
            users_collection.insert_one(user_data)
            messagebox.showinfo("Registro", "Registro exitoso. Ahora puedes iniciar sesión.")
            register_window.destroy()
            create_login_window()
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un problema al registrar al usuario: {e}")

    ctk.CTkButton(register_window, text="Registrar", command=register_user).pack(pady=20)

    register_window.mainloop()
    
    ctk.CTkButton(
        frame, text="Registrar", 
        fg_color="#48cbef", hover_color="#3796b0", 
        text_color="white", font=("Arial", 16), 
        command=register_user, height=40
    ).pack(pady=20, padx=10)

    #Regresa a login
    def back_to_login():
        register_window.destroy()
        create_login_window()

    ctk.CTkButton(
        frame, text="Volver al Inicio de Sesión", 
        fg_color="#aee3fa", hover_color="#48cbef", 
        text_color="#034efc", font=("Arial", 14), 
        command=back_to_login, height=35
    ).pack(pady=5, padx=10)

    register_window.mainloop()
#Hace la prediccion de los generos
def predict_genres(emotion):
    genres = emotion_to_genres.get(emotion, [])
    return genres

#Da la recomendacion
def handle_emotion(emotion):
    genres = predict_genres(emotion)
    if not genres:
        messagebox.showerror("Error", f"No se encontraron géneros para la emoción '{emotion}'.")
        return
    
    messagebox.showinfo("Predicción de Géneros", f"Para la emoción '{emotion}', los géneros recomendados son: {genres}")

#Crea las cartitas con la informacion
def create_movie_card(movie, parent, row, column):
    card = ctk.CTkFrame(parent, width=500, height=700, fg_color="#e0f7fa", corner_radius=20) 
    card.grid_propagate(False) 
    card.grid(row=row, column=column, padx=10, pady=10)

    ctk.CTkLabel(card, text=movie['Titulo'], font=("Arial", 12, "bold"), text_color="black").pack(pady=5)
    ctk.CTkLabel(card, text=f"Fecha de lanzamiento: {movie['Fecha de lanzamiento']}",justify="left", text_color="black").pack(pady=3)
    ctk.CTkLabel(card, text=f"Calificación: {movie['Calificación']} ☆",justify="left", text_color="black").pack(pady=3)
    ctk.CTkLabel(card, text=f"Géneros: {movie['Géneros']}", justify="left", text_color="black").pack(pady=3)
    ctk.CTkLabel(card, text=movie['Resumen'], wraplength=200, justify="left", text_color="black").pack(pady=5) 


# Ventana Principal con Carrusel y Botones
def create_main_window():

    main_window = ctk.CTk()
    main_window.title("CINEMOTION")
    main_window.geometry("1045x600")
    main_window.configure(fg_color="#b7eeff")

    logo_path = "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/logo2.png"  # ruta del logo
    logo_image = load_and_resize_image(logo_path, 800,170)  
    if logo_image:
        logo_label = ctk.CTkLabel(main_window, image=logo_image, text="")  
        logo_label.image = logo_image 
        logo_label.pack(pady=10)

        #campos de texto:
        
    text_frame = ctk.CTkFrame(main_window, fg_color="white", corner_radius=10) 
    text_frame.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(
        text_frame,
        text=(
            "Cinemotion es una plataforma interactiva única que une tus emociones con el universo del cine. "
            " Una vez seleccionada la emoción, Cinemotion analiza tu elección y te recomienda una lista personalizada"
            " de películas que encajan perfectamente con tu estado de ánimo. ¿Estás alegre? Te sugeriremos comedias"
            " vibrantes y películas inspiradoras. ¿Te encuentras Nostálgico? Encuentra dramas conmovedores que te acompañen en ese momento."
        ),
        wraplength=1280,  
        justify="left", 
        font=("creatodisplay-medium", 18),
        text_color="black", 
    ).pack(pady=10, padx=10) 



    buttons_frame = ctk.CTkFrame(main_window, fg_color="white")
    buttons_frame.pack(fill="x", pady=10)

    # aqui se debe cargar las imagenes de los botones
    buttons_images = {
    "Feliz": "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/feliz.png",
    "Serio": "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/serio.png",
    "Nostalgia": "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/nostalgia.png",
    "Preocupado": "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/preocu.png",
    "Enojado": "C:/Users/cesar/OneDrive/Escritorio/Proyectos/Proyecto Sheyla/img/enojado.png",
}
    
    center_frame = tk.Frame(buttons_frame, bg="white")
    center_frame.pack(anchor="center")  

    for emotion, filepath in buttons_images.items():
        img = load_and_resize_image(filepath, 50,50)
        if img:  
            ctk.CTkButton(center_frame, image=img, text="", fg_color="#421a8c", hover_color="#2f1363", width=70, height=40,  command=lambda e=emotion: handle_emotion(e)).pack(side="left", padx=10)
        else:  
            ctk.CTkButton(center_frame, text=emotion, command=lambda e=emotion: handle_emotion(e)).pack(side="left", padx=10)
    #se crea el carrusel y se configura la barra desplazadora
    carousel_frame = ctk.CTkFrame(main_window, fg_color="white")
    carousel_frame.pack(fill="both", expand=True, padx=20, pady=20)

    canvas = tk.Canvas(carousel_frame, bg="#f0f0f0", highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew") 

    h_scrollbar = tk.Scrollbar(carousel_frame, orient="horizontal", command=canvas.xview)
    v_scrollbar = tk.Scrollbar(carousel_frame, orient="vertical", command=canvas.yview)

    h_scrollbar.grid(row=1, column=0, sticky="ew")  
    v_scrollbar.grid(row=0, column=1, sticky="ns") 

    canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

    carousel_frame.grid_rowconfigure(0, weight=1)
    carousel_frame.grid_columnconfigure(0, weight=1)

    scrollable_frame = tk.Frame(canvas, bg="white") 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    #Aqui se reelena el array que muestra la info de las peliculas
    genre_map = get_genre_mapping()
    peliculas = get_all_movies()
    movies = [
        {
            "Titulo": pelicula.get("titulo", "Título no disponible"),
            "Fecha de lanzamiento": pelicula.get("fecha_lanzamiento", "Fecha no disponible"),
            "Resumen": pelicula.get("resumen", "Resumen no disponible"),
            "Calificación": pelicula.get("puntuacion", "Calificación no disponible"),
            "Géneros": ", ".join(genre_map.get(str(g), f"ID no encontrado: {g}") for g in pelicula.get("generos", [])),
        }
        for pelicula in peliculas
    ]

    # aqui se crea las tarjetas dobles
    cards_per_row = len(movies) // 2 
    for i, movie in enumerate(movies):
        row = i // cards_per_row 
        column = i % cards_per_row 
        create_movie_card(movie, scrollable_frame, row=row, column=column)
    

    main_window.mainloop()

create_login_window()
