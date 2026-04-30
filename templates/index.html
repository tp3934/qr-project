document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const fileInput = document.getElementById('qr-input-image');
    const textContent = document.getElementById('text-content');
    const btnGenerate = document.getElementById('btn-generate');
    const qrImage = document.getElementById('qr-image');
    let isDarkMode = false;

    themeToggle.onclick = () => {
        isDarkMode = !isDarkMode;
        document.body.classList.toggle('dark-mode');
        themeToggle.innerText = isDarkMode ? '☀️ Modo Día' : '🌙 Modo Oscuro';
    };

    fileInput.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        document.getElementById('scan-loading').style.display = 'block';
        
        const reader = new FileReader();
        reader.onload = (event) => {
            const img = new Image();
            img.onload = () => {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                canvas.width = img.width; canvas.height = img.height;
                ctx.drawImage(img, 0, 0);
                const data = ctx.getImageData(0, 0, canvas.width, canvas.height);
                const code = jsQR(data.data, data.width, data.height);
                if (code) textContent.value = code.data;
                document.getElementById('scan-loading').style.display = 'none';
            };
            img.src = event.target.result;
        };
        reader.readAsDataURL(file);
    };

    btnGenerate.onclick = async () => {
        if (!textContent.value) return alert("Escribe algo");
        qrImage.style.display = 'none';
        
        const res = await fetch('/api/generate-qr', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ textContent: textContent.value, darkMode: isDarkMode })
        });
        
        if (res.ok) {
            const blob = await res.blob();
            qrImage.src = URL.createObjectURL(blob);
            qrImage.style.display = 'block';
        }
    };
});
