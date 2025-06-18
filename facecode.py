from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox
import cv2
import numpy as np
import os
import pickle
import time
import tkinter as tk
from tkinter import PhotoImage
import RPi.GPIO as GPIO

# Credenciales de administrador
ADMIN_USER = "admin"
ADMIN_PASS = "admin"

# Configuración del GPIO para el relé
relay = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay, GPIO.OUT)
GPIO.output(relay, 1)

# Cargar el clasificador Haar Cascade
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# Configurar el recognizer para reconocimiento facial
recognizer = cv2.face.LBPHFaceRecognizer_create()

# Crear el directorio "dataset" si no existe
os.makedirs('dataset', exist_ok=True)

# Crear el archivo del reporte si no existe
REPORTE_PATH = 'reporte_accesos.txt'
if not os.path.exists(REPORTE_PATH):
    with open(REPORTE_PATH, 'w') as f:
        f.write("Registro de Accesos\n\n")

# Función para registrar el acceso en el archivo de reporte
def registrar_acceso(nombre):
    with open(REPORTE_PATH, 'a') as f:
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{hora} - {nombre}\n")

# Función para descargar el reporte con autenticación
def descargar_reporte():
    def validar_credenciales(user, password):
        return user == ADMIN_USER and password == ADMIN_PASS

    # Crear una ventana de diálogo para las credenciales
    dialog = tk.Toplevel()
    dialog.title("Autenticación")
    dialog.geometry("300x150")
    
    # Campos de entrada
    tk.Label(dialog, text="Usuario:").pack(pady=5)
    user_entry = tk.Entry(dialog)
    user_entry.pack(pady=5)
    
    tk.Label(dialog, text="Contraseña:").pack(pady=5)
    pass_entry = tk.Entry(dialog, show="*")
    pass_entry.pack(pady=5)
    
    def verificar():
        if validar_credenciales(user_entry.get(), pass_entry.get()):
            dialog.destroy()
            # Generar nombre de archivo con timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f'reporte_accesos_{timestamp}.txt'
            
            # Copiar el contenido del reporte al nuevo archivo
            with open(REPORTE_PATH, 'r') as fuente:
                with open(nombre_archivo, 'w') as destino:
                    destino.write(fuente.read())
            messagebox.showinfo("Éxito", f"Reporte guardado como: {nombre_archivo}")
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            
    tk.Button(dialog, text="Aceptar", command=verificar).pack(pady=10)

# Función para registrar nuevo usuario con autenticación
def registrar_usuario():
    def validar_credenciales(user, password):
        return user == ADMIN_USER and password == ADMIN_PASS

    # Crear una ventana de diálogo para las credenciales
    dialog = tk.Toplevel()
    dialog.title("Autenticación")
    dialog.geometry("300x150")
    
    tk.Label(dialog, text="Usuario:").pack(pady=5)
    user_entry = tk.Entry(dialog)
    user_entry.pack(pady=5)
    
    tk.Label(dialog, text="Contraseña:").pack(pady=5)
    pass_entry = tk.Entry(dialog, show="*")
    pass_entry.pack(pady=5)
    
    def verificar():
        if validar_credenciales(user_entry.get(), pass_entry.get()):
            dialog.destroy()
            realizar_registro()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")
            
    tk.Button(dialog, text="Aceptar", command=verificar).pack(pady=10)

