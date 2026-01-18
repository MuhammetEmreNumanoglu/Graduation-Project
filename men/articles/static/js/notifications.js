/**
 * Ortak Bildirim Servisi
 * Tüm üye sayfalarında tek kaynak olarak kullanılır
 */

(function() {
    'use strict';
    
    // CSRF token helper
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const csrfToken = getCookie('csrftoken');
    
    // Badge elementi oluştur (yoksa) ve click handler'ları ekle
    function ensureBadgeElement() {
        let notificationBell = document.getElementById('notificationBell');
        let popup = document.getElementById('notificationPopup');
        
        if (!notificationBell) {
            // Notification bell yoksa oluştur
            notificationBell = document.createElement('button');
            notificationBell.id = 'notificationBell';
            notificationBell.className = 'notification-bell';
            notificationBell.setAttribute('aria-label', 'Bildirimler');
            notificationBell.innerHTML = '<span class="material-symbols-outlined">notifications</span>';
            document.body.appendChild(notificationBell);
        }
        
        if (!popup) {
            // Popup yoksa oluştur
            popup = document.createElement('div');
            popup.id = 'notificationPopup';
            popup.className = 'notification-popup';
            popup.innerHTML = `
                <div class="popup-title">Bildirimler</div>
                <ul class="notification-list" id="notificationList"></ul>
            `;
            document.body.appendChild(popup);
        }
        
        // Click handler ekle (sadece bir kez)
        if (!notificationBell._notificationsHandlerAdded) {
            notificationBell.addEventListener('click', function(e) {
                e.stopPropagation();
                const currentPopup = document.getElementById('notificationPopup');
                if (currentPopup) {
                    currentPopup.classList.toggle('active');
                    if (currentPopup.classList.contains('active')) {
                        // Popup açıldığında bildirimleri yükle ve okundu işaretle
                        loadNotifications();
                        markNotificationsRead();
                    }
                }
            });
            
            // Dışarı tıklayınca kapat
            document.addEventListener('click', function(e) {
                const currentPopup = document.getElementById('notificationPopup');
                const currentBell = document.getElementById('notificationBell');
                if (currentPopup && currentPopup.classList.contains('active') && 
                    !currentPopup.contains(e.target) && e.target !== currentBell) {
                    currentPopup.classList.remove('active');
                }
            });
            
            notificationBell._notificationsHandlerAdded = true;
        }
        
        let badge = document.getElementById('unreadBadge');
        if (!badge) {
            badge = document.createElement('span');
            badge.id = 'unreadBadge';
            badge.className = 'unread-badge';
            notificationBell.appendChild(badge);
        }
        return badge;
    }
    
    // Badge güncelleme
    function updateBadges() {
        fetch("/api/member/badges/", {
            method: "GET",
            headers: { "X-CSRFToken": csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const badge = ensureBadgeElement();
                const total = data.total || 0;
                
                if (total > 0) {
                    badge.textContent = total > 99 ? '99+' : total;
                    badge.style.display = 'flex';
                } else {
                    badge.style.display = 'none';
                }
            }
        })
        .catch(error => console.error("Badge sayıları yüklenemedi:", error));
    }
    
    // Bildirimleri yükle
    function loadNotifications() {
        fetch("/api/get-user-notifications/", {
            method: "GET",
            headers: { "X-CSRFToken": csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const list = document.getElementById('notificationList');
                if (list) {
                    list.innerHTML = '';
                    if (data.notifications && data.notifications.length > 0) {
                        data.notifications.forEach(notif => {
                            const item = document.createElement('li');
                            item.className = 'notification-item';
                            item.textContent = notif.text;
                            list.appendChild(item);
                        });
                    } else {
                        const item = document.createElement('li');
                        item.className = 'notification-item';
                        item.style.opacity = '0.6';
                        item.textContent = 'Henüz bildirim yok';
                        list.appendChild(item);
                    }
                }
            }
        })
        .catch(error => console.error("Bildirimler yüklenemedi:", error));
    }
    
    // Bildirimleri okundu işaretle
    function markNotificationsRead() {
        fetch("/api/member/mark-notifications-read/", {
            method: "POST",
            headers: { "X-CSRFToken": csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateBadges();
            }
        })
        .catch(error => console.error("Bildirimler okundu işaretlenemedi:", error));
    }
    
    // Public API
    window.NotificationsService = {
        init: function() {
            ensureBadgeElement();
            updateBadges();
            loadNotifications();
            
            // Badge polling - 5 saniyede bir güncelle
            setInterval(() => {
                if (!document.hidden) {
                    updateBadges();
                }
            }, 5000);
        },
        updateBadges: updateBadges,
        loadNotifications: loadNotifications,
        markNotificationsRead: markNotificationsRead
    };
    
    // Sayfa yüklendiğinde otomatik başlat
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            window.NotificationsService.init();
        });
    } else {
        window.NotificationsService.init();
    }
})();

