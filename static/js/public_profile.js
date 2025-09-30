/**
 * Public Profile JavaScript
 * Handles QR code generation, clipboard operations, and UI interactions
 */

// Toast system
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = 'toast' + (isError ? ' error' : '');
  
  // Force reflow
  void toast.offsetWidth;
  
  toast.classList.add('show');
  
  setTimeout(() => {
    toast.classList.remove('show');
  }, 2500);
}

// Copy text to clipboard
async function copyText(text) {
  if (!text) {
    showToast('No hay texto para copiar', true);
    return;
  }

  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      await navigator.clipboard.writeText(text);
      showToast('¡Copiado!');
    } else {
      // Fallback for older browsers
      const textarea = document.createElement('textarea');
      textarea.value = text;
      textarea.style.position = 'fixed';
      textarea.style.opacity = '0';
      document.body.appendChild(textarea);
      textarea.select();
      const success = document.execCommand('copy');
      document.body.removeChild(textarea);
      
      if (success) {
        showToast('¡Copiado!');
      } else {
        showToast('Error al copiar', true);
      }
    }
  } catch (err) {
    showToast('Error al copiar', true);
  }
}

// Copy public link
async function copyPublicLink() {
  const publicUrl = window.PUBLIC_URL;
  await copyText(publicUrl);
  if (publicUrl) {
    showToast('Enlace copiado');
  }
}

// QR Code Generator using QRCode.js
let qrCodeInstance = null;

function generateQR(text) {
  if (!text) {
    return;
  }

  const container = document.getElementById('qr-container');
  
  // Clear previous QR code
  container.innerHTML = '';
  
  // Generate new QR code
  try {
    // Check if QRCode is available
    if (typeof QRCode === 'undefined') {
      container.innerHTML = '<p style="color: #dc2626; padding: 20px;">La librería QR no se cargó correctamente</p>';
      return;
    }

    qrCodeInstance = new QRCode(container, {
      text: text,
      width: 256,
      height: 256,
      colorDark: '#000000',
      colorLight: '#ffffff',
      correctLevel: QRCode.CorrectLevel.M
    });
  } catch (error) {
    console.error('Error generating QR:', error);
    container.innerHTML = '<p style="color: #dc2626; padding: 20px;">Error al generar el código QR</p>';
  }
}

// Toggle QR modal
function toggleQR() {
  const modal = document.getElementById('qr-modal');
  const isShowing = modal.classList.contains('show');
  
  if (isShowing) {
    modal.classList.remove('show');
  } else {
    modal.classList.add('show');
    // Generate QR on first open or regenerate if needed
    if (!qrCodeInstance) {
      generateQR(window.PUBLIC_URL);
    }
  }
}

// Close QR if clicking backdrop
function closeQRIfBackdrop(event) {
  if (event.target.id === 'qr-modal') {
    toggleQR();
  }
}

// Close QR with Escape key
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const modal = document.getElementById('qr-modal');
    if (modal.classList.contains('show')) {
      toggleQR();
    }
  }
});
