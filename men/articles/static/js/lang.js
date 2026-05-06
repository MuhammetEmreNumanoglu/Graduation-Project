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
        "Profil Yönetimi": "Profile Management",
        "Profile Management": "Profil Yönetimi",
        "Help": "Yardım",
        "Welcome": "Hoşgeldin",
        "Hoş geldin!": "Welcome",

        // Dil ve tema değiştirme popup'ları
        "Language": "Dil",
        "language changed to": "değiştirildi",
        "Theme": "Tema",
        "theme changed to": "teması değiştirildı",
        "Light Mode": "Açık Mod",
        "Dark Mode": "Koyu Mod",
        "Font Size": "Yazı Tipi Boyutu",
        "size set to": "boyutuna ayarlandı",

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
        // EN -> TR yansımaları (sunucu EN döndürdüğünde TR'ye çevirmek için)
        "Emergency Support": "Acil Destek",
        "Safe support system you can reach immediately when you need it": "İhtiyacınız olduğunda hemen ulaşabileceğiniz güvenli destek sistemi",
        "Click the button to send an emergency message": "Acil durum mesajı göndermek için butona tıklayın",
        "CALL ME NOW, I'M IN CRISIS!!!": "BENİ ARA ACİLL KRİZ GEÇİRİYORUM !!!",
        "I don't feel well right now, can you contact me?": "Şu an kendimi iyi hissetmiyorum bana ulaşır mısın ?",
        "I'm not well — please contact me if I don't respond in 10 minutes": "İyi değilim 10 dk içinde bir şey yazmazsam bana ulaş",
        // Acil Destek toast metinleri (TR)
        "Message Sent": "Mesaj Gönderildi",
        "Your emergency message has been sent successfully. We will contact you as soon as possible.": "Acil durum mesajınız başarıyla gönderildi. En kısa sürede sizinle iletişime geçeceğiz.",
        "No Message Selected": "Mesaj Seçilmedi",
        "Please select a message first.": "Lütfen önce bir mesaj seçin.",

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
        "Help Center - Feel Good": "Yardım Merkezi - İyi Hisset",
        "Help Center": "Yardım Merkezi",
        "Help": "Yardım",
        "Feel Good is a comprehensive application designed to support users' mental health and help them better manage their daily lives.": "İyi Hisset, kullanıcıların ruh sağlığını desteklemek ve günlük yaşamlarını daha iyi yönetmelerine yardımcı olmak için tasarlanmış kapsamlı bir uygulamadır.",
        "Project Overview": "Projeye Genel Bakış",
        "Main Features": "Ana Özellikler",
        "Get instant help with the AI-powered chatbot available 24/7.": "7/24 destek sağlayan yapay zeka destekli sohbet botu ile anında yardım alın.",
        "Improve yourself with personalized daily tasks and activities.": "Kişiselleştirilmiş günlük görevler ve aktiviteler ile kendinizi geliştirin.",
        "Track your mood and progress, and get detailed reports.": "Ruh halinizi ve ilerlemenizi takip edin, detaylı raporlar alın.",
        "Emergency Support System": "Acil Destek Sistemi",
        "Instant help call with emergency button": "Acil durum butonu ile anında yardım çağırma",
        "Automatic notification to pre-defined emergency contacts": "Önceden belirlenmiş acil iletişim kişilerine otomatik bildirim",
        "Location sharing and quick response": "Konum paylaşımı ve hızlı müdahale",
        "Daily Motivation Cards": "Günlük Motivasyon Kartları",
        "Daily motivational quotes": "Günlük motive edici sözler",
        "Interactive card design": "Etkileşimli kart tasarımı",
        "Personalized content": "Kişiselleştirilmiş içerik",
        "Support Wall": "Destek Duvarı",
        "Anonymous sharing option": "Anonim paylaşım seçeneği",
        "Like and support system": "Beğeni ve destek sistemi",
        "Community support": "Topluluk desteği",
        "Weekly Reports": "Haftalık Raporlar",
        "Achievement statistics": "Başarı istatistikleri",
        "Personal development analysis": "Kişisel gelişim analizi",
        "Notification System": "Bildirim Sistemi",
        "Task reminders": "Görev hatırlatıcıları",
        "Achievement notifications": "Başarı bildirimleri",
        "Community interactions": "Topluluk etkileşimleri",
        "Account Management": "Hesap Yönetimi",
        "Change profile photo": "Profil fotoğrafı değiştirme",
        "Update password": "Şifre güncelleme",
        "Language and appearance settings": "Dil ve görünüm ayarları",
        "Frequently Asked Questions": "Sıkça Sorulan Sorular",
        "How can I start using the app?": "Uygulamayı nasıl kullanmaya başlayabilirim?",
        "To start using the app, you first need to create an account. Then, you can track your daily tasks and interact with the chatbot.": "Uygulamayı kullanmaya başlamak için öncelikle hesabınızı oluşturmanız gerekiyor. Ardından, günlük görevlerinizi takip edebilir ve sohbet botu ile iletişime geçebilirsiniz.",
        "How can I get help in an emergency?": "Acil durumda nasıl yardım alabilirim?",
        "You can instantly send a message to your pre-defined emergency contact using the emergency button. Don't forget to save your emergency contact information on the settings page before using this feature.": "Acil durum butonunu kullanarak önceden belirlediğiniz acil iletişim kişinize anında mesaj gönderebilirsiniz. Bu özelliği kullanmadan önce ayarlar sayfasından acil durum iletişim bilgilerinizi kaydetmeyi unutmayın.",
        "How do daily cards work?": "Günlük kartlar nasıl çalışır?",
        "Daily cards contain motivational quotes and thoughts prepared especially for you every day. These cards help you start your day positively.": "Günlük kartlar, her gün size özel olarak hazırlanan motivasyon sözleri ve düşünceler içerir. Bu kartlar, gününüze olumlu bir başlangıç yapmanıza yardımcı olur.",
        "Can I share on the support wall?": "Destek duvarında paylaşım yapabilir miyim?",
        "Yes, you can share your experiences anonymously on the support wall. Other users can also like and support your posts.": "Evet, destek duvarında anonim olarak deneyimlerinizi paylaşabilirsiniz. Diğer kullanıcılar da sizin paylaşımlarınızı beğenebilir ve destek olabilir.",
        "How can I change my account settings?": "Hesap ayarlarımı nasıl değiştirebilirim?",
        "You can update your profile photo, password, and other account settings from the settings page. You can also change appearance settings such as font size and theme here.": "Ayarlar sayfasından profil fotoğrafınızı, şifrenizi ve diğer hesap ayarlarınızı güncelleyebilirsiniz. Ayrıca yazı tipi boyutu ve tema gibi görünüm ayarlarını da buradan değiştirebilirsiniz.",

        // Psikolog paneli çevirileri
        "Psychologist Dashboard": "Psikolog Paneli",
        "User Information": "Kullanıcı Bilgileri",
        "Last 7 Days Usage": "Son 7 Gün Kullanımı",
        "Loading...": "Yükleniyor...",
        "Active": "Aktif",
        "Inactive": "Pasif",
        "Session Rating": "Seans Değerlendirmesi",
        "Score:": "Puan:",
        "Save Rating": "Değerlendirmeyi Kaydet",
        "Saved ✓": "Kaydedildi ✓",
        "Session note (optional)...": "Seans notu (isteğe bağlı)...",
        "Assigned Tasks": "Atanan Görevler",
        "Completed": "Tamamlandı",
        "Pending": "Bekliyor",
        "No tasks assigned yet.": "Henüz görev atanmamış.",
        "Send Task": "Görev Gönder",
        "Breathing Exercise": "Nefes Egzersizi",
        "Meditation": "Meditasyon",
        "Daily Cards": "Günlük Kartlar",
        "Support Wall": "Destek Duvarı",
        "Apply breathing techniques": "Nefes tekniklerini uygula",
        "Do daily meditation": "Günlük meditasyon yap",
        "View motivation cards": "Motivasyon kartlarını gör",
        "Post in the forum": "Forumda paylaşım yap",
        "Please select a task type.": "Lütfen bir görev türü seçin.",
        "Takip": "Track",
        "Acil": "Urgent",
        "Normal": "Normal",
        "Private Notes": "Kişiye Özel Notlar",
        "Notes load when a user is selected.": "Bir kullanıcı seçince notlar yüklenir.",
        "Save": "Kaydet",
        "Session Rating History": "Seans Puanı Geçmişi",
        "Waiting": "Bekliyor",
        "Sana yeni bir görev atandı: {}": "Sana yeni bir görev atandı: {}",
        "Text": "Metin",
        "Choose File": "Dosya Seç",
        "No file chosen": "Dosya seçilmedi",
        "Last message": "Son mesaj",
        "Select a user from the sidebar to start messaging.": "Mesajlaşmaya başlamak için sidebar'dan bir kullanıcı seçin.",

        // Forum çevirileri
        "Share Your Story": "Hikayeni Paylaş",
        "Write your story here...": "Hikayeni buraya yazabilirsin...",
        "Share": "Paylaş",
        "Like": "Beğen",
        "Comments": "Yorumlar",
        "Add a comment...": "Yorum ekle...",
        "Send": "Gönder",
        "Anonymous": "Anonim",
        "Previous": "Önceki",
        "Next": "Sonraki",
        "Bugün nasıl hissediyorsun?": "Bugün nasıl hissediyorsun?",
        "Günde sadece 1 kez sorulur. İstersen kısa bir not ekleyebilirsin.": "Günde sadece 1 kez sorulur. İstersen kısa bir not ekleyebilirsin.",
        "Kısa Not (Opsiyonel)": "Kısa Not (Opsiyonel)",
        "Kısa not (opsiyonel)": "Kısa not (opsiyonel)",
        "Psikolog ile sohbet başlatmak için mesaj gönderebilirsiniz.": "Psikolog ile sohbet başlatmak için mesaj gönderebilirsiniz.",
        "Very good": "Çok iyi",
        "Good": "İyi",
        "Nötr": "Nötr",
        "Bad": "Kötü",
        "Very bad": "Çok kötü",
        "Örn: Bugün biraz gergindim…": "Örn: Bugün biraz gergindim…",
        "Şimdi değil": "Şimdi değil",
        "İsterseniz buraya uzun bir metin yazabilirsiniz...": "İsterseniz buraya uzun bir metin yazabilirsiniz...",
        "Psikolog ile Sohbet": "Psikolog ile Sohbet",
        "Henüz bildirim yok": "Henüz bildirim yok",
        "Bildirimler": "Bildirimler",
        "Kullanıcı henüz hayat hikayesini paylaşmadı.": "Kullanıcı henüz hayat hikayesini paylaşmadı.",
        "Bu kullanıcıya özel notunuzu buraya yazın...": "Bu kullanıcıya özel notunuzu buraya yazın...",
        "Bildirim Gönder": "Bildirim Gönder",
        "Bildirim metnini yazın...": "Bildirim metnini yazın...",
        "İptal": "İptal",
        "Gönder": "Gönder",
        "Şifre uzunluğu uygun.": "Şifre uzunluğu uygun.",
        "Henüz mesaj yok. İlk mesajı siz gönderin!": "Henüz mesaj yok. İlk mesajı siz gönderin!",
        "Şifreler eşleşiyor.": "Şifreler eşleşiyor.",
        "Kaydedildi ✓": "Kaydedildi ✓",
        "Meditasyon ✓": "Meditasyon ✓",
        "Nefes Egzersizi ✓": "Nefes Egzersizi ✓",
        "Üye Girişi": "Üye Girişi",
        "🤝 Support Wall": "🤝 Destek Duvarı",
        "🃏 Daily Cards ✓": "🃏 Günlük Kartlar ✓",
        "🧘 Meditasyon ✓": "🧘 Meditasyon ✓",
        "🌬️ Nefes Egzersizi ✓": "🌬️ Nefes Egzersizi ✓",
        "Bir kullanıcı seçtiğinizde bugünkü ruh hali ve hayat hikayesi burada görünecek.": "Bir kullanıcı seçtiğinizde bugünkü ruh hali ve hayat hikayesi burada görünecek.",
        "Henüz mesaj yok": "Henüz mesaj yok",
        "Henüz görev yok.": "Henüz görev yok.",
        "Kimlere bildirim göndermek istiyorsunuz?": "Kimlere bildirim göndermek istiyorsunuz?",
        "Tamamlandı": "Tamamlandı",
        "Bekliyor": "Bekliyor",
        "No posts yet.": "Henüz gönderi yok.",
        "Be the first to share!": "İlk paylaşan sen ol!",
        "Bütün mesajlar okundu olarak işaretle": "Bütün bildirimleri okundu olarak işaretle"
    },
    en: {
        // Additional UI Element Translations
        "Beni Hatırla": "Remember Me",
        "Psikolog Girişi": "Psychologist Login",
        "İyi Hisset": "Feel Good",
        "Tamamlananlar": "Completed",
        "Bugünkü ruh hali": "Today's mood",
        "Çok iyi": "Very good",
        "İyi": "Good",
        "Normal": "Neutral",
        "Kötü": "Bad",
        "Çok kötü": "Very bad",
        "Son günler": "Recent days",
        "Hayat Hikayem": "My Life Story",
        "Son 7 Gün Kullanımı": "Last 7 Days Usage",
        "Seans Değerlendirmesi": "Session Rating",
        "Puan:": "Score:",
        "Seans notu (isteğe bağlı)...": "Session note (optional)...",
        "Değerlendirmeyi Kaydet": "Save Rating",
        "Atanan Görevler": "Assigned Tasks",
        "Tamamlandı": "Completed",
        "Acil": "Urgent",
        "Takip": "Follow-up",
        "Bir kullanıcı seçtiğinizde bugünkü ruh hali ve hayat hikayesi burada görünecek. Mesajlaşmaya başlamak için sidebar'dan bir kullanıcı seçin.": "When you select a user, their today's mood and life story will appear here. Select a user from the sidebar to start messaging.",
        "Bir kullanıcı seçtiğinizde bugünkü ruh hali ve hayat hikayesi burada görünecek. Mesajlaşmaya başlamak için sidebar'dan bir kullanıcı seçin .": "When you select a user, their today's mood and life story will appear here. Select a user from the sidebar to start messaging.",
        "Henüz ruh hali geçmişi yok.": "No mood history yet.",
        "Kayıt yok": "No record",
        "Pzt": "Mon",
        "Sal": "Tue",
        "Çar": "Wed",
        "Per": "Thu",
        "Cum": "Fri",
        "Cmt": "Sat",
        "Paz": "Sun",
        "Bekliyor": "Waiting",
        "Kişiye Özel Notlar": "Private Notes",
        "Son mesaj": "Last message",
        "Metin": "Text",
        "Dosya Seç": "Choose File",
        "Dosya seçilmedi": "No file chosen",
        "Psikoloğunuzun sizi daha iyi tanıması için isterseniz hayat hikayenizi paylaşabilirsiniz.": "You can share your life story if you want so that your psychologist can get to know you better.",
        "Sana yeni bir görev atandı: {}": "A new task has been assigned to you: {}",
        "Bugün nasıl hissediyorsun?": "How are you feeling today?",
        "Günde sadece 1 kez sorulur. İstersen kısa bir not ekleyebilirsin.": "Asked only once a day. You can add a short note if you want.",
        "Kısa Not (Opsiyonel)": "Short Note (Optional)",
        "Kısa not (opsiyonel)": "Short note (optional)",
        "Psikolog ile sohbet başlatmak için mesaj gönderebilirsiniz.": "You can send a message to start a chat with the psychologist.",
        "Very good": "Very good",
        "Good": "Good",
        "Nötr": "Neutral",
        "Bad": "Bad",
        "Very bad": "Very bad",
        "Örn: Bugün biraz gergindim…": "e.g., I was a bit nervous today...",
        "Şimdi değil": "Not now",
        "İsterseniz buraya uzun bir metin yazabilirsiniz...": "You can write a long text here if you want...",
        "Psikolog ile Sohbet": "Chat with Psychologist",
        "Henüz bildirim yok": "No notifications yet",
        "Bildirimler": "Notifications",
        "Kullanıcı henüz hayat hikayesini paylaşmadı.": "The user has not shared their life story yet.",
        "Bu kullanıcıya özel notunuzu buraya yazın...": "Write your private note for this user here...",
        "Bildirim Gönder": "Send Notification",
        "Bildirim metnini yazın...": "Write the notification text...",
        "İptal": "Cancel",
        "Gönder": "Send",
        "Şifre uzunluğu uygun.": "Password length is appropriate.",
        "Henüz mesaj yok. İlk mesajı siz gönderin!": "No messages yet. Send the first message!",
        "Şifreler eşleşiyor.": "Passwords match.",
        "Kaydedildi ✓": "Saved ✓",
        "Meditasyon ✓": "Meditation ✓",
        "Nefes Egzersizi ✓": "Breathing Exercise ✓",
        "Üye Girişi": "Member Login",
        "🤝 Support Wall": "🤝 Support Wall",
        "🃏 Daily Cards ✓": "🃏 Daily Cards ✓",
        "🧘 Meditasyon ✓": "🧘 Meditation ✓",
        "🌬️ Nefes Egzersizi ✓": "🌬️ Breathing Exercise ✓",
        "Bir kullanıcı seçtiğinizde bugünkü ruh hali ve hayat hikayesi burada görünecek.": "When you select a user, their today's mood and life story will appear here.",
        "Henüz mesaj yok": "No messages yet",
        "Henüz görev yok.": "No tasks yet.",
        "Kimlere bildirim göndermek istiyorsunuz?": "To whom do you want to send notifications?",
        "Tamamlandı": "Completed",
        "Bekliyor": "Waiting",
        "Mesajlaşmaya başlamak için sidebar'dan bir kullanıcı seçin": "Select a user from the sidebar to start messaging.",

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
        "Yardım": "Help",
        "Help": "Help",
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
        "Profile Management": "Profile Management",
        "Help": "Help",
        "Hoş geldin": "Welcome",
        "Hoş geldin!": "Welcome!",

        // Dil ve tema değiştirme popup'ları
        "Language": "Language",
        "language changed to": "changed to",
        "Theme": "Theme",
        "theme changed to": "theme changed to",
        "Light Mode": "Light Mode",
        "Dark Mode": "Dark Mode",
        "Font Size": "Font Size",
        "size set to": "size set to",

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
        // Acil Destek toast metinleri (EN)
        "Message Sent": "Message Sent",
        "Your emergency message has been sent successfully. We will contact you as soon as possible.": "Your emergency message has been sent successfully. We will contact you as soon as possible.",
        "No Message Selected": "No Message Selected",
        "Please select a message first.": "Please select a message first.",

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
        "Specially selected cards for new motivation and inspiration every day": "Cards specially selected for new motivation and inspiration every day",
        "Bugünün Sözü": "Today's Quote",
        "Every day is a new beginning. Believe in yourself and stay strong.": "Every day is a new beginning. Believe in yourself and stay strong.",
        "Trust yourself today": "Trust yourself today",
        "Motivasyon": "Motivation",
        "Small steps lead to big changes. Take one step every day.": "Small steps lead to big changes. Take one step every day.",
        "Move forward step by step": "Move forward step by step",
        "Positive thoughts lead to positive results. Be kind to yourself today.": "Positive thoughts lead to positive results. Be kind to yourself today.",
        "Stay positive": "Stay positive",
        "Live in the present, let go of the past, plan the future but focus on today.": "Live in the present, let go of the past, plan the future but focus on today.",
        "Live the moment": "Live the moment",
        "Love and accept yourself. You don't have to be perfect, just be yourself.": "Love and accept yourself. You don't have to be perfect, just be yourself.",
        "Love yourself": "Love yourself",
        "The journey to success begins with small steps taken every day. Today is your day.": "The journey to success begins with small steps taken every day. Today is your day.",
        "Focus on success": "Focus on success",
        "Notifications": "Notifications",
        "Welcome! Today is a great day.": "Welcome! Today is a great day.",
        "Hoş geldin! Bugün harika bir gün.": "Welcome! Today is a great day.",
        "Hoşgeldiniz": "Welcome",
        "Hoş geldin": "Welcome",
        "Hoş geldin!": "Welcome!",
        "A new breathing exercise has been added.": "A new breathing exercise has been added.",
        "Don't forget your daily reflection!": "Don't forget your daily reflection!",
        "A friend left a message on the support wall.": "A friend left a message on the support wall.",
        "Your weekly report is ready!": "Your weekly report is ready!",

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
        "Font Size": "Font Size",
        "size set to": "size set to",
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
        "2 gün önce": "2 days ago",

        // Anasayfa çevirileri
        "My Tasks": "My Tasks",
        "Breathing Exercise": "Breathing Exercise",
        "Daily Reflection": "Daily Reflection",
        "Welcome to Feel Good!": "Welcome to Feel Good!",
        "Find the path to health and happiness with the Feel Good system.": "Find the path to health and happiness with the Feel Good system.",
        "EMERGENCY SUPPORT": "EMERGENCY SUPPORT",
        "Click to get help immediately": "Click to get help immediately",
        "Daily Cards": "Daily Cards",
        "Record your daily activities and health status.": "Record your daily activities and health status.",
        "Support Wall": "Support Wall",
        "Connect with other users and get support.": "Connect with other users and get support.",
        "Strengthen your respiratory system by doing breathing exercises.": "Strengthen your respiratory system by doing breathing exercises.",
        "Meditation": "Meditation",
        "Reduce your stress level by meditating.": "Reduce your stress level by meditating.",

        // Help Center translations (EN)
        "Help Center - Feel Good": "Help Center - Feel Good",
        "Help Center": "Help Center",
        "Feel Good is a comprehensive application designed to support users' mental health and help them better manage their daily lives.": "Feel Good is a comprehensive application designed to support users' mental health and help them better manage their daily lives.",
        "Project Overview": "Project Overview",
        "Main Features": "Main Features",
        "Get instant help with the AI-powered chatbot available 24/7.": "Get instant help with the AI-powered chatbot available 24/7.",
        "Improve yourself with personalized daily tasks and activities.": "Improve yourself with personalized daily tasks and activities.",
        "Track your mood and progress, and get detailed reports.": "Track your mood and progress, and get detailed reports.",
        "Emergency Support System": "Emergency Support System",
        "Instant help call with emergency button": "Instant help call with emergency button",
        "Automatic notification to pre-defined emergency contacts": "Automatic notification to pre-defined emergency contacts",
        "Location sharing and quick response": "Location sharing and quick response",
        "Daily Motivation Cards": "Daily Motivation Cards",
        "Daily motivational quotes": "Daily motivational quotes",
        "Interactive card design": "Interactive card design",
        "Personalized content": "Personalized content",
        "Support Wall": "Support Wall",
        "Anonymous sharing option": "Anonymous sharing option",
        "Like and support system": "Like and support system",
        "Community support": "Community support",
        "Weekly Reports": "Weekly Reports",
        "Achievement statistics": "Achievement statistics",
        "Personal development analysis": "Personal development analysis",
        "Notification System": "Notification System",
        "Task reminders": "Task reminders",
        "Achievement notifications": "Achievement notifications",
        "Community interactions": "Community interactions",
        "Account Management": "Account Management",
        "Change profile photo": "Change profile photo",
        "Update password": "Update password",
        "Language and appearance settings": "Language and appearance settings",
        "Frequently Asked Questions": "Frequently Asked Questions",
        "How can I start using the app?": "How can I start using the app?",
        "To start using the app, you first need to create an account. Then, you can track your daily tasks and interact with the chatbot.": "To start using the app, you first need to create an account. Then, you can track your daily tasks and interact with the chatbot.",
        "How can I get help in an emergency?": "How can I get help in an emergency?",
        "You can instantly send a message to your pre-defined emergency contact using the emergency button. Don't forget to save your emergency contact information on the settings page before using this feature.": "You can instantly send a message to your pre-defined emergency contact using the emergency button. Don't forget to save your emergency contact information on the settings page before using this feature.",
        "How do daily cards work?": "How do daily cards work?",
        "Daily cards contain motivational quotes and thoughts prepared especially for you every day. These cards help you start your day positively.": "Daily cards contain motivational quotes and thoughts prepared especially for you every day. These cards help you start your day positively.",
        "Can I share on the support wall?": "Can I share on the support wall?",
        "Yes, you can share your experiences anonymously on the support wall. Other users can also like and support your posts.": "Yes, you can share your experiences anonymously on the support wall. Other users can also like and support your posts.",
        "How can I change my account settings?": "How can I change my account settings?",
        "You can update your profile photo, password, and other account settings from the settings page. You can also change appearance settings such as font size and theme here.": "You can update your profile photo, password, and other account settings from the settings page. You can also change appearance settings such as font size and theme here.",

        // Psychologist dashboard translations
        "Psychologist Dashboard": "Psychologist Dashboard",
        "Last 7 Days Usage": "Last 7 Days Usage",
        "Loading...": "Loading...",
        "Active": "Active",
        "Inactive": "Inactive",
        "Session Rating": "Session Rating",
        "Score:": "Score:",
        "Save Rating": "Save Rating",
        "Saved ✓": "Saved ✓",
        "Session note (optional)...": "Session note (optional)...",
        "Assigned Tasks": "Assigned Tasks",
        "Completed": "Completed",
        "Pending": "Pending",
        "No tasks assigned yet.": "No tasks assigned yet.",
        "Send Task": "Send Task",
        "Breathing Exercise": "Breathing Exercise",
        "Meditation": "Meditation",
        "Daily Cards": "Daily Cards",
        "Support Wall": "Support Wall",
        "Apply breathing techniques": "Apply breathing techniques",
        "Do daily meditation": "Do daily meditation",
        "View motivation cards": "View motivation cards",
        "Post in the forum": "Post in the forum",
        "Please select a task type.": "Please select a task type.",
        "Takip": "Monitor",
        "Acil": "Urgent",
        "Normal": "Normal",
        "Private Notes": "Private Notes",
        "Notes load when a user is selected.": "Notes load when a user is selected.",
        "Save": "Save",
        "Session Rating History": "Session Rating History",

        // Forum translations
        "Share Your Story": "Share Your Story",
        "Write your story here...": "Write your story here...",
        "Share": "Share",
        "Like": "Like",
        "Comments": "Comments",
        "Add a comment...": "Add a comment...",
        "Send": "Send",
        "Anonymous": "Anonymous",
        "Previous": "Previous",
        "Next": "Next",
        "No posts yet.": "No posts yet.",
        "Be the first to share!": "Be the first to share!",
        "Bütün mesajlar okundu olarak işaretle": "Mark all as read"
    }
};

