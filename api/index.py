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
    
    # Colores según el modo
    fill = "white" if is_dark else "black"
    back = "black" if is_dark else "white"
    icon_file = "iconoblack.svg" if is_dark else "iconowhite.svg"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(text_content)
    qr.make(fit=True)

    # Crear imagen con los colores solicitados
    qr_img = qr.make_image(fill_color=fill, back_color=back).convert('RGB')
    
    try:
        logo_path = os.path.join(app.static_folder, icon_file)
        if os.path.exists(logo_path):
            # Nota: PIL no lee SVG nativo, pero si lo guardas como PNG funcionará 100%
            logo = Image.open(logo_path).convert("RGBA")
            qr_width, qr_height = qr_img.size
            logo_size = int(qr_width / 5)
            logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
            pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
            qr_img.paste(logo, pos, mask=logo)
    except:
        pass

    img_io = io.BytesIO()
    qr_img.save(img_io, 'PNG')
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')
