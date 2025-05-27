// Main JavaScript for Bar Yedra TPV System - Clean Design

// Variables globales
let privacyMode = false;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);

    // Initialize touch-friendly interactions
    initTouchInteractions();
    
    // Auto-refresh for real-time updates (optional)
    if (window.location.pathname === '/') {
        // Refresh main page every 30 seconds
        setInterval(function() {
            if (document.visibilityState === 'visible') {
                window.location.reload();
            }
        }, 30000);
    }

    // Add staggered animation to cards
    const cards = document.querySelectorAll('.table-card, .product-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.05}s`;
    });
});

// Touch-friendly interactions
function initTouchInteractions() {
    // Add touch feedback for cards
    const cards = document.querySelectorAll('.table-card, .product-card');
    
    cards.forEach(card => {
        card.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.98)';
        });
        
        card.addEventListener('touchend', function() {
            this.style.transform = '';
        });
    });
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-ES', {
        style: 'currency',
        currency: 'EUR'
    }).format(amount);
}

function formatTime(date) {
    return new Intl.DateTimeFormat('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

function formatDate(date) {
    return new Intl.DateTimeFormat('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric'
    }).format(new Date(date));
}

// Confirmation dialogs
function confirmAction(message) {
    return confirm(message);
}

// Loading states for buttons
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.classList.add('loading');
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Procesando...';
    } else {
        button.disabled = false;
        button.classList.remove('loading');
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
        }
    }
}

// Form validation helpers
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Number input helpers
function setupNumberInputs() {
    const numberInputs = document.querySelectorAll('input[type="number"]');
    
    numberInputs.forEach(input => {
        // Add increment/decrement buttons for touch devices
        const wrapper = document.createElement('div');
        wrapper.className = 'input-group';
        
        const decrementBtn = document.createElement('button');
        decrementBtn.type = 'button';
        decrementBtn.className = 'btn btn-outline-secondary';
        decrementBtn.innerHTML = '<i class="fas fa-minus"></i>';
        decrementBtn.onclick = () => {
            const value = parseInt(input.value) || 0;
            if (value > parseInt(input.min) || 0) {
                input.value = value - 1;
                input.dispatchEvent(new Event('change'));
            }
        };
        
        const incrementBtn = document.createElement('button');
        incrementBtn.type = 'button';
        incrementBtn.className = 'btn btn-outline-secondary';
        incrementBtn.innerHTML = '<i class="fas fa-plus"></i>';
        incrementBtn.onclick = () => {
            const value = parseInt(input.value) || 0;
            const max = parseInt(input.max) || 999;
            if (value < max) {
                input.value = value + 1;
                input.dispatchEvent(new Event('change'));
            }
        };
        
        // Only add if not already wrapped
        if (!input.parentElement.classList.contains('input-group')) {
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(decrementBtn);
            wrapper.appendChild(input);
            wrapper.appendChild(incrementBtn);
        }
    });
}

// Print helpers
function printReceipt(pedidoId) {
    const printWindow = window.open(`/print_receipt/${pedidoId}`, '_blank');
    printWindow.onload = function() {
        printWindow.print();
    };
}

// Local storage helpers for offline functionality
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
        return true;
    } catch (error) {
        console.error('Error saving to localStorage:', error);
        return false;
    }
}

function loadFromLocalStorage(key) {
    try {
        const data = localStorage.getItem(key);
        return data ? JSON.parse(data) : null;
    } catch (error) {
        console.error('Error loading from localStorage:', error);
        return null;
    }
}

// Keyboard shortcuts
document.addEventListener('keydown', function(event) {
    // Ctrl/Cmd + P for print
    if ((event.ctrlKey || event.metaKey) && event.key === 'p') {
        const printButtons = document.querySelectorAll('[onclick*="print"]');
        if (printButtons.length > 0) {
            event.preventDefault();
            printButtons[0].click();
        }
    }
    
    // Escape to close modals
    if (event.key === 'Escape') {
        const openModals = document.querySelectorAll('.modal.show');
        openModals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }
});

// Error handling
window.addEventListener('error', function(event) {
    console.error('JavaScript error:', event.error);
    // Could show user-friendly error message here
});

// Offline detection
window.addEventListener('online', function() {
    console.log('Connection restored');
    // Could sync data here if needed
});

window.addEventListener('offline', function() {
    console.log('Connection lost');
    // Show offline indicator
    showOfflineIndicator();
});

function showOfflineIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'alert alert-warning position-fixed top-0 end-0 m-3';
    indicator.style.zIndex = '9999';
    indicator.innerHTML = `
        <i class="fas fa-wifi-slash me-2"></i>
        Modo sin conexión activo
    `;
    document.body.appendChild(indicator);
    
    // Remove when online
    window.addEventListener('online', function() {
        if (indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }, { once: true });
}

