    async function fetchData() {
        const response = await fetch('/data');
        const data = await response.json();
        const container = document.getElementById('devices-info');
        container.innerHTML = ''; // Limpiar antes de actualizar

        if (Object.keys(data).length === 0) {
            container.innerHTML = "<p>Esperando datos...</p>";
            setTimeout(fetchData, 2000);
            return;
        }

        for (const device in data) {
            const info = data[device][0]; // Tomamos el primer registro del dispositivo

            const total = info.total || 1; // Evitar división por 0
            const used = info.used || 0;
            const available = (total - used).toFixed(2);
            const percent = Math.round((used / total) * 100);

            // Determinar color de la barra
            let color = "green";
            if (percent > 80) color = "red";
            else if (percent > 50) color = "yellow";

            // Crear HTML del dispositivo
            const deviceHTML = `
            <div class="device">
                <h2>${device}</h2>
                <img src="/static/Hardware.png" alt="Icono del dispositivo">
                <p><strong>Total:</strong> ${total} GB</p>
                <p><strong>Usado:</strong> ${used} GB</p>
                <p><strong>Disponible:</strong> ${available} GB</p>
                <div class="progress-bar">
                    <div class="progress" style="width: ${percent}%; background-color: ${color};"></div>
                </div>
            </div>
        `;        

            container.innerHTML += deviceHTML;
        }

        setTimeout(fetchData, 5000); // Refrescar cada 5 segundos
    }

    fetchData();
