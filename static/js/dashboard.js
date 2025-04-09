// dashboard.js

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

  // --- Mostrar notificaciones con Toastr ---
  if (window.flashedMessages && Array.isArray(window.flashedMessages)) {
    toastr.options = {
      "positionClass": "toast-top-right",
      "timeOut": "3000"
    };
    window.flashedMessages.forEach(pair => {
      toastr[pair[0]](pair[1]);
    });
  }

  // --- Generar gráfico si estamos en la página de inicio y se inyectaron datos ---
  const ctx = document.getElementById('salesChart');
  if (ctx && window.salesLabels && window.salesTotals) {
    const rootStyles = getComputedStyle(document.documentElement);
    const backgroundColor = rootStyles.getPropertyValue('--color-red').trim();
    const borderColor = rootStyles.getPropertyValue('--color-mid-blue').trim();

    const salesChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: window.salesLabels, // Inyectado desde la plantilla
        datasets: [{
          label: 'Ventas de los últimos 5 meses',
          data: window.salesTotals, // Inyectado desde la plantilla
          backgroundColor: backgroundColor,
          borderColor: borderColor,
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        scales: {
          y: { beginAtZero: true }
        },
        onClick: (evt, elements) => {
          if (elements.length > 0) {
            const index = elements[0].index;
            const month = window.salesLabels[index];
            // Si deseas mostrar detalles al hacer clic, puedes hacer una petición fetch al endpoint correspondiente
            // Por ejemplo, si tienes un endpoint '/ventas/api/sales_details?month=month'
            // fetch(`/ventas/api/sales_details?month=${month}`)
            //   .then(response => response.json())
            //   .then(details => {
            //     let detailsHTML = `<h3>Ventas de ${month}</h3>`;
            //     if(details.length === 0){
            //       detailsHTML += `<p>No se encontraron ventas para este mes.</p>`;
            //     } else {
            //       detailsHTML += `<ul>`;
            //       details.forEach(item => {
            //         detailsHTML += `<li>ID: ${item.id}, Total: ${item.total}, Fecha: ${item.fecha}</li>`;
            //       });
            //       detailsHTML += `</ul>`;
            //     }
            //     const detailsContainer = document.getElementById('salesDetails');
            //     if (detailsContainer) {
            //       detailsContainer.innerHTML = detailsHTML;
            //     }
            //   })
            //   .catch(error => console.error('Error al obtener detalles:', error));
            // Si no deseas usar un endpoint, puedes inyectar también los detalles en la plantilla.
            console.log(`Se hizo clic en el mes ${month}`);
          }
        }
      }
    });
  }
});
