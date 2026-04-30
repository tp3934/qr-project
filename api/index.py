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
    data = request.json
    text_content = data.get('textContent')
    is_dark = data.get('darkMode', False)
    
    # 1. Definir colores y archivos
    # Para que el logo se vea, usaremos PNGs
    fill = "white" if is_dark else "black"
    back = "black" if is_dark else "white"
    icon_file = "iconoblack.png" if is_dark else "iconowhite.png"

    # 2. Configurar el QR (Importante: Error Correction H para que el logo no lo rompa)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text_content)
    qr.make(fit=True)

    # 3. Crear la imagen base
    qr_img = qr.make_image(fill_color=fill, back_color=back).convert('RGB')
    
    # 4. PEGAR EL LOGO EN EL CENTRO
    try:
        logo_path = os.path.join(app.static_folder, icon_file)
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            
            # Calculamos tamaño (20% del QR)
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width / 5)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Posición central exacta
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            
            # Pegar logo con su transparencia
            qr_img.paste(logo, pos, mask=logo)
    except Exception as e:
        print(f"Error pegando el logo: {e}")

    # 5. Enviar al navegador
    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
