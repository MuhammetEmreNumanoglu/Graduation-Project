// Global Font Size Manager
class FontSizeManager {
    constructor() {
        this.fontSizes = {
            'small': '0.875',
            'normal': '1',
            'large': '1.125',
            'very-large': '1.25'
        };
        
        this.init();
    }
    
    init() {
        // Load saved font size from localStorage
        const savedFontSize = localStorage.getItem('fontSize') || 'normal';
        this.applyFontSize(savedFontSize);
        
        // Set up event listeners for font size buttons
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Find all font size buttons
        const fontSizeBtns = document.querySelectorAll('.font-size-btn, [data-size]');
        
        fontSizeBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const size = btn.dataset.size || btn.getAttribute('data-size');
                if (size && this.fontSizes[size]) {
                    this.applyFontSize(size);
                    this.updateActiveButton(btn);
                    this.saveFontSize(size);
                    this.showToast(size);
                }
            });
        });
        
        // Update active button on page load
        this.updateActiveButtonOnLoad();
    }
    
    applyFontSize(size) {
        // Set the global --font-scale variable
        const scale = this.fontSizes[size] || '1';
        document.documentElement.style.setProperty('--font-scale', scale);
        document.documentElement.setAttribute('data-font-size', size);
    }
    
    updateActiveButton(clickedBtn) {
        // Remove active class from all font size buttons
        const allBtns = document.querySelectorAll('.font-size-btn, [data-size]');
        allBtns.forEach(btn => btn.classList.remove('active'));
        
        // Add active class to clicked button
        clickedBtn.classList.add('active');
    }
    
    updateActiveButtonOnLoad() {
        const savedFontSize = localStorage.getItem('fontSize') || 'normal';
        const activeBtn = document.querySelector(`[data-size="${savedFontSize}"]`);
        if (activeBtn) {
            this.updateActiveButton(activeBtn);
        }
    }
    
    saveFontSize(size) {
        localStorage.setItem('fontSize', size);
    }
    
    showToast(size) {
        const sizeNames = {
            'small': 'Small',
            'normal': 'Normal',
            'large': 'Large',
            'very-large': 'Very Large'
        };
        
        const sizeName = sizeNames[size] || size;
        
        // Get current language
        const currentLang = localStorage.getItem('selectedLanguage') || 'tr';
        
        // Use global getTranslation function if available
        let titleText, messageText;
        if (typeof getTranslation === 'function') {
            titleText = getTranslation('Font Size');
            messageText = getTranslation('size set to');
        } else {
            // Fallback translations
            const translations = {
                tr: {
                    'Font Size': 'Yazı Tipi Boyutu',
                    'size set to': 'boyutuna ayarlandı'
                },
                en: {
                    'Font Size': 'Font Size',
                    'size set to': 'size set to'
                }
            };
            
            const lang = translations[currentLang] || translations.tr;
            titleText = lang['Font Size'];
            messageText = lang['size set to'];
        }
        
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast success';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            border-radius: 8px;
            padding: 16px 20px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
        `;
        toast.innerHTML = `
            <div style="font-weight: 600; margin-bottom: 4px;">${titleText}</div>
            <div style="color: #666;">${sizeName} ${messageText}</div>
        `;
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => {
            toast.style.transform = 'translateX(0)';
        }, 100);
        
        // Hide toast after 3 seconds
        setTimeout(() => {
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (toast.parentNode) {
                    toast.parentNode.removeChild(toast);
                }
            }, 300);
        }, 3000);
    }
    
    // Public method to get current font size
    getCurrentFontSize() {
        return localStorage.getItem('fontSize') || 'normal';
    }
    
    // Public method to set font size programmatically
    setFontSize(size) {
        if (this.fontSizes[size]) {
            this.applyFontSize(size);
            this.saveFontSize(size);
        }
    }
}

// Initialize font size manager when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.fontSizeManager = new FontSizeManager();
});

// Also initialize immediately if DOM is already loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        window.fontSizeManager = new FontSizeManager();
    });
} else {
    window.fontSizeManager = new FontSizeManager();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FontSizeManager;
} 