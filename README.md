<<<<<<< HEAD
# 🚀 Proje Adı

Bu proje, Python ve Django kullanılarak geliştirilmiş bir web uygulamasıdır.  
Aşağıdaki adımları izleyerek kendi bilgisayarınızda kolayca çalıştırabilirsiniz. 🎯

---
```bash
# 🧠 İyi Hisset – Psikolojik Destek ve İletişim Platformu

**İyi Hisset**, üyeler ile tek bir psikolog arasında güvenli, kalıcı ve gerçek zamanlı iletişim sağlayan bir psikolojik destek platformudur.  
Proje; mesajlaşma, görev atama, bildirim sistemi, kullanıcı istatistikleri ve rol bazlı erişim kontrolü gibi gelişmiş özellikler içerir.

---

## 🎯 Projenin Amacı

Bu projenin amacı:

- Üyelerin psikolog ile **özel ve güvenli** şekilde iletişim kurmasını sağlamak  
- Psikoloğun üyeleri tek bir panelden yönetebilmesi  
- Mesaj, görev ve bildirimlerin **kalıcı ve anlık** çalışması  
- Kullanıcı deneyimini artıran **responsive**, **dark/light mode**, **çok dilli** bir yapı sunmak  

---

## 👥 Kullanıcı Rolleri

### 👤 Üye (Member)
- Kayıt olabilir ve giriş yapabilir
- Sadece psikolog ile mesajlaşabilir
- Kendisine verilen görevleri görebilir
- Bildirimleri alır ve okunmamış sayısını görür
- Profil yönetimi sayfasında **gerçek istatistiklerini** görüntüler
- Psikolog veya admin sayfalarına erişemez

### 🧑‍⚕️ Psikolog (Psychologist)
- Database’de kayıtlı tek psikolog hesabı vardır
- Tüm üyeleri liste halinde görebilir
- Üyelere:
  - Mesaj gönderebilir
  - Görev atayabilir
  - Bildirim gönderebilir
- Psikolog dashboard ve psikoloğa özel profile-management sayfalarına erişebilir
- Normal üye dashboard’una yönlendirilmez

---

## 🔐 Giriş Sistemi

- Üye ve psikolog için **ayrı login sayfaları** bulunur
- Form çakışmaları ve doğrulama hataları engellenmiştir
- Kayıt sırasında:
  - Kullanıcı adı ve e-posta **anlık olarak database’den kontrol edilir**
  - Daha önce kullanılmışsa kullanıcıya anında uyarı verilir

---

## 💬 Mesajlaşma Sistemi

- Üye ↔ Psikolog arasında **birebir ve özel** mesajlaşma
- Mesajlar:
  - Database’e kaydedilir
  - Sayfa yenilemeden **anlık olarak güncellenir**
- Mesaj gönderme:
  - **Enter** → mesaj gönder
  - **Shift + Enter** → alt satır
- Aynı mesajın iki kez görünmesi problemi tamamen çözülmüştür

---

## 🔔 Bildirim Sistemi

### Üye Tarafı
- Bildirim türleri:
  - Psikolog mesajı
  - Psikolog bildirimi
  - Psikolog tarafından verilen görev
- Bildirim ikonunda:
  - Okunmamış bildirim sayısı **badge** ile gösterilir
- Bildirim paneli açıldığında:
  - Bildirimler otomatik olarak okundu sayılır
  - Badge sıfırlanır (DB tarafında da)

### Otomatik Görev Bildirimi
Psikolog bir görev verdiğinde üyeye otomatik bildirim oluşturulur:

> Psikolog tarafından "**görev metni**" görevi verilmiştir.

---

## 📋 Görev Sistemi

- Psikolog, üyeye görev atayabilir
- Görevler:
  - Database’de kalıcıdır
  - Üyenin **tüm sayfalarındaki sidebar** üzerinde eşzamanlı görünür
- Görev yoksa:
  - “Henüz görev yok” mesajı gösterilir

---

## 📊 Üye İstatistikleri (Gerçek Veriler)

Üye profile-management sayfasında gösterilen istatistikler **tamamen database’den hesaplanır**:

- **Aktif Günler**  
  Kullanıcının siteye giriş yaptığı farklı gün sayısı

- **Sohbet Seansları**  
  Kullanıcının psikolog ile en az 1 mesaj attığı gün sayısı

- **Görev Sayısı**  
  Psikoloğun o kullanıcıya verdiği toplam görev sayısı

❌ Ruh hali puanı sistemi kaldırılmıştır.

---

## 🎨 Tema, Dil ve Yazı Boyutu

- **Dark / Light Mode**
- **Türkçe / İngilizce dil desteği**
- **Font size ayarı**

Özellikler:
- Tema, dil ve font ayarları **tek kaynaktan** yönetilir
- Profile management’ta yapılan değişiklikler:
  - Dashboard dahil tüm sayfalara yansır
- Psikolog ve üye ayarları birbirinden bağımsızdır

---

## 📱 Responsive Tasarım

- **1200px üstü**
  - Sidebar sabit ve açık
- **1200px altı**
  - Hamburger menü ile sidebar açılıp kapanır
- Hiçbir sayfada:
  - Taşma
  - Üst üste binme
  - Kaybolan içerik bulunmaz

Profile-management sayfasında:
- Sidebar viewport’a sığar
- Sidebar ve ana içerik ayrı ayrı scroll alır

---

## 🛠️ Kullanılan Teknolojiler

- HTML5
- CSS3
- JavaScript
- Django
- Django Templates
- Django Authentication
- Django i18n (gettext / django.po)
- REST API
- Database (kalıcı veri yönetimi)

---

## ✅ Proje Durumu

✔️ Tamamlandı  
✔️ Test senaryoları uygulanmış  
✔️ Gerçek zamanlı mesajlaşma aktif  
✔️ Rol bazlı erişim güvenli  

---

## 📌 Not

Bu proje, hem **akademik (bitirme projesi)** hem de **gerçek hayatta kullanılabilir** bir sistem olarak tasarlanmıştır.  
Kod yapısı genişletilmeye ve yeni özellikler eklemeye uygundur.

---



