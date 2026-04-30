document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('qr-input-image');
    const textContentArea = document.getElementById('text-content');
    const scanLoading = document.getElementById('scan-loading');
    const generatorForm = document.getElementById('qr-generator-form');
    const qrResultImage = document.getElementById('qr-image');

    // Manejar la subida y escaneo de imagen
    fileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        scanLoading.style.display = 'block';
        qrResultImage.style.display = 'none'; // Ocultar QR anterior

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/scan-qr', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (response.ok) {
                // Pre-cargar el texto plano en el formulario
                textContentArea.value = result.text;
                alert('Código QR escaneado con éxito.');
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error('Error al escanear:', error);
            alert('Hubo un problema al conectar con el servidor.');
        } finally {
            scanLoading.style.display = 'none';
        }
    });

    // Manejar la generación del nuevo QR
    generatorForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evitar recarga de página estándar

        const textContent = textContentArea.value;
        if (!textContent) {
            alert('Por favor, introduce contenido de texto.');
            return;
        }

        const formData = new FormData(generatorForm);
        const jsonData = {};
        formData.forEach((value, key) => jsonData[key] = value);

        qrResultImage.style.display = 'none'; // Ocultar imagen anterior mientras carga

        try {
            const response = await fetch('/generate-qr', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(jsonData)
            });

            if (response.ok) {
                // Recibir la imagen como un Blob (binary large object)
                const blob = await response.blob();
                const imageUrl = URL.createObjectURL(blob);
                qrResultImage.src = imageUrl;
                qrResultImage.style.display = 'inline-block'; // Mostrar la nueva imagen
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
