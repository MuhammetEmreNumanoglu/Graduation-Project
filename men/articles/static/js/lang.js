// Dinamik dil değiştirme sistemi
const translations = {
    tr: {
        // Profile Management sayfası çevirileri
        "My Statistics": "İstatistiklerim",
        "Track your progress and see how you're doing with your mental health journey.": "İlerlemenizi takip edin ve ruh sağlığı yolculuğunuzda nasıl olduğunuzu görün.",
        "Days Active": "Aktif Günler",
        "Chat Sessions": "Sohbet Seansları",
        "Mood Score": "Ruh Hali Puanı",
        "Completed Tasks": "Tamamlanan Görevler",
        "Edit Profile": "Profili Düzenle",
        "Click or drag to upload your profile photo": "Profil fotoğrafınızı yüklemek için tıklayın veya sürükleyin",
        "Select Photo": "Fotoğraf Seç",
        "Username": "Kullanıcı Adı",
        "Email": "E-posta",
        "First Name": "Ad",
        "Enter your first name": "Adınızı girin",
        "Last Name": "Soyad",
        "Enter your last name": "Soyadınızı girin",
        "Save Changes": "Değişiklikleri Kaydet",
        "Settings": "Ayarlar",
        "Language Selection": "Dil Seçimi",
        "Set language across the site": "Site genelinde dil ayarlayın",
        "Turkish": "Türkçe",
        "English": "English",
        "User Information": "Kullanıcı Bilgileri",
        "Update Information": "Bilgileri Güncelle",
        "Change Password": "Şifre Değiştir",
        "Current Password": "Mevcut Şifre",
        "New Password": "Yeni Şifre",
        "Confirm New Password": "Yeni Şifre (Tekrar)",
        "Profile Photo": "Profil Fotoğrafı",
        "Update Photo": "Fotoğrafı Güncelle",
        "Font Size": "Yazı Tipi Boyutu",
        "Adjust font size across the site": "Site genelinde yazı boyutunu ayarlayın",
        "Small": "Küçük",
        "Normal": "Normal",
        "Large": "Büyük",
        "Very Large": "Çok Büyük",
        "Help Center": "Yardım Merkezi",
        "Find answers to common questions and get support when you need it.": "Sık sorulan soruların cevaplarını bulun ve ihtiyacınız olduğunda destek alın.",
        "Frequently Asked Questions": "Sık Sorulan Sorular",
        "How can I change my password?": "Şifremi nasıl değiştirebilirim?",
        "How do I update my profile picture?": "Profil fotoğrafımı nasıl güncelleyebilirim?",
        "What are the privacy settings?": "Gizlilik ayarları nelerdir?",
        "How can I contact support?": "Destek ile nasıl iletişime geçebilirim?",
        "Visit Help Center": "Yardım Merkezini Ziyaret Et",
        "Delete Account": "Hesabı Sil",
        "This action cannot be undone. All your data will be permanently deleted.": "Bu işlem geri alınamaz. Tüm verileriniz kalıcı olarak silinecek.",
        "Type 'DELETE MY ACCOUNT' to confirm": "Onay için 'HESABIMI SİL' yazınız",
        "Permanently Delete My Account": "Hesabımı Kalıcı Olarak Sil",
        "Please fill in all fields.": "Lütfen tüm alanları doldurun.",
        "New passwords do not match.": "Yeni şifreler eşleşmiyor.",
        "New password cannot be the same as current password.": "Yeni şifre mevcut şifre ile aynı olamaz.",
        "Password updated successfully!": "Şifre başarıyla güncellendi!",
        "Please type DELETE MY ACCOUNT to confirm.": "Onay için 'HESABIMI SİL' yazınız.",
        "This action cannot be undone. Are you sure you want to delete your account?": "Bu işlem geri alınamaz. Hesabınızı silmek istediğinize emin misiniz?",
        "Account deleted.": "Hesap silindi.",
        "Home": "Ana Sayfa",
        "Feel Good": "İyi Hisset",
        "My Profile": "Profilim",
        "Log Out": "Çıkış Yap",
        "Profil Yönetimi": "Profil Yönetimi",

        // Meditasyon sayfası çevirileri
        "Tümü": "Tümü",
        "Uyku & Rahatlama": "Uyku & Rahatlama",
        "Odaklanma & Üretkenlik": "Odaklanma & Üretkenlik",
        "Doğa & Farkındalık": "Doğa & Farkındalık",
        "Sabah Aktivasyonu": "Sabah Aktivasyonu",
        "Nefes & Sakinlik": "Nefes & Sakinlik",
        "Derin Uyku İçin Yağmur": "Derin Uyku İçin Yağmur",
        "Gece Meditasyonu": "Gece Meditasyonu",
        "Ay Işığı Meditasyonu": "Ay Işığı Meditasyonu",
        "Odaklanma Piyanosu": "Odaklanma Piyanosu",
        "Çalışma Odaklanması": "Çalışma Odaklanması",
        "Stres Azaltan Dalgalar": "Stres Azaltan Dalgalar",
        "Orman Sesi Meditasyonu": "Orman Sesi Meditasyonu",
        "Sabah Esnemesi": "Sabah Esnemesi",
        "Güneş Doğuşu Meditasyonu": "Güneş Doğuşu Meditasyonu",
        "Derin Nefes Egzersizi": "Derin Nefes Egzersizi",
        "Sakinlik Meditasyonu": "Sakinlik Meditasyonu",

        // Acil Destek sayfası çevirileri
        "Acil Destek": "Acil Destek",
        "İhtiyacınız olduğunda hemen ulaşabileceğiniz güvenli destek sistemi": "İhtiyacınız olduğunda hemen ulaşabileceğiniz güvenli destek sistemi",
        "Acil durum mesajı göndermek için butona tıklayın": "Acil durum mesajı göndermek için butona tıklayın",
        "BENİ ARA ACİLL KRİZ GEÇİRİYORUM !!!": "BENİ ARA ACİLL KRİZ GEÇİRİYORUM !!!",
        "Şu an kendimi iyi hissetmiyorum bana ulaşır mısın ?": "Şu an kendimi iyi hissetmiyorum bana ulaşır mısın ?",
        "İyi değilim 10 dk içinde bir şey yazmazsam bana ulaş": "İyi değilim 10 dk içinde bir şey yazmazsam bana ulaş",

        // Dashboard sayfası çevirileri
        "Hoşgeldiniz": "Hoşgeldiniz",
        "Merhaba! Size nasıl yardımcı olabilirim?": "Merhaba! Size nasıl yardımcı olabilirim?",
        "Mesajınızı yazın...": "Mesajınızı yazın...",
        "Bu bir örnek bot yanıtıdır.": "Bu bir örnek bot yanıtıdır.",

        // Destek Duvarı sayfası çevirileri
        "Destek Duvarı": "Destek Duvarı",
        "Hikayeni Paylaş": "Hikayeni Paylaş",
        "Hikayeni buraya yazabilirsin...": "Hikayeni buraya yazabilirsin...",
        "Paylaş": "Paylaş",
        "Anonim": "Anonim",
        "Beğen": "Beğen",

        // Günlük Kartlar sayfası çevirileri
        "Günlük Kartlar": "Günlük Kartlar",
        "Bugünün Sözü": "Bugünün Sözü",
        "Motivasyon": "Motivasyon",
        "Düşünce": "Düşünce",

        // Haftalık Raporlar sayfası çevirileri
        "Haftalık Raporlar": "Haftalık Raporlar",
        "Haftalık Aktivite": "Haftalık Aktivite",
        "Uygulama Kullanım Günü": "Uygulama Kullanım Günü",
        "Tamamlanan Görev": "Tamamlanan Görev",
        "Nefes Egzersizi Seansı": "Nefes Egzersizi Seansı",
        "Görev Tamamlama": "Görev Tamamlama",

        // Help Center sayfası çevirileri
        "İyi Hisset - Yardım Merkezi": "İyi Hisset - Yardım Merkezi",
        "Projeye Genel Bakış": "Projeye Genel Bakış",
        "Ana Özellikler": "Ana Özellikler",
        "Sohbet Botu": "Sohbet Botu",
        "Günlük Görevler": "Günlük Görevler",
        "Durum Takibi": "Durum Takibi",
        "Acil Destek Sistemi": "Acil Destek Sistemi",
        "Günlük Motivasyon Kartları": "Günlük Motivasyon Kartları",
        "Bildirim Sistemi": "Bildirim Sistemi",
        "Hesap Yönetimi": "Hesap Yönetimi",

        // Login sayfası çevirileri
        "Kullanıcı Girişi": "Kullanıcı Girişi",
        "Giriş Yap": "Giriş Yap",
        "Hesabın yok mu?": "Hesabın yok mu?",
        "Bu alan zorunludur.": "Bu alan zorunludur.",

        // Register sayfası çevirileri
        "Hesap Oluştur": "Hesap Oluştur",
        "Kaydol": "Kaydol",
        "Hesabın zaten var mı?": "Hesabın zaten var mı?",

        // Settings sayfası çevirileri
        "Yazı Tipi Boyutu": "Yazı Tipi Boyutu",
        "Boyut Seçin": "Boyut Seçin",
        "Acil Durum İletişim Bilgileri": "Acil Durum İletişim Bilgileri",
        "Acil Durum Telefon Numarası": "Acil Durum Telefon Numarası",
        "Acil Durum Mesajı": "Acil Durum Mesajı",
        "Acil durumda gönderilecek mesaj...": "Acil durumda gönderilecek mesaj...",
        "Kaydet": "Kaydet",

        // Bildirimler sayfası çevirileri
        "Bildirimler": "Bildirimler",
        "Günlük Görevleriniz Hazır!": "Günlük Görevleriniz Hazır!",
        "Bugün için 3 yeni görev eklendi. Hemen kontrol edin!": "Bugün için 3 yeni görev eklendi. Hemen kontrol edin!",
        "5 dakika önce": "5 dakika önce",
        "Tebrikler!": "Tebrikler!",
        "Bu hafta 5 gün üst üste günlük görevlerinizi tamamladınız.": "Bu hafta 5 gün üst üste günlük görevlerinizi tamamladınız.",
        "2 saat önce": "2 saat önce",
        "Yeni İçerik": "Yeni İçerik",
        "Stres yönetimi için yeni bir nefes egzersizi eklendi.": "Stres yönetimi için yeni bir nefes egzersizi eklendi.",
        "Dün": "Dün",
        "Destek Mesajınız": "Destek Mesajınız",
        "Destek duvarında paylaştığınız mesaja 3 yeni yorum geldi.": "Destek duvarında paylaştığınız mesaja 3 yeni yorum geldi.",
        "2 gün önce": "2 gün önce"
    },
    en: {
        // English translations (keep original English text)
        "My Statistics": "My Statistics",
        "Track your progress and see how you're doing with your mental health journey.": "Track your progress and see how you're doing with your mental health journey.",
        "Days Active": "Days Active",
        "Chat Sessions": "Chat Sessions",
        "Mood Score": "Mood Score",
        "Completed Tasks": "Completed Tasks",
        "Edit Profile": "Edit Profile",
        "Click or drag to upload your profile photo": "Click or drag to upload your profile photo",
        "Select Photo": "Select Photo",
        "Username": "Username",
        "Email": "Email",
        "First Name": "First Name",
        "Enter your first name": "Enter your first name",
        "Last Name": "Last Name",
        "Enter your last name": "Enter your last name",
        "Save Changes": "Save Changes",
        "Settings": "Settings",
        "Language Selection": "Language Selection",
        "Set language across the site": "Set language across the site",
        "Turkish": "Turkish",
        "English": "English",
        "User Information": "User Information",
        "Update Information": "Update Information",
        "Change Password": "Change Password",
        "Current Password": "Current Password",
        "New Password": "New Password",
        "Confirm New Password": "Confirm New Password",
        "Profile Photo": "Profile Photo",
        "Update Photo": "Update Photo",
        "Font Size": "Font Size",
        "Adjust font size across the site": "Adjust font size across the site",
        "Small": "Small",
        "Normal": "Normal",
        "Large": "Large",
        "Very Large": "Very Large",
        "Help Center": "Help Center",
        "Find answers to common questions and get support when you need it.": "Find answers to common questions and get support when you need it.",
        "Frequently Asked Questions": "Frequently Asked Questions",
        "How can I change my password?": "How can I change my password?",
        "How do I update my profile picture?": "How do I update my profile picture?",
        "What are the privacy settings?": "What are the privacy settings?",
        "How can I contact support?": "How can I contact support?",
        "Visit Help Center": "Visit Help Center",
        "Delete Account": "Delete Account",
        "This action cannot be undone. All your data will be permanently deleted.": "This action cannot be undone. All your data will be permanently deleted.",
        "Type 'DELETE MY ACCOUNT' to confirm": "Type 'DELETE MY ACCOUNT' to confirm",
        "Permanently Delete My Account": "Permanently Delete My Account",
        "Please fill in all fields.": "Please fill in all fields.",
        "New passwords do not match.": "New passwords do not match.",
        "New password cannot be the same as current password.": "New password cannot be the same as current password.",
        "Password updated successfully!": "Password updated successfully!",
        "Please type DELETE MY ACCOUNT to confirm.": "Please type DELETE MY ACCOUNT to confirm.",
        "This action cannot be undone. Are you sure you want to delete your account?": "This action cannot be undone. Are you sure you want to delete your account?",
        "Account deleted.": "Account deleted.",
        "Home": "Home",
        "Feel Good": "Feel Good",
        "My Profile": "My Profile",
        "Log Out": "Log Out",
        "Profil Yönetimi": "Profile Management",

        // Meditasyon sayfası çevirileri
        "Tümü": "All",
        "Uyku & Rahatlama": "Sleep & Relaxation",
        "Odaklanma & Üretkenlik": "Focus & Productivity",
        "Doğa & Farkındalık": "Nature & Mindfulness",
        "Sabah Aktivasyonu": "Morning Activation",
        "Nefes & Sakinlik": "Breathing & Calm",
        "Derin Uyku İçin Yağmur": "Rain for Deep Sleep",
        "Gece Meditasyonu": "Night Meditation",
        "Ay Işığı Meditasyonu": "Moonlight Meditation",
        "Odaklanma Piyanosu": "Focus Piano",
        "Çalışma Odaklanması": "Work Focus",
        "Stres Azaltan Dalgalar": "Stress-Relieving Waves",
        "Orman Sesi Meditasyonu": "Forest Sound Meditation",
        "Sabah Esnemesi": "Morning Stretch",
        "Güneş Doğuşu Meditasyonu": "Sunrise Meditation",
        "Derin Nefes Egzersizi": "Deep Breathing Exercise",
        "Sakinlik Meditasyonu": "Calm Meditation",

        // Acil Destek sayfası çevirileri
        "Acil Destek": "Emergency Support",
        "İhtiyacınız olduğunda hemen ulaşabileceğiniz güvenli destek sistemi": "Safe support system you can reach immediately when needed",
        "Acil durum mesajı göndermek için butona tıklayın": "Click the button to send an emergency message",
        "BENİ ARA ACİLL KRİZ GEÇİRİYORUM !!!": "CALL ME URGENTLY I'M HAVING A CRISIS !!!",
        "Şu an kendimi iyi hissetmiyorum bana ulaşır mısın ?": "I'm not feeling well right now, can you reach out to me?",
        "İyi değilim 10 dk içinde bir şey yazmazsam bana ulaş": "I'm not feeling well — please check on me if I don't respond in 10 minutes",

        // Dashboard sayfası çevirileri
        "Hoşgeldiniz": "Welcome",
        "Merhaba! Size nasıl yardımcı olabilirim?": "Hello! How can I help you?",
        "Mesajınızı yazın...": "Type your message...",
        "Bu bir örnek bot yanıtıdır.": "This is a sample bot response.",

        // Destek Duvarı sayfası çevirileri
        "Destek Duvarı": "Support Wall",
        "Hikayeni Paylaş": "Share Your Story",
        "Hikayeni buraya yazabilirsin...": "Write your story here...",
        "Paylaş": "Share",
        "Anonim": "Anonymous",
        "Beğen": "Like",

        // Günlük Kartlar sayfası çevirileri
        "Günlük Kartlar": "Daily Cards",
        "Her gün yeni bir motivasyon ve ilham için özel olarak seçilmiş kartlar": "Cards specially selected for new motivation and inspiration every day",
        "Bugünün Sözü": "Today's Quote",
        "Her gün yeni bir başlangıçtır. Kendine inan ve ilerle.": "Every day is a new beginning. Believe in yourself and move forward.",
        "Bugün kendine güven": "Trust yourself today",
        "Motivasyon": "Motivation",
        "Küçük adımlar büyük değişimlere yol açar. Her gün bir adım at.": "Small steps lead to big changes. Take one step every day.",
        "Adım adım ilerle": "Move forward step by step",
        "Düşünce": "Thought",
        "Olumlu düşünceler, olumlu sonuçlar doğurur. Bugün kendine iyi davran.": "Positive thoughts lead to positive results. Be kind to yourself today.",
        "Pozitif kal": "Stay positive",
        "Farkındalık": "Awareness",
        "Şu anı yaşa, geçmişi bırak, geleceği planla ama bugüne odaklan.": "Live in the present, let go of the past, plan the future but focus on today.",
        "Anı yaşa": "Live the moment",
        "İyileşme": "Healing",
        "Kendini sev ve kabul et. Mükemmel olmak zorunda değilsin, sadece kendin ol.": "Love and accept yourself. You don't have to be perfect, just be yourself.",
        "Kendini sev": "Love yourself",
        "Başarı": "Success",
        "Başarı yolculuğu, her gün atılan küçük adımlarla başlar. Bugün senin günün.": "The journey to success begins with small steps taken every day. Today is your day.",
        "Başarıya odaklan": "Focus on success",

        // Haftalık Raporlar sayfası çevirileri
        "Haftalık Raporlar": "Weekly Reports",
        "Haftalık Aktivite": "Weekly Activity",
        "Uygulama Kullanım Günü": "App Usage Day",
        "Tamamlanan Görev": "Completed Task",
        "Nefes Egzersizi Seansı": "Breathing Exercise Session",
        "Görev Tamamlama": "Task Completion",

        // Help Center sayfası çevirileri
        "İyi Hisset - Yardım Merkezi": "Feel Good - Help Center",
        "Projeye Genel Bakış": "Project Overview",
        "Ana Özellikler": "Main Features",
        "Sohbet Botu": "Chat Bot",
        "Günlük Görevler": "Daily Tasks",
        "Durum Takibi": "Status Tracking",
        "Acil Destek Sistemi": "Emergency Support System",
        "Günlük Motivasyon Kartları": "Daily Motivation Cards",
        "Bildirim Sistemi": "Notification System",
        "Hesap Yönetimi": "Account Management",

        // Login sayfası çevirileri
        "Kullanıcı Girişi": "User Login",
        "Giriş Yap": "Login",
        "Hesabın yok mu?": "Don't have an account?",
        "Bu alan zorunludur.": "This field is required.",

        // Register sayfası çevirileri
        "Hesap Oluştur": "Create Account",
        "Kaydol": "Sign Up",
        "Hesabın zaten var mı?": "Already have an account?",

        // Settings sayfası çevirileri
        "Yazı Tipi Boyutu": "Font Size",
        "Boyut Seçin": "Select Size",
        "Acil Durum İletişim Bilgileri": "Emergency Contact Information",
        "Acil Durum Telefon Numarası": "Emergency Phone Number",
        "Acil Durum Mesajı": "Emergency Message",
        "Acil durumda gönderilecek mesaj...": "Message to be sent in case of emergency...",
        "Kaydet": "Save",

        // Bildirimler sayfası çevirileri
        "Bildirimler": "Notifications",
        "Günlük Görevleriniz Hazır!": "Your Daily Tasks are Ready!",
        "Bugün için 3 yeni görev eklendi. Hemen kontrol edin!": "3 new tasks have been added for today. Check them out now!",
        "5 dakika önce": "5 minutes ago",
        "Tebrikler!": "Congratulations!",
        "Bu hafta 5 gün üst üste günlük görevlerinizi tamamladınız.": "You have completed your daily tasks for 5 consecutive days this week.",
        "2 saat önce": "2 hours ago",
        "Yeni İçerik": "New Content",
        "Stres yönetimi için yeni bir nefes egzersizi eklendi.": "A new breathing exercise for stress management has been added.",
        "Dün": "Yesterday",
        "Destek Mesajınız": "Your Support Message",
        "Destek duvarında paylaştığınız mesaja 3 yeni yorum geldi.": "3 new comments have been added to your message on the support wall.",
        "2 gün önce": "2 days ago"
    }
};

