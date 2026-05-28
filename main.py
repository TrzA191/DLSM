import cv2 as cv
import time
import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Inicializar el reconocedor de voz
recognizer = sr.Recognizer()
# Inicializar el motor de síntesis de voz
engine = pyttsx3.init()

Conf_threshold = 0.70
NMS_threshold = 0.4
COLORS = [(0, 255, 0), (0, 0, 255), (255, 0, 0),
        (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# La carpeta de recursos está en el mismo directorio del proyecto
PROJECT_DATA_DIR = 'Detector LSM Python'

class_name = []
with open(os.path.join(PROJECT_DATA_DIR, 'clases.txt'), 'r') as f:
    class_name = [cname.strip() for cname in f.readlines()]

net = cv.dnn.readNet(os.path.join(PROJECT_DATA_DIR, 'LSM.weights'), os.path.join(PROJECT_DATA_DIR, 'LSM.cfg'))
# Forzar uso de CPU para evitar errores si OpenCV no tiene build con CUDA
try:
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_DEFAULT)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
except Exception:
    pass

# Inicializar variable para almacenar el texto detectado
texto_detectado = ""

# Crear el modelo de detección
model = cv.dnn_DetectionModel(net)
model.setInputParams(size=(416, 416), scale=1/255, swapRB=True)

cap = cv.VideoCapture(0)
starting_time = time.time()
frame_counter = 0  # Definir frame_counter como global

# Inicializar el interruptor de audio
audio_activado = True

# Función para encender o apagar la cámara
def toggle_camera():
    global cap
    if cap.isOpened():
        cap.release()
        camera_button.config(text="Encender Cámara")
    else:
        cap = cv.VideoCapture(0)
        camera_button.config(text="Apagar Cámara")

# Función para encender o apagar el audio
def toggle_audio():
    global audio_activado
    audio_activado = not audio_activado
    if audio_activado:
        audio_button.config(text="Apagar Sonido")
    else:
        audio_button.config(text="Encender Sonido")

# Función para guardar los registros
def save_records():
    with open("registros.txt", "a") as f:
        f.write(texto_detectado + "\n")

# Función para terminar el programa
def exit_program():
    cap.release()
    cv.destroyAllWindows()
    root.quit()

# Crear la ventana principal
root = tk.Tk()
root.title("Detector LSM - Interfaz de Control")

# Crear el marco principal
main_frame = ttk.Frame(root)
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Columna 1
column1_frame = ttk.Frame(main_frame, width=15)
column1_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
column1_frame.rowconfigure(0, weight=1)
column1_frame.rowconfigure(1, weight=1)
column1_frame.rowconfigure(2, weight=1)
column1_frame.rowconfigure(3, weight=1)

camera_button = ttk.Button(column1_frame, text="Apagar Cámara", command=toggle_camera)
camera_button.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

audio_button = ttk.Button(column1_frame, text="Apagar Sonido", command=toggle_audio)
audio_button.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

save_button = ttk.Button(column1_frame, text="Guardar Registros", command=save_records)
save_button.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

exit_button = ttk.Button(column1_frame, text="Salir", command=exit_program)
exit_button.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

# Columna 2
column2_frame = ttk.Frame(main_frame)
column2_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
column2_frame.columnconfigure(0, weight=1)
column2_frame.columnconfigure(1, weight=4)
column2_frame.rowconfigure(0, weight=8)
column2_frame.rowconfigure(1, weight=2)

video_label = ttk.Label(column2_frame)
video_label.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

letter_label = ttk.Label(column2_frame, text="Letra detectada:")
letter_label.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)

root.protocol("WM_DELETE_WINDOW", exit_program)

# Iniciar el bucle de vídeo
def video_loop():
    global frame_counter, texto_detectado  # Declarar frame_counter y texto_detectado como globales
    ret, frame = cap.read()
    if ret:
        frame_counter += 1
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)  # Convertir el frame a RGB

        # Aplicar el modelo de detección al frame
        classes, scores, boxes = model.detect(frame, Conf_threshold, NMS_threshold)
        for idx, (classid, score, box) in enumerate(zip(classes, scores, boxes)):
            color = COLORS[int(classid) % len(COLORS)]  # Usar classid directamente como índice
            label = "%s : %f" % (class_name[classid], score)  # Utilizar classid directamente como índice
            cv.rectangle(frame, box, color, 2)
            cv.putText(frame, label, (box[0], box[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
            # Obtener la letra detectada
            LL = class_name[classid]
            texto_detectado = LL

            # Configurar la etiqueta con la letra detectada
            letter_label.config(text="Letra detectada: " + LL)

            # Reproducir la letra detectada solo si el audio está activado
            if audio_activado:
                engine.say(LL)
                engine.setProperty('rate', 110)  # Disminuir la velocidad
                voices = engine.getProperty('voices')
                engine.setProperty('voice', 'desired_voice_id')
                engine.runAndWait()

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
    root.after(10, video_loop)  # Llamar a video_loop nuevamente después de 10 ms

# Llamar a video_loop después de que root ha sido definido
root.after(1, video_loop)

# Ejecutar la aplicación
root.mainloop()