def realizar_registro():
    # Crear una ventana de diálogo para los datos del usuario
    dialog = tk.Toplevel()
    dialog.title("Registro de Usuario")
    dialog.geometry("300x150")
    
    tk.Label(dialog, text="Nombre:").pack(pady=5)
    nombre_entry = tk.Entry(dialog)
    nombre_entry.pack(pady=5)
    
    tk.Label(dialog, text="Apellido:").pack(pady=5)
    apellido_entry = tk.Entry(dialog)
    apellido_entry.pack(pady=5)
    
    def iniciar_captura():
        nombre = nombre_entry.get()
        apellido = apellido_entry.get()
        dialog.destroy()
        
        if nombre and apellido:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                messagebox.showerror("Error", "No se pudo abrir la cámara")
                return

            cv2.namedWindow('Registro de Rostros')
            start_time = time.time()
            image_count = 0
            
            try:
                while image_count < 30:
                    ret, frame = cap.read()
                    if time.time() - start_time > 60:  # Tiempo límite de 1 minuto
                        messagebox.showwarning("Tiempo agotado", "No se completó el registro en el tiempo límite")
                        break
                        
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        img_name = f'dataset/{nombre}_{apellido}_{image_count + 1}.png'
                        cv2.imwrite(img_name, frame[y:y + h, x:x + w])
                        image_count += 1
                        if image_count >= 30:
                            break

                    cv2.imshow('Registro de Rostros', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break

            finally:
                cap.release()
                cv2.destroyAllWindows()
                if image_count >= 30:
                    messagebox.showinfo("Registro", f"Usuario {nombre} {apellido} registrado exitosamente")
                else:
                    messagebox.showwarning("Registro incompleto", "No se completó el registro de imágenes")
    
    tk.Button(dialog, text="Iniciar Captura", command=iniciar_captura).pack(pady=10)

# Función para reconocimiento facial y apertura de la puerta
def reconocer_usuario():
    try:
        recognizer.read('trainer.yml')
        with open("names.pkl", "rb") as f:
            names = pickle.load(f)
    except FileNotFoundError:
        messagebox.showerror("Error", "Modelo no entrenado o archivo de nombres no encontrado")
        return

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        messagebox.showerror("Error", "No se pudo abrir la cámara")
        return 

    cv2.namedWindow('Reconocimiento Facial')
    user_recognized = False
    start_time = time.time()

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        # Verificar tiempo límite
        if time.time() - start_time > 60:  # 60 segundos = 1 minuto
            messagebox.showinfo("Tiempo agotado", "No se detectó ningún rostro en el tiempo límite")
            break

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if confidence > 30:
                name = names[id]
                name_parts = name.split('_')
                clean_name = ' '.join(name_parts[:2])

                # Registrar el acceso
                registrar_acceso(clean_name)
                GPIO.output(relay, 0)
                time.sleep(1)
                GPIO.output(relay, 1)

                user_recognized = True
                break

            cv2.putText(img, name if confidence > 30 else "Desconocido", 
                       (x + 5, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Reconocimiento Facial', img)

        if user_recognized:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Sistema de Reconocimiento Facial")
ventana.configure(background='white')

icono = PhotoImage(file='facial.png')
ventana.iconphoto(True, icono)

# Crear una barra de menú
menu_bar = tk.Menu(ventana)
ventana.config(menu=menu_bar)

# Crear un menú desplegable de opciones
opciones_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Opciones", menu=opciones_menu)

opciones_menu.add_command(label="Nuevo Usuario", command=registrar_usuario)
opciones_menu.add_command(label="Reporte", command=descargar_reporte)
opciones_menu.add_command(label="Entrenar", command=entrenar_modelo)

# Configurar la ventana para pantalla completa
ventana.attributes("-fullscreen", True)

# Botón para reconocimiento facial
btn_reconocer = tk.Button(ventana, text="Abrir Puerta", command=reconocer_usuario, 
                         font=("Arial", 20), width=30, height=2)
btn_reconocer.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# Texto al pie de página
texto_desarrollo = tk.Label(ventana, text="\u00A9 2024 Todos los derechos reservados", 
                          font=("Arial", 8), anchor="se")
texto_desarrollo.pack(side="bottom", anchor="e", padx=10, pady=5)
texto_desarrollo.config(bg=ventana.cget("bg"))

# Función para salir del modo pantalla completa presionando "Esc"
def salir_pantalla_completa(event):
    ventana.attributes("-fullscreen", False)

ventana.bind("<Escape>", salir_pantalla_completa)

ventana.mainloop()
