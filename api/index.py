import os
import io
from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from PIL import Image

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-qr', methods=['POST'])
def generate_qr():
    try:
        data = request.json
        text_content = data.get('textContent')
        is_dark = data.get('darkMode', False)
        
        # Configuramos colores y el archivo PNG correcto
        # Si es modo oscuro: puntos blancos, fondo negro, icono negro
        # Si es modo claro: puntos negros, fondo blanco, icono blanco
        fill = "white" if is_dark else "black"
        back = "black" if is_dark else "white"
        icon_name = "iconoblack.png" if is_dark else "iconowhite.png"

        # Generamos el QR con corrección de error ALTA (H)
        # Esto es vital para que el QR siga funcionando aunque le pongamos una imagen encima
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text_content)
        qr.make(fit=True)

        # Creamos la imagen en modo RGB para poder manipularla
        qr_img = qr.make_image(fill_color=fill, back_color=back).convert('RGB')
        
        # Lógica para pegar el LOGO
        logo_path = os.path.join(app.static_folder, icon_name)
        
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            
            # Calculamos que el logo ocupe el 20% del código QR
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width / 5)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Calculamos la posición central exacta
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            # Pegamos el logo usando su propio canal alfa como máscara para la transparencia
            qr_img.paste(logo, pos, mask=logo)
        else:
            print(f"Error: No se encontró el archivo en {logo_path}")

        # Guardamos el resultado en un buffer de memoria
        img_io = io.BytesIO()
        qr_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
