import os
import io
from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from PIL import Image
import cairosvg  # Necesaria para leer los SVG que subiste

app = Flask(__name__, template_folder='../templates', static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json
    text_content = data.get('textContent')
    # Recibimos si el usuario prefiere el icono para modo oscuro o claro
    use_dark_icon = data.get('darkMode', False)
    
    if not text_content:
        return jsonify({'error': 'Falta el contenido'}), 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text_content.encode('utf-8'))
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    try:
        # Elegimos el icono según la preferencia (SVG)
        icon_name = 'iconoblack.svg' if use_dark_icon else 'iconowhite.svg'
        logo_path = os.path.join(app.static_folder, icon_name)
        
        if os.path.exists(logo_path):
            # Convertimos el SVG a PNG en memoria para que Pillow lo entienda
            logo_png = cairosvg.svg2png(url=logo_path, output_width=200, output_height=200)
            logo = Image.open(io.BytesIO(logo_png))
            
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width / 5)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Error con el logo: {e}")

    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

app = app
