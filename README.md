¡Claro! Aquí tienes el contenido completo del `README.md`, listo para copiar y pegar en tu repositorio de GitHub:

---

````markdown
# 🔐 Sistema de Reconocimiento Facial para Apertura de Chapa Electromagnética

Bienvenido a este proyecto de **control de acceso inteligente**, desarrollado con **OpenCV**, **clasificador Haar Cascade**, y una interfaz gráfica en **Tkinter**. El sistema utiliza reconocimiento facial en tiempo real para identificar personas autorizadas y activar una **chapa electromagnética** mediante un **relé controlado por GPIO** (ideal para Raspberry Pi).

## 🚀 Características principales

- ✅ Reconocimiento facial en tiempo real con OpenCV  
- 🎯 Uso del clasificador Haar Cascade preentrenado  
- 🔓 Activación de relé para abrir la chapa electromagnética  
- 👤 Registro de usuarios autorizados  
- 🖥️ Interfaz gráfica simple con Tkinter  
- 📂 Registro de accesos con hora y nombre  


## 🧰 Tecnologías utilizadas

- Python
- OpenCV  
- Haar Cascade Classifier  
- Tkinter  
- GPIO (para control de relé)  
- PIL (para manipulación de imágenes)

## ⚙️ Requisitos

- Python 3.8
- Raspberry Pi 
- Librerías necesarias:

```bash
pip install opencv-python pillow
````

> Para Raspberry Pi:

```bash
sudo apt-get install python3-opencv
pip install RPi.GPIO
```

## 🛠️ Uso

1. **Clona este repositorio:**

```bash
git clone [https://github.com/tu-usuario/reconocimiento-facial-chapa.git](https://github.com/pdavicho/controlAccesoFR.git)
```

2. **Ejecuta el sistema:**

```bash
python faceCode.py
```

3. **Funciones disponibles:**

   * Registrar nuevo rostro
   * Reconocer rostro en vivo
   * Abrir chapa si la persona es reconocida
   * Visualizar historial de accesos

## 📁 Estructura del proyecto

```
📦 reconocimiento-facial-chapa
├── sistema_acceso.py
├── haarcascade_frontalface_default.xml
├── datos_rostros/
├── accesos.csv
├── assets/
└── README.md
```

## 🔐 Seguridad y privacidad

Este sistema **no transmite datos por internet** y todo el procesamiento se realiza **de manera local**. Las imágenes son almacenadas con fines de entrenamiento y se pueden eliminar o anonimizar fácilmente.

## 🤖 Créditos

Desarrollado por [David Minango]([https://github.com/tu-usuariohttps://github.com/pdavicho]).
Proyecto educativo / prototipo funcional para sistemas de control de acceso.

## 📜 Licencia

MIT License – libre de usar, modificar y distribuir con atribución.
