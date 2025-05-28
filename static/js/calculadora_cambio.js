// Calculadora de cambio - Sistema limpio y funcional
let totalAPagar = 0;
let valorActual = '';

function abrirModalPago() {
    console.log('Abriendo modal de pago');
    
    // Calcular total del pedido
    totalAPagar = obtenerTotalPedido();
    console.log('Total a pagar:', totalAPagar);
    
    // Mostrar total en el modal
    const elementoTotal = document.getElementById('totalAmount');
    if (elementoTotal) {
        elementoTotal.textContent = '€' + totalAPagar.toFixed(2);
    }
    
    // Ocultar calculadora
    const calculadora = document.getElementById('cashCalculator');
    if (calculadora) {
        calculadora.style.display = 'none';
    }
    
    // Mostrar modal
    const modal = document.getElementById('closeOrderModal');
    if (modal) {
        modal.style.display = 'flex';
    }
}

function seleccionarEfectivo() {
    console.log('Efectivo seleccionado');
    
    // Mostrar calculadora inmediatamente
    const calculadora = document.getElementById('cashCalculator');
    console.log('Elemento calculadora encontrado:', calculadora);
    
    if (calculadora) {
        console.log('Mostrando calculadora...');
        calculadora.style.display = 'block';
        calculadora.style.visibility = 'visible';
        
        // Limpiar campos y resetear valor actual
        valorActual = '';
        const inputDinero = document.getElementById('cashReceived');
        const displayCambio = document.getElementById('changeAmount');
        const botonConfirmar = document.getElementById('confirmCashBtn');
        
        console.log('Elementos encontrados:', {inputDinero, displayCambio, botonConfirmar});
        
        if (inputDinero) inputDinero.value = '0.00';
        if (displayCambio) displayCambio.textContent = '€0.00';
        if (botonConfirmar) botonConfirmar.disabled = true;
        
        console.log('Calculadora configurada');
    } else {
        console.error('No se encontró el elemento cashCalculator');
    }
}

function seleccionarTarjeta() {
    console.log('Tarjeta seleccionada');
    
    if (confirm('¿Confirmar pago con tarjeta por €' + totalAPagar.toFixed(2) + '?')) {
        enviarPago('tarjeta');
    }
}

function calcularCambio() {
    const inputDinero = document.getElementById('cashReceived');
    const displayCambio = document.getElementById('changeAmount');
    const botonConfirmar = document.getElementById('confirmCashBtn');
    
    if (!inputDinero || !displayCambio || !botonConfirmar) return;
    
    const dineroRecibido = parseFloat(valorActual) || 0;
    const cambio = dineroRecibido - totalAPagar;
    
    console.log('Calculando:', {dineroRecibido, totalAPagar, cambio, valorActual});
    
    if (cambio < 0) {
        displayCambio.textContent = '€' + Math.abs(cambio).toFixed(2) + ' (Falta)';
        displayCambio.style.color = 'red';
        botonConfirmar.disabled = true;
        botonConfirmar.style.background = '#6c757d';
    } else {
        displayCambio.textContent = '€' + cambio.toFixed(2);
        displayCambio.style.color = 'green';
        botonConfirmar.disabled = false;
        botonConfirmar.style.background = '#28a745';
    }
}

function confirmarPagoEfectivo() {
    const inputDinero = document.getElementById('cashReceived');
    if (!inputDinero) return;
    
    const dineroRecibido = parseFloat(inputDinero.value) || 0;
    if (dineroRecibido >= totalAPagar) {
        enviarPago('efectivo', dineroRecibido);
    }
}

function enviarPago(metodoPago, dineroRecibido = null) {
    console.log('Enviando pago:', metodoPago, dineroRecibido);
    
    // Crear formulario
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = window.location.pathname.replace('/mesa/', '/pay_order/');
    
    // Método de pago
    const inputMetodo = document.createElement('input');
    inputMetodo.type = 'hidden';
    inputMetodo.name = 'forma_pago';
    inputMetodo.value = metodoPago;
    form.appendChild(inputMetodo);
    
    // Para efectivo, datos adicionales
    if (metodoPago === 'efectivo' && dineroRecibido) {
        const inputRecibido = document.createElement('input');
        inputRecibido.type = 'hidden';
        inputRecibido.name = 'dinero_recibido';
        inputRecibido.value = dineroRecibido.toFixed(2);
        form.appendChild(inputRecibido);
        
        const inputCambio = document.createElement('input');
        inputCambio.type = 'hidden';
        inputCambio.name = 'cambio';
        inputCambio.value = (dineroRecibido - totalAPagar).toFixed(2);
        form.appendChild(inputCambio);
    }
    
    document.body.appendChild(form);
    form.submit();
}

function obtenerTotalPedido() {
    // Buscar total en el resumen
    const elementoTotal = document.querySelector('.summary-value');
    if (elementoTotal) {
        const texto = elementoTotal.textContent.replace('€', '').replace(',', '.');
        const total = parseFloat(texto) || 0;
        console.log('Total desde resumen:', total);
        return total;
    }
    
    // Calcular desde items si no hay resumen
    let total = 0;
    const items = document.querySelectorAll('.order-item');
    
    items.forEach(item => {
        const precio = item.querySelector('.item-price');
        const cantidad = item.querySelector('.quantity');
        
        if (precio && cantidad) {
            const p = parseFloat(precio.textContent.replace('€', '')) || 0;
            const c = parseInt(cantidad.textContent) || 0;
            total += p * c;
        }
    });
    
    return total;
}

function cerrarModal() {
    const modal = document.getElementById('closeOrderModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function ocultarCalculadora() {
    const calculadora = document.getElementById('cashCalculator');
    if (calculadora) {
        calculadora.style.display = 'none';
    }
}

// Funciones del teclado numérico
function agregarNumero(numero) {
    valorActual += numero;
    actualizarDisplay();
    calcularCambio();
}

function agregarDecimal() {
    if (!valorActual.includes('.')) {
        if (valorActual === '') {
            valorActual = '0.';
        } else {
            valorActual += '.';
        }
        actualizarDisplay();
        calcularCambio();
    }
}

function borrarUltimo() {
    valorActual = valorActual.slice(0, -1);
    actualizarDisplay();
    calcularCambio();
}

function establecerCantidad(cantidad) {
    valorActual = cantidad;
    actualizarDisplay();
    calcularCambio();
}

function limpiarCantidad() {
    valorActual = '';
    actualizarDisplay();
    calcularCambio();
}

function actualizarDisplay() {
    const input = document.getElementById('cashReceived');
    if (input) {
        input.value = valorActual || '0.00';
    }
}