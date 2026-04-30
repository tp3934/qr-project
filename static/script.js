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
        use_dark_icon = data.get('darkMode', False)
        
        if not text_content:
            return jsonify({'error': 'Falta el contenido'}), 400

        # Generar QR con nivel de corrección H (Alto) para soportar el logo
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text_content)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Lógica del Logo
        icon_name = 'iconoblack.svg' if use_dark_icon else 'iconowhite.svg'
        logo_path = os.path.join(app.static_folder, icon_name)
        
        # Intentar cargar el logo (solo si PIL lo soporta directamente, como PNG/JPG)
        # Nota: Vercel tiene problemas nativos con SVG. Si falla, genera el QR sin logo.
        if os.path.exists(logo_path):
            try:
                logo = Image.open(logo_path)
                logo = logo.convert("RGBA")
                
                qr_width, qr_height = qr_img.size
                logo_size = int(qr_width / 5)
                logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
                qr_img.paste(logo, pos, mask=logo)
            except:
                pass # Si el formato no es compatible, envía el QR limpio

        img_io = io.BytesIO()
        qr_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

app = app
