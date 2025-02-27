async function fetchData() {
  const response = await fetch("/data");
  const data = await response.json();
  const container = document.getElementById("devices-info");
  container.innerHTML = ""; // Limpiar antes de actualizar

  if (data.length === 0) {
    container.innerHTML = "<p>Esperando datos...</p>";
    setTimeout(fetchData, 2000);
    return;
  }

  data.forEach((deviceInfo) => {
    const device = deviceInfo.device_name;
    const info = deviceInfo.data[0]; // Primer registro del dispositivo

    const total = info.total || 1;
    const used = info.used || 0;
    const available = (total - used).toFixed(2);
    const percent = Math.round((used / total) * 100);
    const status = deviceInfo.status;

    let color = "green";
    if (percent > 80) color = "red";
    else if (percent > 50) color = "yellow";

    const deviceHTML = `
      <div class="device ${status === "No reporta" ? "no-reporta" : ""}">
          <h2>
            ${device} <br/>
            <span style="color: ${status === "No reporta" ? "red" : "green"}">
              ${status === "No reporta" ? "Última conexión" : "Reportando"}
            </span>
          </h2>
          <img src="/static/Hardware.png" alt="Icono del dispositivo">
          <p><strong>Total:</strong> ${total} GB</p>
          <p><strong>Usado:</strong> ${used} GB</p>
          <p><strong>Disponible:</strong> ${available} GB</p>
          <div class="progress-bar">
              <div class="progress" style="width: ${percent}%; background-color: ${color};"></div>
          </div>

          <div class="overlay">
            ${device} <br/> No reporta
          </div>
      </div>
    `;

    container.innerHTML += deviceHTML;
  });

  setTimeout(fetchData, 5000);
}

fetchData();