// Dinamik dil değiştirme fonksiyonu
function changeLanguage(lang) {
    // localStorage'a kaydet
    localStorage.setItem('selectedLanguage', lang);
    
    // Butonların active durumunu güncelle
    updateLanguageButtons(lang);
    
    // Sayfadaki tüm metinleri çevir
    translatePage(lang);
    
    // Django'ya dil değişikliğini bildir (arka planda)
    notifyDjango(lang);
}

// Sayfadaki metinleri çevir
function translatePage(lang) {
    const langTranslations = translations[lang];
    if (!langTranslations) return;
    
    // data-translate attribute'u olan elementleri çevir
    const elementsWithTranslate = document.querySelectorAll('[data-translate]');
    elementsWithTranslate.forEach(element => {
        const translationKey = element.getAttribute('data-translate');
        if (langTranslations[translationKey]) {
            element.textContent = langTranslations[translationKey];
        }
    });
    
    // Placeholder'ları çevir
    const inputs = document.querySelectorAll('input[placeholder]');
    inputs.forEach(input => {
        const placeholder = input.getAttribute('placeholder');
        if (placeholder && langTranslations[placeholder]) {
            input.setAttribute('placeholder', langTranslations[placeholder]);
        }
    });
    
    // Title'ı çevir
    const title = document.querySelector('title');
    if (title && langTranslations[title.textContent]) {
        title.textContent = langTranslations[title.textContent];
    }
    
    // HTML lang attribute'unu güncelle
    document.documentElement.lang = lang;
    
    // Tüm metin içeriklerini çevir
    translateTextContent(document.body, langTranslations);
}

