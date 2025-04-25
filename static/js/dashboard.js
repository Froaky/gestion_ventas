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


document.addEventListener('DOMContentLoaded', () => {
  const productos = JSON.parse(document.getElementById('productosData')?.textContent || '[]');
  const productosContainer = document.getElementById('productosContainer');
  const totalInput = document.getElementById('total');
  const addProductBtn = document.getElementById('addProduct');

  function actualizarTotal() {
    let total = 0;
    const filas = productosContainer.querySelectorAll('.producto-row');

    filas.forEach(fila => {
      const select = fila.querySelector('select');
      const cantidadInput = fila.querySelector('input[type="number"]');

      const precio = parseFloat(select?.selectedOptions[0]?.dataset.precio || '0');
      const cantidad = parseInt(cantidadInput.value || '0');
      if (!isNaN(precio) && !isNaN(cantidad)) {
        total += precio * cantidad;
      }
    });

    totalInput.value = total.toFixed(2);
  }

  productosContainer.addEventListener('change', actualizarTotal);
  productosContainer.addEventListener('input', actualizarTotal);

  addProductBtn.addEventListener('click', () => {
    const index = productosContainer.querySelectorAll('.producto-row').length;
    const nuevaFila = document.createElement('div');
    nuevaFila.classList.add('producto-row');
    nuevaFila.style.marginTop = '10px';

    nuevaFila.innerHTML = `
      <select name="productos_seleccionados[${index}][producto_id]" class="form-control producto-select" required>
        <option value="" disabled selected>Selecciona un producto</option>
        ${productos.map(p => `<option value="${p.id}" data-precio="${p.precio}">${p.name} (${p.stock} en stock)</option>`).join('')}
      </select>
      <input type="number" name="productos_seleccionados[${index}][cantidad]" class="form-control cantidad-input" placeholder="Cantidad" min="1" value="1" required>
    `;

    productosContainer.appendChild(nuevaFila);
  });

  // validación final antes de enviar (ya estaba en tu HTML)
  document.getElementById('ventaForm')?.addEventListener('submit', function (e) {
    if (!totalInput.value || parseFloat(totalInput.value) <= 0) {
      e.preventDefault();
      alert('Debes seleccionar productos válidos y cantidades para calcular el total antes de enviar.');
    }
  });

  actualizarTotal(); // calcular al inicio
});

 // Script para pintar según stock y ordenar columnas en la tabla de productos
document.addEventListener("DOMContentLoaded", () => {
  const tabla = document.getElementById("tabla-stock");
  if (!tabla) return; // Solo aplica si existe la tabla con id "tabla-stock"

  const tbody = tabla.querySelector("tbody");
  const filasOriginales = Array.from(tbody.querySelectorAll("tr"));

    // Pintar filas según el stock
  const pintarFilas = filas => {
    filas.forEach(fila => {
      const stock = parseInt(fila.dataset.stock);
      fila.classList.remove("sin-stock", "bajo-stock", "stock-ok");

      if (!isNaN(stock)) {
        if (stock < 1) {
          fila.classList.add("sin-stock");
        } else if (stock>0 && stock<= 2 ) {
          fila.classList.add("bajo-stock");
        } else {
          fila.classList.add("stock-ok");
        }
      }
    });
  };

    // Pintar al cargar
  pintarFilas(filasOriginales);

    // Función para ordenar por cualquier campo
  const ordenarPor = campo => {
    const filasOrdenadas = [...filasOriginales].sort((a, b) => {
      const valA = a.dataset[campo];
      const valB = b.dataset[campo];

      if (campo === "stock") {
        return parseInt(valA) - parseInt(valB);
      } else {
        return valA.localeCompare(valB);
      }
    });

    tbody.innerHTML = "";
    filasOrdenadas.forEach(f => tbody.appendChild(f));
    pintarFilas(filasOrdenadas);
  };

    // Botones de ordenar
  const botonesOrdenar = document.querySelectorAll(".ordenar-btn");
  botonesOrdenar.forEach(btn => {
    btn.addEventListener("click", () => {
      const campo = btn.dataset.sort;
      ordenarPor(campo);
    });
  });

    // Botón para restaurar el orden original
  const resetBtn = document.getElementById("reset-order");
  if (resetBtn) {
    resetBtn.addEventListener("click", () => {
      tbody.innerHTML = "";
      filasOriginales.forEach(f => tbody.appendChild(f));
      pintarFilas(filasOriginales);
    });
  }
});
// fIN Scripts productos 