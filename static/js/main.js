// Main JavaScript for Bar Yedra TPV System

// Initialize Bootstrap tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize Bootstrap popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert-dismissible');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
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

// Initialize number inputs when DOM is ready
document.addEventListener('DOMContentLoaded', setupNumberInputs);

// Export functions for global use
window.YedraTPV = {
    formatCurrency,
    formatTime,
    formatDate,
    confirmAction,
    setButtonLoading,
    validateForm,
    printReceipt,
    saveToLocalStorage,
    loadFromLocalStorage
};