// Tüm metin içeriklerini recursive olarak çevir
function translateTextContent(element, translations) {
    if (element.nodeType === Node.TEXT_NODE) {
        const text = element.textContent.trim();
        if (text && translations[text]) {
            element.textContent = translations[text];
        }
    } else {
        for (let child of element.childNodes) {
            translateTextContent(child, translations);
        }
    }
}

// Dil butonlarının active durumunu güncelle
function updateLanguageButtons(selectedLang) {
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        const langCode = btn.getAttribute('data-lang');
        if (langCode === selectedLang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

// Django'ya dil değişikliğini bildir (arka planda)
function notifyDjango(lang) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
    if (!csrfToken) return;
    
    const formData = new FormData();
    formData.append('language', lang);
    formData.append('next', window.location.pathname);
    
    fetch('/i18n/setlang/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    }).catch(error => {
        console.log('Language change notification failed:', error);
    });
}

// Çeviri anahtarını al
function getTranslation(key) {
    const currentLang = localStorage.getItem('selectedLanguage') || 'tr';
    return translations[currentLang][key] || key;
}

// Dil sistemini başlat
function initializeLanguage() {
    const savedLanguage = localStorage.getItem('selectedLanguage') || 'tr';
    
    // Sayfa yüklendiğinde kaydedilmiş dili uygula
    translatePage(savedLanguage);
    updateLanguageButtons(savedLanguage);
    
    // Dil değiştirme butonlarını dinle
    const langButtons = document.querySelectorAll('.lang-btn');
    langButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const lang = this.getAttribute('data-lang');
            changeLanguage(lang);
        });
    });
}

// Sayfa yüklendiğinde dil sistemini başlat
document.addEventListener('DOMContentLoaded', function() {
    initializeLanguage();
});

// Global olarak erişilebilir yap
window.changeLanguage = changeLanguage;
window.getTranslation = getTranslation;
window.initializeLanguage = initializeLanguage; 