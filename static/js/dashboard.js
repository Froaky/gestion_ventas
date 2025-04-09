// static/js/dashboard.js

document.addEventListener('DOMContentLoaded', () => {
  // --- Alternar Modo Oscuro ---
  const toggleThemeBtn = document.getElementById('toggleTheme');
  if (toggleThemeBtn) {
    toggleThemeBtn.addEventListener('click', function() {
      document.body.classList.toggle('dark-mode');
      const icon = this.querySelector('i');
      icon.className = document.body.classList.contains('dark-mode')
        ? 'fa-solid fa-sun'
        : 'fa-solid fa-moon';
    });
  }

  // --- Mostrar notificaciones con Toastr (si existieran mensajes flash) ---
  if (window.flashedMessages && Array.isArray(window.flashedMessages)) {
    toastr.options = {
      "positionClass": "toast-top-right",
      "timeOut": "3000"
    };
    window.flashedMessages.forEach(pair => {
      toastr[pair[0]](pair[1]);
    });
  }

  // --- Actualizar gráfico de ventas ---
  const ctx = document.getElementById('salesChart');
  if (!ctx) {
    console.error("No se encontró el elemento 'salesChart'.");
    return;
  }
  let salesChart;

  function updateChartData() {
    fetch('/ventas/api/sales_by_month')
      .then(response => {
        if (!response.ok) {
          throw new Error('Respuesta no válida del servidor');
        }
        return response.json();
      })
      .then(data => {
        console.log("Datos recibidos del endpoint:", data);
        const labels = data.labels;
        const totals = data.totals;
        const counts = data.counts;

        // Obtener colores definidos en CSS para mantener la estética
        const rootStyles = getComputedStyle(document.documentElement);
        const backgroundColor = rootStyles.getPropertyValue('--color-red').trim();
        const borderColor = rootStyles.getPropertyValue('--color-mid-blue').trim();

        // Si no existe el gráfico, lo creamos
        if (!salesChart) {
          salesChart = new Chart(ctx, {
            type: 'bar',
            data: {
              labels: labels,
              datasets: [
                {
                  label: 'Ventas Totales ($)',
                  data: totals,
                  backgroundColor: backgroundColor,
                  borderColor: borderColor,
                  borderWidth: 1,
                  yAxisID: 'y'
                },
                {
                  label: 'Cantidad de Ventas',
                  data: counts,
                  backgroundColor: 'rgba(0, 0, 0, 0.3)',  // Podés ajustar este color
                  borderColor: 'rgba(0, 0, 0, 0.5)',
                  borderWidth: 1,
                  yAxisID: 'y1'
                }
              ]
            },
            options: {
              responsive: true,
              interaction: { mode: 'index', intersect: false },
              scales: {
                y: {
                  beginAtZero: true,
                  position: 'left',
                  title: {
                    display: true,
                    text: 'Ventas en $'
                  }
                },
                y1: {
                  beginAtZero: true,
                  position: 'right',
                  grid: { drawOnChartArea: false },
                  title: {
                    display: true,
                    text: 'Cantidad de ventas'
                  }
                }
              },
              onClick: (evt, elements) => {
                if (elements.length > 0) {
                  const index = elements[0].index;
                  const month = labels[index];
                  console.log(`Se hizo clic en la barra del mes ${month}`);
                  // Aquí podrías agregar lógica para mostrar detalles específicos de ese mes.
                }
              }
            }
          });
        } else {
          // Si el gráfico ya existe, actualizamos sus datos
          salesChart.data.labels = labels;
          salesChart.data.datasets[0].data = totals;
          salesChart.data.datasets[1].data = counts;
          salesChart.update();
        }
      })
      .catch(error => {
        console.error("Error al obtener datos de ventas:", error);
      });
  }

  // Crear el gráfico al cargar la página
  updateChartData();
  // Actualizar automáticamente cada 60 segundos (60000 milisegundos)
  setInterval(updateChartData, 60000);
});
