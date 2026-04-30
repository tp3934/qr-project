document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-toggle');
    const qrInput = document.getElementById('qr-input');
    const textContent = document.getElementById('text-content');
    const generateBtn = document.getElementById('generate-btn');
    const qrImage = document.getElementById('qr-image');
    const scanLoading = document.getElementById('scan-loading');
    
    let isDarkMode = false;

    // Alternar modo oscuro
    themeBtn.onclick = () => {
        isDarkMode = !isDarkMode;
        document.body.classList.toggle('dark-mode');
        themeBtn.innerText = isDarkMode ? '☀️ Modo Día' : '🌙 Modo Oscuro';
    };

    // Escáner local (Rápido y privado)
    qrInput.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        scanLoading.style.display = 'block';
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width; canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const code = jsQR(imageData.data, imageData.width, imageData.height);
                
                if (code) {
                    textContent.value = code.data;
                } else {
                    alert("No se encontró un QR. Intenta con otra foto.");
                }
                scanLoading.style.display = 'none';
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    };

    // Generar QR llamando a la API de Python
    generateBtn.onclick = async () => {
        if (!textContent.value) return alert("Escribe algo primero.");
        
        qrImage.style.display = 'none';
        try {
            const res = await fetch('/api/generate-qr', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    textContent: textContent.value,
                    darkMode: isDarkMode
                })
            });

            if (res.ok) {
                const blob = await res.blob();
                qrImage.src = URL.createObjectURL(blob);
                qrImage.style.display = 'block';
            } else {
                alert("Error al generar el QR. Revisa los logs de Vercel.");
            }
        } catch (err) {
            alert("Error de conexión con el servidor.");
        }
    };
});
