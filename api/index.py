import os
import io
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from PIL import Image

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Ruta principal: Sirve la página web
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para escanear la imagen subida (CORREGIDO PARA VERCEL)
@app.route('/api/scan-qr', methods=['POST'])
def scan_qr():
    if 'image' not in request.files:
        return jsonify({'error': 'No se subió ninguna imagen'}), 400
    
    file = request.files['image']
    
    # Leer la imagen usando OpenCV
    filestr = file.read()
    npimg = np.frombuffer(filestr, np.uint8) # Corregido a frombuffer
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    
    # Usar el detector de QR de OpenCV
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    
    if bbox is not None and data:
        return jsonify({'text': data})
    else:
        return jsonify({'error': 'No se pudo detectar un código QR válido en la imagen.'}), 404

# Ruta para generar el nuevo QR con los parámetros del formulario (CORREGIDO PARA VERCEL)
@app.route('/api/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json
    text_content = data.get('textContent')
    barcode_size_str = data.get('barcodeSize')
    error_correction_str = data.get('errorCorrection')
    character_encoding = data.get('characterEncoding') # En python 'qrcode' asume UTF-8 por defecto

    if not text_content:
        return jsonify({'error': 'Falta el contenido de texto'}), 400

    # Mapear el tamaño del código de barras a 'box_size' de qrcode
    size_map = {'Small': 5, 'Medium': 10, 'Large': 15}
    box_size = size_map.get(barcode_size_str, 10)

    # Mapear la corrección de errores
    ec_map = {
        'L': qrcode.constants.ERROR_CORRECT_L,
        'M': qrcode.constants.ERROR_CORRECT_M,
        'Q': qrcode.constants.ERROR_CORRECT_Q,
        'H': qrcode.constants.ERROR_CORRECT_H
    }
    error_correction = ec_map.get(error_correction_str, qrcode.constants.ERROR_CORRECT_M)

    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=error_correction,
        box_size=box_size,
        border=4,
    )
    qr.add_data(text_content.encode('utf-8')) # Asegurar UTF-8
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar en memoria para enviarlo
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

# Asegurar que Vercel reconozca la app
app = app

if __name__ == '__main__':
    # Para pruebas locales
    app.run(debug=True, host='0.0.0.0', port=5000)
