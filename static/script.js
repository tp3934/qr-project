document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('qr-input-image');
    const textContentArea = document.getElementById('text-content');
    const scanLoading = document.getElementById('scan-loading');
    const generatorForm = document.getElementById('qr-generator-form');
    const qrResultImage = document.getElementById('qr-image');

    // Manejar la subida y escaneo de imagen DIRECTAMENTE EN EL NAVEGADOR
    fileInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (!file) return;

        scanLoading.style.display = 'block';
        qrResultImage.style.display = 'none';

        const reader = new FileReader();
        reader.onload = (e) => {
            const img = new Image();
            img.onload = () => {
                // Dibujar la imagen en un lienzo invisible para leer sus píxeles
                const canvas = document.createElement('canvas');
                const context = canvas.getContext('2d');
                canvas.width = img.width;
                canvas.height = img.height;
                context.drawImage(img, 0, 0, img.width, img.height);
                
                // Extraer la información de los píxeles
                const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
                
                // Aquí ocurre la magia con jsQR
                const code = jsQR(imageData.data, imageData.width, imageData.height, {
                    inversionAttempts: "dontInvert",
                });

                if (code) {
                    textContentArea.value = code.data;
                    alert('Código QR escaneado con éxito.');
                } else {
                    alert('Error: No se pudo detectar un QR. Intenta recortar la imagen para que solo se vea el QR.');
                }
                scanLoading.style.display = 'none';
            };
            img.src = e.target.result;
        };
        reader.readAsDataURL(file);
    });

    // Manejar la generación del nuevo QR (Esto sigue enviándose a Python)
    generatorForm.addEventListener('submit', async (event) => {
        event.preventDefault(); 

        const textContent = textContentArea.value;
        if (!textContent) {
            alert('Por favor, introduce contenido de texto.');
            return;
        }

        const formData = new FormData(generatorForm);
        const jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        qrResultImage.style.display = 'none'; 

        try {
            const response = await fetch('/api/generate-qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            if (response.ok) {
                const blob = await response.blob();
                const imageUrl = URL.createObjectURL(blob);
                qrResultImage.src = imageUrl;
                qrResultImage.style.display = 'inline-block'; 
            } else {
                const result = await response.json();
                alert(`Error al generar: ${result.error}`);
            }
        } catch (error) {
            console.error('Error al generar:', error);
            alert('Hubo un problema al generar el código QR.');
        }
    });
});