// Günlük Kartlar Havuzu
const DAILY_CARDS_POOL = [
    {
        icon: 'auto_awesome',
        tr: { title: 'Bugünün Sözü', quote: 'Her gün yeni bir başlangıçtır. Kendine inan ve güçlü kal.', encour: 'Bugün kendine güven' },
        en: { title: "Today's Quote", quote: 'Every day is a new beginning. Believe in yourself and stay strong.', encour: 'Trust yourself today' },
        color: 'card-lavender'
    },
    {
        icon: 'favorite',
        tr: { title: 'Motivasyon', quote: 'Küçük adımlar büyük değişimlere yol açar. Her gün bir adım at.', encour: 'Adım adım ilerle' },
        en: { title: 'Motivation', quote: 'Small steps lead to big changes. Take one step every day.', encour: 'Move forward step by step' },
        color: 'card-blue'
    },
    {
        icon: 'psychology',
        tr: { title: 'Düşünce', quote: 'Olumlu düşünceler, olumlu sonuçlar doğurur. Bugün kendine iyi davran.', encour: 'Pozitif kal' },
        en: { title: 'Thought', quote: 'Positive thoughts lead to positive results. Be kind to yourself today.', encour: 'Stay positive' },
        color: 'card-beige'
    },
    {
        icon: 'self_improvement',
        tr: { title: 'Farkındalık', quote: 'Şu anı yaşa, geçmişi bırak, geleceği planla ama bugüne odaklan.', encour: 'Anı yaşa' },
        en: { title: 'Mindfulness', quote: 'Live in the present, let go of the past, plan the future but focus on today.', encour: 'Live the moment' },
        color: 'card-mint'
    },
    {
        icon: 'healing',
        tr: { title: 'İyileşme', quote: 'Kendini sev ve kabul et. Mükemmel olmak zorunda değilsin, sadece kendin ol.', encour: 'Kendini sev' },
        en: { title: 'Healing', quote: "Love and accept yourself. You don't have to be perfect, just be yourself.", encour: 'Love yourself' },
        color: 'card-peach'
    },
    {
        icon: 'star',
        tr: { title: 'Başarı', quote: 'Başarı yolculuğu, her gün atılan küçük adımlarla başlar. Bugün senin günün.', encour: 'Başarıya odaklan' },
        en: { title: 'Success', quote: 'The journey to success begins with small steps taken every day. Today is your day.', encour: 'Focus on success' },
        color: 'card-lavender-light'
    },
    {
        icon: 'spa',
        tr: { title: 'Huzur', quote: 'İç huzur, dış dünyadaki fırtınalara rağmen sakin kalabilmektir.', encour: 'Sakinliğini koru' },
        en: { title: 'Peace', quote: 'Inner peace is staying calm despite the storms in the outside world.', encour: 'Keep your calm' },
        color: 'card-lavender'
    },
    {
        icon: 'bolt',
        tr: { title: 'Cesaret', quote: 'Cesaret korkusuzluk değil, korkuya rağmen ilerlemektir.', encour: 'Cesur ol' },
        en: { title: 'Courage', quote: 'Courage is not the absence of fear, but moving forward despite it.', encour: 'Be brave' },
        color: 'card-blue'
    },
    {
        icon: 'volunteer_activism',
        tr: { title: 'Şükran', quote: 'Sahip olduğun şeyler için şükretmek, daha fazlasının kapısını açar.', encour: 'Şükret' },
        en: { title: 'Gratitude', quote: 'Being grateful for what you have opens the door to more.', encour: 'Be grateful' },
        color: 'card-beige'
    },
    {
        icon: 'timer',
        tr: { title: 'Sabır', quote: 'En güzel şeyler sabırdan sonra gelir. Beklemeye değer.', encour: 'Sabırlı ol' },
        en: { title: 'Patience', quote: 'The most beautiful things come after patience. It is worth the wait.', encour: 'Be patient' },
        color: 'card-mint'
    },
    {
        icon: 'sentiment_very_satisfied',
        tr: { title: 'Gülümse', quote: 'Bir gülümseme dünyayı değiştirebilir. Bugün birine gülümse.', encour: 'Gülümse' },
        en: { title: 'Smile', quote: 'A smile can change the world. Smile at someone today.', encour: 'Smile' },
        color: 'card-peach'
    },
    {
        icon: 'fitness_center',
        tr: { title: 'Güç', quote: 'Gerçek güç, düştüğünde tekrar ayağa kalkabilme yeteneğidir.', encour: 'Güçlü kal' },
        en: { title: 'Strength', quote: 'True strength is the ability to get back up after you fall.', encour: 'Stay strong' },
        color: 'card-lavender-light'
    },
    {
        icon: 'wb_sunny',
        tr: { title: 'Umut', quote: 'En karanlık gece bile sona erer ve güneş tekrar doğar.', encour: 'Umudunu kaybetme' },
        en: { title: 'Hope', quote: 'Even the darkest night ends and the sun rises again.', encour: 'Keep hoping' },
        color: 'card-lavender'
    },
    {
        icon: 'military_tech',
        tr: { title: 'Disiplin', quote: 'Disiplin, ne istediğin ile neyi en çok istediğin arasındaki seçimdir.', encour: 'Disiplinli ol' },
        en: { title: 'Discipline', quote: 'Discipline is the choice between what you want now and what you want most.', encour: 'Be disciplined' },
        color: 'card-blue'
    },
    {
        icon: 'brush',
        tr: { title: 'Yaratıcılık', quote: 'Hayal gücü bilgiden daha önemlidir. Hayal kurmaktan korkma.', encour: 'Hayal et' },
        en: { title: 'Creativity', quote: "Imagination is more important than knowledge. Don't be afraid to dream.", encour: 'Imagine' },
        color: 'card-beige'
    },
    {
        icon: 'handshake',
        tr: { title: 'Nezaket', quote: 'Başkalarına karşı nazik ol, çünkü herkes zor bir savaş veriyor.', encour: 'Nazik ol' },
        en: { title: 'Kindness', quote: 'Be kind to others, for everyone is fighting a hard battle.', encour: 'Be kind' },
        color: 'card-mint'
    },
    {
        icon: 'center_focus_strong',
        tr: { title: 'Odak', quote: 'Nereye odaklanırsan, enerjin oraya akar. Hedefine odaklan.', encour: 'Odaklan' },
        en: { title: 'Focus', quote: 'Where you focus, your energy flows. Focus on your goal.', encour: 'Stay focused' },
        color: 'card-peach'
    },
    {
        icon: 'autorenew',
        tr: { title: 'Değişim', quote: 'Değişim kaçınılmazdır, gelişim ise isteğe bağlıdır. Gelişmeyi seç.', encour: 'Geliş' },
        en: { title: 'Change', quote: 'Change is inevitable, growth is optional. Choose to grow.', encour: 'Grow' },
        color: 'card-lavender-light'
    },
    {
        icon: 'verified_user',
        tr: { title: 'Özgüven', quote: 'Kendine güvendiğinde, başkalarının ne düşündüğü önemini yitirir.', encour: 'Kendine güven' },
        en: { title: 'Self-confidence', quote: 'When you trust yourself, what others think loses its importance.', encour: 'Trust yourself' },
        color: 'card-lavender'
    },
    {
        icon: 'local_fire_department',
        tr: { title: 'Tutku', quote: 'Tutkuyla yaptığın her şey, seni başarıya bir adım daha yaklaştırır.', encour: 'Tutkuyla yap' },
        en: { title: 'Passion', quote: 'Everything you do with passion brings you one step closer to success.', encour: 'Do it with passion' },
        color: 'card-blue'
    }
];

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
    
    // Popup göster (eğer showToast fonksiyonu varsa)
    if (typeof showToast === 'function') {
        setTimeout(() => {
            showToast('language', lang);
        }, 200);
    }
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
window.translations = translations; 