// Funcionalidades del panel de pedido mejorado
function toggleOrderPanel() {
    const panel = document.querySelector('.order-panel-fixed');
    if (panel) {
        panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    }
}

function removeFromOrder(mesaId, productoId) {
    if (confirmAction('¿Estás seguro de que quieres eliminar este producto del pedido?')) {
        fetch('/remove_from_order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `mesa_id=${mesaId}&producto_id=${productoId}`
        }).then(response => {
            if (response.ok) {
                location.reload();
            } else {
                alert('Error al eliminar el producto');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
}

function splitBill(mesaId) {
    const personas = prompt('¿Entre cuántas personas quieres dividir la cuenta?', '2');
    if (personas && !isNaN(personas) && personas > 1) {
        fetch('/split_bill', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `mesa_id=${mesaId}&personas=${personas}`
        }).then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(`Cuenta dividida entre ${personas} personas:\nCada persona debe pagar: €${data.amount_per_person}`);
            } else {
                alert('Error al dividir la cuenta');
            }
        }).catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
}

// Initialize number inputs when DOM is ready
document.addEventListener('DOMContentLoaded', setupNumberInputs);

// Privacy toggle function
function togglePrivacy() {
    privacyMode = !privacyMode;
    const icon = document.getElementById('privacy-icon');
    const button = document.getElementById('privacy-btn');
    
    if (privacyMode) {
        icon.className = 'fas fa-eye-slash';
        button.classList.add('active');
        button.innerHTML = '<i class="fas fa-eye-slash"></i> Mostrar cifras';
        
        // Ocultar todos los elementos que contengan €, precios o totales
        document.querySelectorAll('*').forEach(el => {
            if (el.textContent.match(/€[\d\.,]+|[\d\.,]+\s*€|\d+[\.,]\d+/) && 
                !el.classList.contains('privacy-toggle')) {
                el.classList.add('privacy-blur');
            }
        });
    } else {
        icon.className = 'fas fa-eye';
        button.classList.remove('active');
        button.innerHTML = '<i class="fas fa-eye"></i> Ocultar cifras';
        
        document.querySelectorAll('.privacy-blur').forEach(el => {
            el.classList.remove('privacy-blur');
        });
    }
}

// Enhanced form validation
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = 'var(--color-danger)';
            isValid = false;
        } else {
            field.style.borderColor = 'var(--color-gray-medium)';
        }
    });
    
    return isValid;
}

// Enhanced button loading states
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.style.opacity = '0.6';
        const originalText = button.innerHTML;
        button.setAttribute('data-original-text', originalText);
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
    } else {
        button.disabled = false;
        button.style.opacity = '1';
        const originalText = button.getAttribute('data-original-text');
        if (originalText) {
            button.innerHTML = originalText;
        }
    }
}

// Print functionality
function printReceipt(pedidoId) {
    const printWindow = window.open(`/print_receipt/${pedidoId}`, '_blank');
    printWindow.onload = function() {
        printWindow.print();
    };
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Función para mostrar/ocultar menú móvil
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    const body = document.body;
    
    sidebar.classList.toggle('show');
    
    // Prevenir scroll del body cuando el menú está abierto
    if (sidebar.classList.contains('show')) {
        body.style.overflow = 'hidden';
    } else {
        body.style.overflow = '';
    }
}

// Inicializar funcionalidad móvil cuando se carga el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Cerrar menú móvil al hacer clic fuera de él
    document.addEventListener('click', function(event) {
        const sidebar = document.querySelector('.sidebar');
        const menuToggle = document.querySelector('.mobile-menu-toggle');
        
        // Si el menú está abierto y se hace clic fuera de él
        if (sidebar && sidebar.classList.contains('show') && 
            !sidebar.contains(event.target) && 
            menuToggle && !menuToggle.contains(event.target)) {
            sidebar.classList.remove('show');
            document.body.style.overflow = '';
        }
    });

    // Cerrar menú móvil al hacer clic en un enlace del menú
    document.querySelectorAll('.sidebar .nav-link').forEach(link => {
        link.addEventListener('click', function() {
            const sidebar = document.querySelector('.sidebar');
            if (sidebar && sidebar.classList.contains('show')) {
                sidebar.classList.remove('show');
                document.body.style.overflow = '';
            }
        });
    });

    // Cerrar menú móvil al cambiar orientación o redimensionar
    window.addEventListener('resize', function() {
        const sidebar = document.querySelector('.sidebar');
        if (window.innerWidth > 768 && sidebar && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
            document.body.style.overflow = '';
        }
    });
});

// Export functions for global use
window.YedraTPV = {
    formatCurrency,
    formatTime,
    formatDate,
    confirmAction,
    setButtonLoading,
    validateForm,
    printReceipt,
    togglePrivacy,
    toggleMobileMenu,
    scrollToElement,
    saveToLocalStorage,
    loadFromLocalStorage
};
