/**
 * Public Profile JavaScript
 * Handles QR code generation, clipboard operations, and UI interactions
 */

// Toast system con Tailwind
function showToast(message, isError = false) {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  
  // Aplicar clases según tipo
  if (isError) {
    toast.className = 'fixed bottom-4 right-4 z-50 px-6 py-3 rounded-xl bg-red-500/90 text-white font-medium shadow-lg transform transition-all duration-300 opacity-100 translate-y-0';
  } else {
    toast.className = 'fixed bottom-4 right-4 z-50 px-6 py-3 rounded-xl bg-green-500/90 text-white font-medium shadow-lg transform transition-all duration-300 opacity-100 translate-y-0';
  }
  
  // Ocultar después de 2.5s
  setTimeout(() => {
    toast.className = 'fixed bottom-4 right-4 z-50 px-6 py-3 rounded-xl bg-green-500/90 text-white font-medium shadow-lg transform transition-all duration-300 opacity-0 translate-y-2 pointer-events-none';
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
      showToast('¡Copiado al portapapeles!');
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
        showToast('¡Copiado al portapapeles!');
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
    showToast('Enlace público copiado');
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
      container.innerHTML = '<p class="text-red-400 p-5">La librería QR no se cargó correctamente</p>';
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
    container.innerHTML = '<p class="text-red-400 p-5">Error al generar el código QR</p>';
  }
}

// Toggle QR modal con Tailwind
function toggleQR() {
  const modal = document.getElementById('qr-modal');
  const content = modal.querySelector('.relative');
  
  // Check si está visible
  const isShowing = !modal.classList.contains('pointer-events-none');
  
  if (isShowing) {
    // Ocultar con animación
    modal.classList.add('opacity-0');
    content.classList.add('scale-95');
    setTimeout(() => {
      modal.classList.add('pointer-events-none');
    }, 300);
  } else {
    // Mostrar con animación
    modal.classList.remove('pointer-events-none');
    setTimeout(() => {
      modal.classList.remove('opacity-0');
      content.classList.remove('scale-95');
    }, 10);
    
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
    if (!modal.classList.contains('pointer-events-none')) {
      toggleQR();
    }
  }
});
