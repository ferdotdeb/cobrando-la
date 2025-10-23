async function copyText(text) {
    try {
        await navigator.clipboard.writeText((text || "").trim());
        // Mostrar notificación de éxito
        const notification = document.createElement('div');
        notification.className = 'fixed bottom-4 right-4 z-50 px-6 py-3 rounded-xl bg-green-500/90 text-white font-medium shadow-lg transform transition-all duration-300';
        notification.innerHTML = '<div class="flex items-center gap-2"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg><span>¡Copiado al portapapeles!</span></div>';
        document.body.appendChild(notification);
        setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }, 2000);
    } catch (e) {
        console.error(e);
        alert("Error al copiar. Por favor, intenta de nuevo.");
    }
}