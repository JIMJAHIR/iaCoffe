from flask import Flask, render_template, request
import os
import numpy as np
from PIL import Image
import tensorflow as tf
import cv2  # Agregar esta línea

app = Flask(__name__)

# Definir el tamaño deseado para las imágenes
imagen_alto, imagen_ancho = 150, 300

# Cargar el modelo preentrenado (asegúrate de que el nombre coincide)
model = tf.keras.models.load_model('modelFinal.h5')

# Función para preprocesar la imagen cargada
def preprocess_image(image):
    # Redimensionar la imagen a las dimensiones deseadas
    image = image.resize((imagen_ancho, imagen_alto))
    
    return image

# Función para realizar la predicción
def predict_disease(image):
    # Preprocesar la imagen
    preprocessed_image = preprocess_image(image)
    # Normalizar los valores de píxeles
    normalizar = np.array(preprocessed_image) / 255.0
    # Expandir las dimensiones para crear un lote (si es necesario)
    input_batch = np.expand_dims(np.array(normalizar), axis=0)
    # Realizar la predicción utilizando el modelo
    prediction = model.predict(input_batch)
    
    # Decodificar la predicción en una etiqueta (por ejemplo, 'miner', 'nodisease', ...)
    labels = ['Miner', 'Hoja Sana', 'Phoma', 'Rust']
    predicted_label = labels[np.argmax(prediction)]
    
    return predicted_label

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    result = None
    
    if request.method == 'POST':
        # Verificar si se cargó una imagen
        if 'file' not in request.files:
            return render_template('Predecir.html', result='No se cargó una imagen.')

        uploaded_image = request.files['file']

        # Verificar si se seleccionó un archivo
        if uploaded_image.filename == '':
            return render_template('Predecir.html', result='No se seleccionó un archivo.')

        # Verificar si la extensión del archivo es válida (puedes ajustar las extensiones según tus necesidades)
        allowed_extensions = {'jpg', 'jpeg', 'png'}
        if '.' not in uploaded_image.filename or uploaded_image.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return render_template('Predecir.html', result='Formato de archivo no válido. Use imágenes JPG o PNG.')

        # Leer la imagen cargada
        image = Image.open(uploaded_image)

        # Realizar la predicción
        predicted_disease = predict_disease(image)

        # Preparar el resultado para mostrar en la página
        result = f"Predicción: {predicted_disease}"

    return render_template('Predecir.html', result=result)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/enfermedades', methods=['GET', 'POST'])
def enfermedades():
    return render_template('enfermedades.html')

@app.route('/predecir', methods=['GET', 'POST'])
def predecir():
    return render_template('predecir.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
    return render_template('info.html')

if __name__ == '__main__':
    app.run(debug=True)