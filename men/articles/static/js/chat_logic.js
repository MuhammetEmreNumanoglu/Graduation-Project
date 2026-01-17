// Bu dosya, AI sohbet arayüzünün tüm mantığını yönetir.
document.addEventListener("DOMContentLoaded", function () {
    // --- Gerekli HTML Elementlerini Seçme ---
    const chatForm = document.getElementById("chatForm");
    const messageInput = document.getElementById("messageInput");
    const chatMessages = document.getElementById("chatMessages");
    const newChatBtn = document.getElementById("newChatBtn");
    
    let history_id = null; // Aktif sohbetin ID'sini tutar
    const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

    // --- Ana Fonksiyonlar ---

    /**
     * Sohbet ekranına yeni bir mesaj balonu ekler (kullanıcı veya bot için).
     * @param {string} text - Mesaj metni.
     * @param {string} sender - 'user' veya 'bot'.
     */
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        // Yükleniyor animasyonu için özel bir sınıf ekliyoruz
        const senderClass = sender === 'bot-loading' ? 'bot-message bot-loading-message' : `${sender}-message`;
        messageDiv.className = `message ${senderClass}`;
        
        const now = new Date();
        const time = now.toLocaleTimeString('tr-TR', { hour: '2-digit', minute: '2-digit', hour12: false });

        const htmlContent = marked.parse(text);
        
        messageDiv.innerHTML = `
            <div class="message-content">${htmlContent}</div>
            <div class="message-time">${time}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    /**
     * AI'dan gelen eylem önerilerini işler ve butonları oluşturur.
     * @param {object} action - AI'dan gelen suggested_action objesi.
     */
    function handleSuggestedAction(action) {
        if (!action) return;
        const existingActionButtons = document.querySelectorAll('.action-buttons');
        existingActionButtons.forEach(btn => btn.remove());

        const actionContainer = document.createElement('div');
        actionContainer.className = 'action-buttons';
        
        switch (action.action_type) {
            case 'NAVIGATE_TO_PAGE':
                actionContainer.innerHTML = `<button class="action-btn" data-action="navigate" data-page-name="${action.action_payload.pageName}">Evet, Lütfen</button><button class="action-btn cancel" data-action="cancel">Hayır, Teşekkürler</button>`;
                break;
            case 'CREATE_TASK':
                actionContainer.innerHTML = `<button class="action-btn" data-action="create-task" data-task-name="${action.action_payload.taskName}" data-task-details="${action.action_payload.taskDetails}">Görevi Ekle</button><button class="action-btn cancel" data-action="cancel">İstemiyorum</button>`;
                break;
        }

        const lastBotMessage = chatMessages.querySelector('.bot-message:last-child');
        if (lastBotMessage) {
            lastBotMessage.querySelector('.message-content').appendChild(actionContainer);
        }
    }

    // --- Olay Dinleyicileri (Event Listeners) ---

    // Mesaj gönderme formu
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const message = messageInput.value.trim();
    
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            
            const existingActionButtons = document.querySelectorAll('.action-buttons');
            existingActionButtons.forEach(btn => btn.remove());

            addMessage('<p>Yazıyor...</p>', 'bot-loading');

            fetch("/llm_api/stream", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
                body: JSON.stringify({ message: message, history_id: history_id })
            })
            .then(response => {
                if (!response.ok) throw new Error("Yanıt alınamadı");
                return response.json();
            })
            .then(data => {
                const loadingMessage = chatMessages.querySelector('.bot-loading-message');
                if(loadingMessage) loadingMessage.remove();
                
                history_id = data.history_id;
                addMessage(data.reply_text, "bot");

                if (data.suggested_action) {
                    handleSuggestedAction(data.suggested_action);
                }
            })
            .catch(error => {
                const loadingMessage = chatMessages.querySelector('.bot-loading-message');
                if(loadingMessage) loadingMessage.remove();
                console.error("Hata:", error);
                addMessage("Bir hata oluştu. Lütfen tekrar deneyin.", "bot");
            });
        }
    });

    // Eylem butonlarına tıklamaları yöneten genel event listener
    document.addEventListener('click', function(e) {
        if (!e.target.classList.contains('action-btn')) return;
        const button = e.target;
        const action = button.dataset.action;

        if (action === 'navigate') {
            const pageName = button.dataset.pageName;
            // pageUrls değişkeni HTML dosyasında global olarak tanımlanmalıdır.
            if (window.pageUrls && window.pageUrls[pageName]) {
                window.location.href = window.pageUrls[pageName];
            } else {
                console.error('Bilinmeyen sayfa adı:', pageName);
            }
        } 
        else if (action === 'create-task') {
            const taskName = button.dataset.taskName;
            alert(`'${taskName}' görevi eklendi!`);
        }
        
        const buttonContainer = button.closest('.action-buttons');
        if (buttonContainer) buttonContainer.remove();
    });

    // Yeni sohbet butonu
    newChatBtn.addEventListener("click", function () {
        history_id = null;
        chatMessages.innerHTML = '';
        addMessage('Merhaba! Size nasıl yardımcı olabilirim?', 'bot');
    });

    // Başlangıçta ilk bot mesajını ekle
    addMessage('Merhaba! Size nasıl yardımcı olabilirim?', 'bot');
});