// Responsive Sidebar JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Hamburger menu functionality
    const hamburger = document.querySelector('.hamburger');
    const sidebarContainer = document.querySelector('.sidebar-container');
    const body = document.body;
    
    // Create overlay if it doesn't exist
    let overlay = document.querySelector('.sidebar-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'sidebar-overlay';
        document.body.appendChild(overlay);
    }
    
    // Hamburger click handler
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            sidebarContainer.classList.toggle('active');
            body.classList.toggle('sidebar-open');
            overlay.classList.toggle('active');
        });
    }
    
    // Overlay click handler
    overlay.addEventListener('click', function() {
        hamburger.classList.remove('active');
        sidebarContainer.classList.remove('active');
        body.classList.remove('sidebar-open');
        overlay.classList.remove('active');
    });
    
    // Close sidebar on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            hamburger.classList.remove('active');
            sidebarContainer.classList.remove('active');
            body.classList.remove('sidebar-open');
            overlay.classList.remove('active');
        }
    });
    
    // Handle window resize
    window.addEventListener('resize', function() {
        if (window.innerWidth > 1200) {
            hamburger.classList.remove('active');
            sidebarContainer.classList.remove('active');
            body.classList.remove('sidebar-open');
            overlay.classList.remove('active');
        }
    });
    
    // Add hamburger menu to pages that don't have it
    if (!hamburger && sidebarContainer) {
        const newHamburger = document.createElement('button');
        newHamburger.className = 'hamburger';
        newHamburger.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        document.body.appendChild(newHamburger);
        
        newHamburger.addEventListener('click', function() {
            newHamburger.classList.toggle('active');
            sidebarContainer.classList.toggle('active');
            body.classList.toggle('sidebar-open');
            overlay.classList.toggle('active');
        });
    }
    
    // Ensure sidebar sections have the dashboard style
    const sidebarSections = document.querySelectorAll('.sidebar-section');
    sidebarSections.forEach(section => {
        const h3 = section.querySelector('h3');
        if (h3 && h3.style) {
            if (!h3.style.getPropertyValue('--before-content')) {
            h3.style.setProperty('--before-content', '');
            }
        }
    });
    
    // Ensure sidebar blocks have the dashboard style
    const sidebarBlocks = document.querySelectorAll('.sidebar-block');
    sidebarBlocks.forEach(block => {
        const h3 = block.querySelector('h3');
        if (h3 && h3.style) {
            if (!h3.style.getPropertyValue('--before-content')) {
            h3.style.setProperty('--before-content', '');
            }
        }
    });
    
    // Add smooth transitions to all sidebar elements
    const sidebarElements = document.querySelectorAll('.sidebar-container, .sidebar-header, .sidebar-user, .sidebar-menu, .sidebar-sections, .sidebar-section, .sidebar-block, .menu-item');
    sidebarElements.forEach(element => {
        if (element && element.style) {
        element.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        }
    });
    
    // Prevent content from overlapping sidebar
    const mainContent = document.querySelector('.main-content');
    if (mainContent) {
        mainContent.style.position = 'relative';
        mainContent.style.zIndex = '1';
    }
    
    // Ensure sidebar is always on top
    if (sidebarContainer) {
        sidebarContainer.style.zIndex = '1000';
    }
    
    // Add responsive behavior to menu items
    const menuItems = document.querySelectorAll('.menu-item');
    menuItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(4px)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
    
    // Add hover effects to sidebar sections and blocks
    const sidebarElementsWithHover = document.querySelectorAll('.sidebar-section, .sidebar-block');
    sidebarElementsWithHover.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.boxShadow = '0 4px 16px rgba(139, 92, 246, 0.1)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
            this.style.boxShadow = '0 2px 8px rgba(139, 92, 246, 0.05)';
        });
    });
    
    // Handle active menu items
    const currentPath = window.location.pathname;
    menuItems.forEach(item => {
        const link = item.getAttribute('href');
        if (link && currentPath.includes(link)) {
            item.classList.add('active');
        }
    });
    
    // Add loading animation
    window.addEventListener('load', function() {
        if (sidebarContainer) {
            sidebarContainer.style.opacity = '0';
            sidebarContainer.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                sidebarContainer.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
                sidebarContainer.style.opacity = '1';
                sidebarContainer.style.transform = 'translateX(0)';
            }, 100);
        }
    });
    
    // Handle touch events for mobile
    let touchStartX = 0;
    let touchEndX = 0;
    
    document.addEventListener('touchstart', function(e) {
        touchStartX = e.changedTouches[0].screenX;
    });
    
    document.addEventListener('touchend', function(e) {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    });
    
    function handleSwipe() {
        const swipeThreshold = 50;
        const swipeDistance = touchEndX - touchStartX;
        
        if (Math.abs(swipeDistance) > swipeThreshold) {
            if (swipeDistance > 0 && touchStartX < 50) {
                // Swipe right from left edge - open sidebar
                if (hamburger && !sidebarContainer.classList.contains('active')) {
                    hamburger.click();
                }
            } else if (swipeDistance < 0 && sidebarContainer.classList.contains('active')) {
                // Swipe left - close sidebar
                hamburger.click();
            }
        }
    }
    
    // Add keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'b') {
            e.preventDefault();
            if (hamburger) {
                hamburger.click();
            }
        }
    });
    
    // Auto-hide sidebar on mobile when clicking outside
    if (window.innerWidth <= 1200) {
        document.addEventListener('click', function(e) {
            if (!sidebarContainer.contains(e.target) && 
                !hamburger.contains(e.target) && 
                sidebarContainer.classList.contains('active')) {
                hamburger.click();
            }
        });
    }
    
    // Add scroll lock when sidebar is open on mobile
    function toggleScrollLock(lock) {
        if (lock) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
    
    // Update scroll lock when sidebar state changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && mutation.attributeName === 'class') {
                const isOpen = body.classList.contains('sidebar-open');
                toggleScrollLock(isOpen && window.innerWidth <= 1200);
            }
        });
    });
    
    observer.observe(body, {
        attributes: true,
        attributeFilter: ['class']
    });
    
    // Initialize scroll lock state
    toggleScrollLock(body.classList.contains('sidebar-open') && window.innerWidth <= 1200);
}); 