// Función para cargar estadísticas
async function loadStats() {
    try {
        const response = await fetch('/risks/');
        const risks = await response.json();
        
        document.getElementById('total-risks').textContent = risks.length;
        document.getElementById('critical-risks').textContent = risks.filter(r => r.risk_level === 'CRITICAL').length;
        document.getElementById('high-risks').textContent = risks.filter(r => r.risk_level === 'HIGH').length;
        document.getElementById('medium-risks').textContent = risks.filter(r => r.risk_level === 'MEDIUM').length;
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Función para eliminar riesgo
async function deleteRisk(id) {
    if (confirm('¿Estás seguro de que quieres eliminar este riesgo?')) {
        try {
            const response = await fetch(`/risks/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert('Riesgo eliminado correctamente');
                location.reload();
            } else {
                alert('Error al eliminar el riesgo');
            }
        } catch (error) {
            console.error('Error deleting risk:', error);
            alert('Error al eliminar el riesgo');
        }
    }
}


// Función para ver riesgo
function viewRisk(id) {
    window.location.href = `/risk/${id}`;
}

// Función para editar riesgo
function editRisk(id) {
    // Por ahora redirigimos al formulario de agregar
    // Puedes implementar edición después
    alert('Funcionalidad de edición en desarrollo. Redirigiendo a crear nuevo riesgo.');
    window.location.href = '/add-risk';
}

// Función para eliminar riesgo
async function deleteRisk(id) {
    if (confirm('¿Estás seguro de que quieres eliminar este riesgo?')) {
        try {
            const response = await fetch(`/risks/${id}`, {
                method: 'DELETE'
            });
            
            if (response.ok) {
                alert('Riesgo eliminado correctamente');
                // Si estamos en la página de detalle, volver a la lista
                if (window.location.pathname.includes('/risk/')) {
                    window.location.href = '/risks';
                } else {
                    location.reload();
                }
            } else {
                alert('Error al eliminar el riesgo');
            }
        } catch (error) {
            console.error('Error deleting risk:', error);
            alert('Error al eliminar el riesgo');
        }
    }
}

// Preview del riesgo en tiempo real
function setupRiskPreview() {
    const form = document.querySelector('form');
    if (!form) return;
    
    const preview = document.getElementById('risk-preview');
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
        input.addEventListener('input', updatePreview);
    });
    
    function updatePreview() {
        const title = form.querySelector('[name="title"]').value || 'Sin título';
        const probability = form.querySelector('[name="probability"]').value || '3';
        const impact = form.querySelector('[name="impact"]').value || '3';
        const score = probability * impact;
        
        let level = 'LOW';
        let levelClass = 'low';
        
        if (score > 20) {
            level = 'CRITICAL';
            levelClass = 'critical';
        } else if (score > 10) {
            level = 'HIGH';
            levelClass = 'high';
        } else if (score > 4) {
            level = 'MEDIUM';
            levelClass = 'medium';
        }
        
        preview.innerHTML = `
            <div class="risk-preview-card ${levelClass}">
                <h5>${title}</h5>
                <div class="d-flex justify-content-between">
                    <span>Probabilidad: ${probability}/5</span>
                    <span>Impacto: ${impact}/5</span>
                    <span>Puntuación: ${score}</span>
                </div>
                <div class="mt-2">
                    <span class="badge risk-badge ${levelClass}">${level}</span>
                </div>
            </div>
        `;
    }
    
    updatePreview();
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('total-risks')) {
        loadStats();
    }
    
    if (document.getElementById('risk-preview')) {
        setupRiskPreview();
    }
});