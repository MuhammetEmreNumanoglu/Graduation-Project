/**
 * Ortak Görev Servisi
 * Tüm üye sayfalarında tek kaynak olarak kullanılır
 * 
 * Görev tipleri → yönlendirme URL'leri:
 *   breathing_exercise  → /nefes-egzersizi
 *   meditation          → /meditasyon
 *   daily_cards         → /gunluk-kartlar
 *   support_wall        → /destek-duvari
 */

(function () {
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

    // Task type → URL route mapping
    const TASK_ROUTES = {
        breathing_exercise: '/nefes-egzersizi',
        meditation: '/meditasyon',
        daily_cards: '/gunluk-kartlar',
        support_wall: '/destek-duvari',
    };

    // Task type → Display name mapping (i18n via lang.js if available)
    const TASK_DISPLAY = {
        breathing_exercise: 'Nefes Egzersizi',
        meditation: 'Meditasyon',
        daily_cards: 'Günlük Kartlar',
        support_wall: 'Destek Duvarı',
    };

    // Task type → Emoji icon
    const TASK_ICONS = {
        breathing_exercise: '🌬️',
        meditation: '🧘',
        daily_cards: '🃏',
        support_wall: '🤝',
    };

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

    // Görevi tamamlandı olarak işaretle
    function completeTask(taskId, callback) {
        const fd = new FormData();
        fd.append('task_id', taskId);
        fetch('/api/member/complete-task/', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken },
            body: fd
        })
            .then(r => r.json())
            .then(data => {
                if (callback) callback(data.success);
            })
            .catch(() => {
                if (callback) callback(false);
            });
    }

    // Mevcut sayfanın URL'ine göre görevi tamamlandı işaretle
    function autoCompleteTaskForCurrentPage() {
        const path = window.location.pathname;
        fetchTasks().then(tasks => {
            tasks.forEach(task => {
                if (!task.is_completed) {
                    const route = TASK_ROUTES[task.text];
                    if (route && path.startsWith(route)) {
                        completeTask(task.id, null);
                    }
                }
            });
        });
    }

    // Görevleri sidebar'a render et (aktif + tamamlanan)
    function renderTasksToSidebar(tasks) {
        let taskListContainer = document.querySelector(
            '.sidebar-tasks, .sidebar-task-list, #sidebarTasks, #taskList, .tasks-list'
        );

        if (!taskListContainer) {
            const taskSection = document.querySelector('.sidebar-block h3, .sidebar-title-text');
            if (taskSection && (taskSection.textContent.includes('Görevlerim') || taskSection.textContent.includes('Görev') || taskSection.textContent.includes('Task'))) {
                const parent = taskSection.parentElement || taskSection.closest('.sidebar-block');
                if (parent) {
                    taskListContainer = parent.querySelector('.sidebar-tasks, .sidebar-task-list');
                    if (!taskListContainer) {
                        const listContainer = document.createElement('div');
                        listContainer.className = 'sidebar-tasks';
                        listContainer.id = 'sidebarTasks';
                        parent.appendChild(listContainer);
                        taskListContainer = listContainer;
                    }
                }
            }
            if (!taskListContainer) return;
        }

        taskListContainer.innerHTML = '';
        const lang = localStorage.getItem('selectedLanguage') || 'tr';

        function t(key) {
            if (window.translations && window.translations[lang] && window.translations[lang][key]) {
                return window.translations[lang][key];
            }
            return key;
        }

        if (tasks && tasks.length > 0) {
            const pending = tasks.filter(t => !t.is_completed);
            const completed = tasks.filter(t => t.is_completed);

            pending.forEach(task => {
                const route = TASK_ROUTES[task.text] || '#';
                const icon = TASK_ICONS[task.text] || '📝';
                const baseLabel = TASK_DISPLAY[task.text] || task.text;
                const label = t(baseLabel);

                const taskItem = document.createElement('div');
                taskItem.className = 'sidebar-task-item';
                taskItem.setAttribute('data-task-id', task.id);
                taskItem.style.cursor = 'pointer';
                taskItem.innerHTML = `
                    <span style="font-size:1.1rem;margin-right:6px;">${icon}</span>
                    <span class="task-text" style="flex:1;" data-translate="${baseLabel}">${escapeHtml(label)}</span>
                    <span style="font-size:0.7rem;color:#8b5cf6;margin-left:4px;">→</span>
                `;
                taskItem.addEventListener('click', function () {
                    window.location.href = route;
                });
                taskListContainer.appendChild(taskItem);
            });

            if (completed.length > 0) {
                const divider = document.createElement('div');
                divider.style.cssText = 'border-top:1px solid #ede9fe;margin:8px 0 6px 0;font-size:0.7rem;color:#9ca3af;font-weight:600;';
                divider.setAttribute('data-translate', 'Tamamlananlar');
                divider.textContent = t('Tamamlananlar');
                taskListContainer.appendChild(divider);

                completed.forEach(task => {
                    const icon = TASK_ICONS[task.text] || '📝';
                    const baseLabel = TASK_DISPLAY[task.text] || task.text;
                    const label = t(baseLabel);

                    const taskItem = document.createElement('div');
                    taskItem.className = 'sidebar-task-item';
                    taskItem.setAttribute('data-task-id', task.id);
                    taskItem.style.opacity = '0.55';
                    taskItem.innerHTML = `
                        <span style="font-size:1.1rem;margin-right:6px;">${icon}</span>
                        <span class="task-text" style="flex:1;text-decoration:line-through;" data-translate="${baseLabel}">${escapeHtml(label)}</span>
                        <span class="task-completed" style="color:#16a34a;font-weight:700;">✓</span>
                    `;
                    taskListContainer.appendChild(taskItem);
                });
            }
        } else {
            const emptyItem = document.createElement('div');
            emptyItem.className = 'sidebar-task-item';
            emptyItem.style.opacity = '0.6';
            emptyItem.setAttribute('data-translate', 'Henüz görev yok.');
            emptyItem.textContent = t('Henüz görev yok.');
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
        init: function () {
            loadAndRenderTasks();
            autoCompleteTaskForCurrentPage();

            // Polling - her 10 saniyede güncelle
            setInterval(() => {
                if (!document.hidden) {
                    loadAndRenderTasks();
                }
            }, 10000);
        },
        fetchTasks: fetchTasks,
        renderTasksToSidebar: renderTasksToSidebar,
        loadAndRenderTasks: loadAndRenderTasks,
        completeTask: completeTask,
    };

    // Sayfa yüklendiğinde otomatik başlat
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function () {
            window.TasksService.init();
        });
    } else {
        window.TasksService.init();
    }
})();
