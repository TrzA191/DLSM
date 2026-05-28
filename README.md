# Detector de Lengua de Señas Mexicana (LSM) en Tiempo Real

Este proyecto consiste en un sistema de visión artificial en tiempo real capaz de detectar e interpretar letras de la **Lengua de Señas Mexicana (LSM)** utilizando la cámara web. Está diseñado para facilitar la comunicación inclusiva traduciendo señas visuales en texto y audio de manera instantánea.

## 🚀 Características Principales

* **Detección en Tiempo Real:** Captura el flujo de video de la cámara web a altos cuadros por segundo (FPS) y detecta las señas de forma continua.
* **Modelo de Redes Neuronales (YOLO):** Utiliza la arquitectura de detección de objetos YOLO cargada a través del módulo DNN de OpenCV (`LSM.weights` y `LSM.cfg`) para una localización y clasificación precisa.
* **Retroalimentación de Audio (Texto a Voz):** Integra síntesis de voz mediante la librería `pyttsx3` para reproducir auditivamente la letra o seña detectada en tiempo real.
* **Panel de Control Interactivo:** Interfaz gráfica intuitiva desarrollada en Tkinter que permite:
  * **Encender/Apagar Cámara:** Pausar o reanudar el flujo de video en cualquier momento.
  * **Activar/Desactivar Sonido:** Habilitar o silenciar la reproducción por voz de las señas detectadas.
  * **Guardar Registros:** Registrar el texto de las señas detectadas en un archivo histórico (`registros.txt`).
  * **Control de FPS:** Muestra el rendimiento del modelo en tiempo real en la pantalla.

> [!NOTE]
> **Limitación de detección:** El modelo está diseñado principalmente para la identificación de señas estáticas. Aquellas letras que requieren movimiento dinámico para su representación en LSM (como por ejemplo la **J**) no son identificadas por el sistema en esta etapa.

---

## 🛠️ Requisitos del Sistema

* **Python 3.10 o superior**
* **Cámara web integrada o externa**

### Librerías Requeridas
* **`opencv-python`** (Procesamiento de imagen y ejecución de la red neuronal)
* **`numpy`** (Operaciones de matrices numéricas)
* **`pillow`** (Manipulación e integración de imágenes en la interfaz gráfica)
* **`pyttsx3`** (Motor de síntesis de voz de texto a audio)
* **`SpeechRecognition`** (Inicialización del motor de voz)

---

## 💻 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/DLSM.git
   cd DLSM
   ```

2. **Crear y activar un entorno virtual:**
   ```powershell
   python -m venv .venv
   # En Windows (PowerShell):
   .\.venv\Scripts\activate
   ```

3. **Instalar las dependencias:**
   ```bash
   python -m pip install opencv-python SpeechRecognition pyttsx3 numpy pillow
   ```

4. **Archivos del modelo requeridos:**
   Asegúrate de que los archivos del modelo estén ubicados en la carpeta `Detector LSM Python/`:
   * `clases.txt` (Listado con los nombres de las letras/señas en orden).
   * `LSM.cfg` (Configuración de la red neuronal).
   * `LSM.weights` (Pesos entrenados del modelo YOLO).
     > [!IMPORTANT]
     > **Descarga de Pesos:** Dado que el archivo `LSM.weights` pesa más de 250 MB, está excluido de este repositorio de GitHub. Debes descargarlo desde **[INGRESA AQUÍ EL ENLACE A TU NUBE]** e introducir el archivo directamente dentro de la carpeta `Detector LSM Python/` antes de ejecutar la aplicación.

---

## ⏱️ Ejecución del Detector

Para iniciar la interfaz del detector de lengua de señas, ejecuta el siguiente comando en tu terminal con el entorno virtual activo:

```bash
python main.py
```

---

## 📁 Estructura del Proyecto

```text
├── main.py               # Script ejecutable principal (lógica del detector e interfaz de control).
├── PROCESO_ENTRENAMIENTO.md # Documentación detallada de recopilación, etiquetado y entrenamiento del modelo.
├── Detector LSM Python/
│   ├── clases.txt        # Definición de las clases y letras del abecedario LSM.
│   ├── LSM.cfg           # Configuración del modelo YOLO.
│   └── LSM.weights       # Pesos entrenados del modelo.
├── registros.txt         # Historial donde se guardan las señas traducidas.
└── README.md             # Documentación general del proyecto.
```
