// MENÚ MÓVIL
        (function() {
            const mobileMenuBtn = document.getElementById('mobile-menu-btn');
            const mobileMenu = document.getElementById('mobile-menu');
            const menuIcon = document.getElementById('menu-icon');
            const closeIcon = document.getElementById('close-icon');

            if (mobileMenuBtn && mobileMenu) {
                mobileMenuBtn.addEventListener('click', function() {
                    const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
                    
                    mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);
                    mobileMenu.classList.toggle('hidden');
                    
                    if (menuIcon && closeIcon) {
                        menuIcon.classList.toggle('hidden');
                        closeIcon.classList.toggle('hidden');
                    }
                });

                // Soporte teclado (Enter y Espacio)
                mobileMenuBtn.addEventListener('keydown', function(e) {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        mobileMenuBtn.click();
                    }
                });
            }
        })();

        // Smooth scroll para navegación (opcional, mejora UX)
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId !== '#' && targetId.length > 1) {
                    const targetElement = document.querySelector(targetId);
                    if (targetElement) {
                        e.preventDefault();
                        
                        // Cerrar menú móvil si está abierto
                        const mobileMenu = document.getElementById('mobile-menu');
                        const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                        if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                            mobileMenu.classList.add('hidden');
                            mobileMenuBtn.setAttribute('aria-expanded', 'false');
                        }
                        
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });