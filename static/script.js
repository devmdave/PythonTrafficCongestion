// Real-time metrics update
let metricsUpdateInterval;

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Traffic Flow Analysis System Initialized');
    
    // Start metrics updates
    startMetricsUpdate();
    
    // Setup restart button
    setupRestartButton();
    
    // Add smooth number transitions
    addNumberTransitions();
});

/**
 * Start periodic metrics updates
 */
function startMetricsUpdate() {
    // Update immediately
    updateMetrics();
    
    // Then update every second
    metricsUpdateInterval = setInterval(updateMetrics, 1000);
}

/**
 * Fetch and update metrics from server
 */
async function updateMetrics() {
    try {
        const response = await fetch('/metrics');
        const data = await response.json();
        
        // Update each metric with animation
        updateMetricValue('vehicles', data.vehicles);
        updateMetricValue('speed', Math.round(data.speed));
        updateMetricValue('accuracy', data.accuracy.toFixed(3));
        updateMetricValue('fps', data.fps);
        updateMetricValue('density', data.density.toFixed(3));
        updateMetricValue('flow', data.flow.toFixed(3));
        updateMetricValue('headway', data.headway.toFixed(3));
        updateMetricValue('vehiclesUp', data.vehicles_up);
        updateMetricValue('vehiclesDown', data.vehicles_down);
        
    } catch (error) {
        console.error('Error fetching metrics:', error);
    }
}

/**
 * Update a metric value with smooth animation
 */
function updateMetricValue(elementId, newValue) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const currentValue = element.textContent.split(' ')[0]; // Get number part only
    
    // Only animate if value changed
    if (currentValue !== String(newValue)) {
        // Add pulse animation
        element.classList.add('metric-update');
        
        // Update value
        if (elementId === 'speed') {
            element.innerHTML = `${newValue} <span class="unit">km/h</span>`;
        } else {
            element.textContent = newValue;
        }
        
        // Remove animation class after animation completes
        setTimeout(() => {
            element.classList.remove('metric-update');
        }, 300);
    }
}

/**
 * Setup restart button functionality
 */
function setupRestartButton() {
    const restartBtn = document.getElementById('restartBtn');
    
    restartBtn.addEventListener('click', async function() {
        // Add loading state
        restartBtn.disabled = true;
        restartBtn.innerHTML = `
            <svg class="spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M23 4v6h-6M1 20v-6h6"/>
                <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
            </svg>
            Restarting...
        `;
        
        try {
            const response = await fetch('/restart');
            const data = await response.json();
            
            if (data.status === 'success') {
                // Show success feedback
                showNotification('Video restarted successfully', 'success');
            }
        } catch (error) {
            console.error('Error restarting video:', error);
            showNotification('Failed to restart video', 'error');
        } finally {
            // Reset button state
            setTimeout(() => {
                restartBtn.disabled = false;
                restartBtn.innerHTML = `
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M23 4v6h-6M1 20v-6h6"/>
                        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
                    </svg>
                    Restart
                `;
            }, 1000);
        }
    });
}

/**
 * Add CSS for number transitions
 */
function addNumberTransitions() {
    const style = document.createElement('style');
    style.textContent = `
        .metric-update {
            animation: metricPulse 0.3s ease-out;
        }
        
        @keyframes metricPulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.1);
                color: #6366f1;
            }
            100% {
                transform: scale(1);
            }
        }
        
        .spinner {
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            from {
                transform: rotate(0deg);
            }
            to {
                transform: rotate(360deg);
            }
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: rgba(30, 33, 57, 0.95);
            border-radius: 12px;
            border: 1px solid rgba(99, 102, 241, 0.3);
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            color: white;
            font-weight: 600;
            z-index: 1000;
            animation: slideInRight 0.3s ease-out, fadeOut 0.3s ease-out 2.7s;
        }
        
        .notification.success {
            border-color: #10b981;
        }
        
        .notification.error {
            border-color: #ef4444;
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes fadeOut {
            from {
                opacity: 1;
            }
            to {
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

/**
 * Show notification message
 */
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

/**
 * Handle video feed errors
 */
const videoFeed = document.getElementById('videoFeed');
if (videoFeed) {
    videoFeed.addEventListener('error', function() {
        console.error('Video feed error');
        showNotification('Video feed connection lost', 'error');
    });
}

/**
 * Cleanup on page unload
 */
window.addEventListener('beforeunload', function() {
    if (metricsUpdateInterval) {
        clearInterval(metricsUpdateInterval);
    }
});

/**
 * Add keyboard shortcuts
 */
document.addEventListener('keydown', function(event) {
    // Press 'R' to restart
    if (event.key === 'r' || event.key === 'R') {
        document.getElementById('restartBtn').click();
    }
});

// Log system info
console.log('%c🚦 Traffic Flow Analysis System', 'color: #6366f1; font-size: 20px; font-weight: bold;');
console.log('%cBuilt with YOLOv8 & Flask', 'color: #8b5cf6; font-size: 14px;');
console.log('%cKeyboard Shortcuts:', 'color: #10b981; font-size: 12px; font-weight: bold;');
console.log('%c  R - Restart video', 'color: #9ca3af; font-size: 12px;');
