import os
import io
from flask import Flask, render_template, request, jsonify, send_file
import qrcode
from PIL import Image, ImageDraw

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
        
        # Colores del QR
        fill = "white" if is_dark else "black"
        back = "black" if is_dark else "white"
        icon_name = "iconoblack.png" if is_dark else "iconowhite.png"

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(text_content)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color=fill, back_color=back).convert('RGB')
        
        logo_path = os.path.join(app.static_folder, icon_name)
        
        if os.path.exists(logo_path):
            logo = Image.open(logo_path).convert("RGBA")
            
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width / 5) # Tamaño del logo
            
            # --- NUEVA LÓGICA: FONDO PARA EL LOGO ---
            # Creamos un cuadrado un poco más grande que el logo para que sirva de "margen"
            padding = 10 
            bg_size = logo_size + padding
            
            # El fondo será del mismo color que el fondo del QR (back)
            logo_bg = Image.new("RGBA", (bg_size, bg_size), back)
            
            # Redimensionar el logo original
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            # Pegar el logo sobre ese fondo nuevo
            logo_bg.paste(logo, (padding // 2, padding // 2), mask=logo)
            
            # Pegar el conjunto (fondo + logo) en el centro del QR
            pos = ((qr_width - bg_size) // 2, (qr_height - bg_size) // 2)
            qr_img.paste(logo_bg, pos)
            # ---------------------------------------

        img_io = io.BytesIO()
        qr_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
