# Proceso de Recopilación, Etiquetado y Entrenamiento del Modelo LSM

Este documento detalla la metodología técnica y los pasos seguidos para la recolección del dataset, el proceso de etiquetado de imágenes, el aumento de datos (data augmentation) y el posterior entrenamiento de la red neuronal convolucional (YOLOv4) utilizada en el sistema de detección de la Lengua de Señas Mexicana (LSM).

---

## 📸 Fase 1: Recopilación del Dataset (Toma de Fotografías)

Para construir un modelo de detección robusto y generalizable, se llevó a cabo una campaña de recolección de fotografías bajo diversas condiciones ambientales.

* **Participantes:** Se contó con la colaboración de 4 personas con conocimientos en Lengua de Señas Mexicana, complementados con 3 integrantes del equipo de desarrollo, totalizando 7 personas participantes.
* **Variabilidad de Fondo:** Los colaboradores realizaron variaciones en la vestimenta (cambio en el color de blusas y camisas) y se ubicaron en diferentes locaciones físicas para capturar fondos heterogéneos y evitar que el modelo se memorizara un entorno específico.
* **Variación de Posturas:** Para cada una de las **27 letras** del abecedario, cada persona se tomó **5 fotografías**. En cada toma, se modificó levemente el ángulo, la posición de la mano y la distancia a la cámara, permitiendo capturar un rango amplio de inclinación y porcentaje de detección.
* **Volumen Base:** El dataset inicial cuenta con aproximadamente 810 imágenes de base (27 letras $\times$ 5 fotos por letra $\times$ 6-7 personas).

### Ejemplo de Captura de Imagen
![Ejemplo de fotografía recopilada](.github/assets/lsm_dataset_sample.jpg?v=2)

---

## 🏷️ Fase 2: Etiquetado del Dataset (LabelImg)

Una vez recopiladas las imágenes, se procedió a delimitar y etiquetar el área de interés (la mano del emisor realizando la seña).

* **Herramienta:** Se utilizó la herramienta de código abierto **LabelImg** en modo de anotación YOLO.
* **Metodología:** Se dibujó una caja de delimitación (bounding box) ajustada al contorno de la mano y se le asignó la etiqueta correspondiente a la letra representada.
* **Formato de Salida:** Por cada archivo de imagen, se generó un archivo de texto homónimo (`.txt`) que contiene la información de anotación estructurada bajo el estándar de YOLO, que consiste en las coordenadas normalizadas del objeto:
  
  `[id_clase] [centro_x] [centro_y] [ancho] [alto]`
  
  *Ejemplo de coordenada obtenida:*  
  `1 0.419271 0.429167 0.046875 0.173148`

### Capturas del Proceso de Etiquetado en LabelImg
![Interfaz de etiquetado en LabelImg - Vista 1](.github/assets/labelimg_sample_1.png?v=2)
![Interfaz de etiquetado en LabelImg - Vista 2](.github/assets/labelimg_sample_2.png?v=2)

---

## ⚙️ Fase 3: Aumento de Datos (Data Augmentation) con CLODSA

Para incrementar la cantidad de datos disponibles y mejorar la capacidad de generalización del modelo frente a cambios de iluminación, enfoque y orientación, se aplicaron técnicas de aumento de datos utilizando la librería especializada **CLODSA** dentro de la plataforma Google Colab.

### Técnicas de Aumentado Aplicadas:
1. **Volteos (Flips):** Volteos verticales, horizontales y combinados (espejo) para simular el uso de la mano izquierda o cambios en la orientación lateral.
2. **Rotación:** Rotación de imágenes en ángulos controlados (90 y 180 grados).
3. **Difuminado Medio (Average Blurring):** Aplicación de filtros de desenfoque (kernel de tamaño 5) para entrenar al modelo en condiciones de movimiento rápido o baja resolución.
4. **Modificación de Tonalidad y Contraste (Raise Hue):** Ajustes en el contraste y valor de tonalidad de la imagen (factor de potencia 0.9) para emular variaciones de iluminación natural y artificial.

Mediante este proceso lineal de transformaciones, el tamaño del dataset de entrenamiento fue multiplicado para dotar a la red neuronal de un espectro más amplio de aprendizaje.

---

## 🧠 Fase 4: Entrenamiento en Google Colab (YOLOv4)

El entrenamiento de la red neuronal convolucional profunda se realizó utilizando el framework **Darknet** configurado para **YOLOv4**.

### Configuración del Entorno de Entrenamiento:
* **Hardware:** Uso de aceleración por GPU (Graphics Processing Unit) en Google Colab para reducir el tiempo de cómputo en la propagación y retropropagación de la red.
* **Almacenamiento:** Integración y montaje del dataset de imágenes aumentadas desde Google Drive (`/content/drive/MyDrive`).
* **Configuración del Modelo (`LSM.cfg`):**
  * Configuración de la capa YOLO para clasificar las 27 señas correspondientes al abecedario.
  * Ajuste de filtros en las capas convolucionales inmediatamente anteriores a cada capa YOLO según la relación matemática para el formato YOLO: `filters = (clases + 5) * 3` (para 27 clases, el número de filtros configurado fue de 96).
  * Redimensionamiento de las dimensiones de entrada a la red a $416 \times 416$ píxeles.

### Monitorización y Resultados del Entrenamiento:
Durante la ejecución del entrenamiento en Google Colab, se monitorizó la curva de pérdida (loss) y el rendimiento en tiempo real. Asimismo, se realizaron predicciones de prueba directamente en el notebook para validar el correcto aprendizaje de la red neuronal sobre las señas de LSM.

A continuación se presentan capturas del proceso de entrenamiento y predicciones obtenidas durante la monitorización del modelo en Colab:

![Captura de Entrenamiento y Predicción 1](.github/assets/colab_training_1.png?v=2)
![Captura de Entrenamiento y Predicción 2](.github/assets/colab_training_2.png?v=2)
![Captura de Entrenamiento y Predicción 3](.github/assets/colab_training_3.png?v=2)
![Captura de Entrenamiento y Predicción 4](.github/assets/colab_training_4.png?v=2)

Los pesos resultantes con el menor error de validación (`LSM.weights`) fueron descargados e integrados directamente en la aplicación de escritorio final.
