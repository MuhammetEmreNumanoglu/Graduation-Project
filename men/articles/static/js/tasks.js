/**
 * Ortak Görev Servisi
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
    
    // Görevleri yükle
    function fetchTasks() {
        return fetch("/api/get-user-tasks/", {
            method: "GET",
            headers: { "X-CSRFToken": csrfToken }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                return data.tasks || [];
            }
            return [];
        })
        .catch(error => {
            console.error("Görevler yüklenemedi:", error);
            return [];
        });
    }
    
    // Görevleri sidebar'a render et
    function renderTasksToSidebar(tasks) {
        // Sidebar'daki görev listesi container'ını bul
        let taskListContainer = document.querySelector('.sidebar-tasks, .sidebar-task-list, #sidebarTasks, #taskList, .tasks-list');
        if (!taskListContainer) {
            // Eğer container yoksa, sidebar'daki görevlerim bölümünü bul
            const taskSection = document.querySelector('.sidebar-block h3, .sidebar-title-text');
            if (taskSection && (taskSection.textContent.includes('Görevlerim') || taskSection.textContent.includes('Görev'))) {
                // Görevlerim başlığının parent'ını bul
                const parent = taskSection.parentElement || taskSection.closest('.sidebar-block');
                if (parent) {
                    // Mevcut container'ı kontrol et
                    taskListContainer = parent.querySelector('.sidebar-tasks, .sidebar-task-list');
                    if (!taskListContainer) {
                        const listContainer = document.createElement('div');
                        listContainer.className = 'sidebar-tasks';
                        parent.appendChild(listContainer);
                        taskListContainer = listContainer;
                    }
                }
            }
            if (!taskListContainer) {
                return; // Container bulunamadı, sessizce çık
            }
        }
        
        // Liste boşalt
        taskListContainer.innerHTML = '';
        
        // Görevleri yeni->eski sıralı (zaten backend'den sıralı geliyor)
        if (tasks && tasks.length > 0) {
            tasks.forEach(task => {
                const taskItem = document.createElement('div');
                taskItem.className = 'sidebar-task-item';
                taskItem.setAttribute('data-task-id', task.id);
                taskItem.innerHTML = `
                    <span class="task-text">${escapeHtml(task.text)}</span>
                    ${task.is_completed ? '<span class="task-completed">✓</span>' : ''}
                `;
                taskListContainer.appendChild(taskItem);
            });
        } else {
            // Henüz görev yok
            const emptyItem = document.createElement('div');
            emptyItem.className = 'sidebar-task-item';
            emptyItem.style.opacity = '0.6';
            emptyItem.textContent = 'Henüz görev yok';
            taskListContainer.appendChild(emptyItem);
        }
    }
    
    // HTML escape helper
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    // Görevleri yükle ve render et
    function loadAndRenderTasks() {
        fetchTasks().then(tasks => {
            renderTasksToSidebar(tasks);
        });
    }
    
    // Public API
    window.TasksService = {
        init: function() {
            loadAndRenderTasks();
            
            // Polling - görevler güncellendiğinde otomatik yükle
            setInterval(() => {
                if (!document.hidden) {
                    loadAndRenderTasks();
                }
            }, 10000); // 10 saniyede bir güncelle
        },
        fetchTasks: fetchTasks,
        renderTasksToSidebar: renderTasksToSidebar,
        loadAndRenderTasks: loadAndRenderTasks
    };
    
    // Sayfa yüklendiğinde otomatik başlat
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            window.TasksService.init();
        });
    } else {
        window.TasksService.init();
    }
})();
