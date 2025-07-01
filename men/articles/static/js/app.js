document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    const closeSidebar = document.querySelector('.close-sidebar');

    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }

    if (closeSidebar && sidebar) {
        closeSidebar.addEventListener('click', function() {
            sidebar.classList.remove('active');
        });
    }

    // Global Font Size Management
    // Load saved font size from localStorage
    const savedFontSize = localStorage.getItem('fontSize') || 'medium';
    applyGlobalFontSize(savedFontSize);

    // GLOBAL THEME MANAGEMENT (modular, FOUC engelleyici, hata loglu)
    (function() {
        function setGlobalTheme(theme) {
            try {
                if (theme === 'dark') {
                    document.documentElement.classList.add('dark');
                    localStorage.setItem('theme', 'dark');
                } else {
                    document.documentElement.classList.remove('dark');
                    localStorage.setItem('theme', 'light');
                }
            } catch (e) {
                console.error('Dark mode failed to apply', e);
            }
            // Buton aktifliklerini güncelle (tüm sayfalarda varsa)
            if (typeof window !== 'undefined') {
                var btns = document.querySelectorAll('.theme-btn');
                btns.forEach(function(btn) {
                    btn.classList.toggle('active', btn.getAttribute('data-theme') === theme);
                });
            }
        }
        function getGlobalTheme() {
            try {
                return localStorage.getItem('theme') || 'light';
            } catch (e) {
                console.error('localStorage read failed', e);
                return 'light';
            }
        }
        // FOUC engelle: HTML yüklenmeden önce temayı uygula
        var theme = getGlobalTheme();
        setGlobalTheme(theme);
        // Tüm sayfalarda erişilebilir yap
        window.setGlobalTheme = setGlobalTheme;
        window.getGlobalTheme = getGlobalTheme;
    })();
});

function applyGlobalFontSize(size) {
    // Remove all font size classes from body
    document.body.classList.remove('font-size-small', 'font-size-medium', 'font-size-large', 'font-size-extra-large');
    
    // Add the selected font size class
    document.body.classList.add(`font-size-${size}`);
}

// Function to be called from profile page
function updateGlobalFontSize(size) {
    applyGlobalFontSize(size);
    localStorage.setItem('fontSize', size);
} 